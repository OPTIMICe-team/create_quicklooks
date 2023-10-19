#----------------------------
# This script contains the functions used for
# resampling the data from:
# Joyrad10, Joyrad35, Mirac94, Grarad94
#
# Author: Jose Dias Neto
# OPTIMIce Emmy-Noether Group
# Institute for Geophysics and Meteorology
# University of Cologne
#---------------------------


import pandas as pd
import numpy as np
import xarray as xr
import netCDF4 as nc
import glob


#----------------------------
# Common functions used for processing X-, Ka-, W-Band radars
#
def getVar(var, tempDataSet, fileList,
           epoch='1970-01-01 00:00:00 UTC'):
    """
    Retrieves the desired radar variables from a list
    of radar files

    Parameters
    ----------
    var: dictionary of the desired variables
    tempDataSet: empty xarray dataset
    fileList: list of files from the same day
    epoch: Time reference used by the radar software
        to define the starting point. The W-Band radar
        uses 1970-01-01 00:00:00 UTC as starting reference time
        (default: 1970-01-01 00:00:00 UTC)

    Returns
    -------
    tempDataSet: xarray dataset containing the desired variables

    """

    for filePath in fileList:

        try:
            tempDS = xr.open_dataset(filePath)
            tempDS.time.attrs['units']='seconds since 1970-01-01 {0}'.format(epoch)
            tempDS = xr.decode_cf(tempDS)
            tempDSVar = tempDS[var]
            tempDataSet = xr.merge([tempDataSet, tempDSVar])

        except:
            print(filePath, var)
            tempDataSet = tempDataSet

    return tempDataSet


def calcRadarDeltaGrid(refGrid, radarGrid):
    """
    Calculates the distance between the reference grid
    and the radar grid (time or range)

    Parameters
    ----------
    refGrid: reference grid (array[n])
    radarGrid: radar grid (array[m])

    Returns
    -------
    deltaGrid: distance between each element from
        the reference grid to each element from the
        radar grid

    """

    radGrid2d = np.ones((len(refGrid),
                         len(radarGrid)))*radarGrid

    deltaGrid = radGrid2d - np.reshape(refGrid,(len(refGrid),1))

    return deltaGrid


def getNearestIndexM2(deltaGrid, tolerance):
    """
    Identify the index of the deltaGrid that fulfil
    the resampling tolerance

    Parameters
    ----------
    deltaGrid: output from calcRadarDeltaGrid
    tolerance: tolerance distance for detecting
        the closest neighbour (time or range)

    Returns
    -------
    gridIndex: array of indexes that fulfil the resampling
        tolerance

    """

    gridIndex = np.argmin(abs(deltaGrid), axis=1)
    deltaGridMin = np.min(abs(deltaGrid), axis=1)
    gridIndex = np.array(gridIndex, np.float)
    gridIndex[deltaGridMin>tolerance] = np.nan

    return gridIndex


def getResampledVar(var, xrDataset, timeIndexArray, rangeIndexArray):
    """
    It resamples a given radar variable using the
    time and range index calculated by getNearestIndexM2

    Parameters
    ----------
    var: radar variable name to be resampled
    xrDataset: xarray dataset containing the variables to
        be resampled
    timeIdexArray: time resampling index (output from getNearestIndexM2)
    rangeIndexArray: range resampling index (output from getNearestIndexM2)

    Returns
    -------
    resampledArr: time/range resampled numpy array

    """

    resampledArr = np.ones((timeIndexArray.shape[0],rangeIndexArray.shape[0]))*np.nan
    resampledTimeArr = np.ones((timeIndexArray.shape[0], xrDataset.range.values.shape[0]))*np.nan

    for t, timeIndex in enumerate(timeIndexArray):

        try:
            resampledTimeArr[t]=  xrDataset[var].values[int(timeIndex)]

        except:
            pass

    resampledTimeArrTra = resampledTimeArr.T
    resampledArr = resampledArr.T

    for r, rangeIndex in enumerate(rangeIndexArray):

        try:
            resampledArr[r] = resampledTimeArrTra[int(rangeIndex)]

        except:
            pass

    return resampledArr.T


def getTimeRef(date, dateFreq='2s'):
    """
    Genetates the time reference grid used for
    resampling the data

    Parameters
    ----------
    date: date for resampling (pandas Timestamp)
    dateFreq: resolution of the reference grid (str, default=2s)

    Returns
    -------
    timeRef: time reference grid (DatetimeIndex)

    """

    start = pd.datetime(date.year,
                        date.month,
                        date.day,
                        0, 0, 0)

    end = pd.datetime(date.year,
                      date.month,
                      date.day,
                      23, 59, 59)

    timeRef = pd.date_range(start, end, freq=dateFreq)

    return timeRef
#----------------------------


#----------------------------
# Functions used only for processing Ka-Band radar
#
def dropTimeDuplicates(xrDS1, xrDS2):
    """
    Experimental function for merging 2 datasets with
    time duplicates

    Parameters
    ----------
    xrDS1: a given xarray dataset A
    xrDS2: a given xarray dataset B

    Returns
    -------
    clearDS: time duplicates free xarray dataset

    """

    pdDF1 = pd.DataFrame(xrDS1.sk.values, index=xrDS1.time.values)
    pdDF1['times'] = xrDS1.time.values

    pdDF2 = pd.DataFrame(xrDS2.sk.values, index=xrDS2.time.values)
    pdDF2['times'] = xrDS2.time.values

    mergedDF = pdDF1.append(pdDF2)
    mergedDF = mergedDF.sort_values(by=['times'], ascending=[True])
    cleanDF = mergedDF.drop_duplicates(subset=['times'])
    del cleanDF['times']

    cleanDA = xr.DataArray(cleanDF.values,
                           dims=('time','range'),
                           coords={'range':xrDS1.range,
                                   'time':cleanDF.index})

    cleanDA.time.attrs = xrDS1.time.attrs
    cleanDS = xr.Dataset({'sk':cleanDA})
    {'Zg': None,'RMSg':None,'VELg':None, 'elv':None}

    return cleanDS
#----------------------------


#----------------------------
# Functions used only for processing W-Band radar
#
def getDataWband(variablesToGet, datasetNC, epoch):
    """
    It extracts the desired data from the
    radar files

    Parameters
    ----------
    variablesToGet: dictionary of the variables to
        be retrieved
    datasetNC: original full w-band data converted
        to a xarray dataset
    epoch: Time reference used by the radar software
        to define the starting point.

    Returns
    -------
    joyrad94Temp: xarray dataset containing the
        retrieved variables

    """

    epoch = pd.to_datetime(epoch)

    for var in variablesToGet.keys():

        correcTime = epoch + pd.to_timedelta(datasetNC['time'][:], unit='s')
        tempVar = xr.DataArray(datasetNC[var][:],
                           coords={'time':correcTime, 'range':datasetNC['range'][:]},
                           dims=('time', 'range'))

        variablesToGet[var]=tempVar

    joyrad94Temp = xr.Dataset({'Zg':variablesToGet['ze'],
                       'VELg':variablesToGet['vm'],
                       'RMSg':variablesToGet['sw'],})
    joyrad94Temp.time.attrs['units']='seconds since 1970-01-01 00:00:00 UTC'

    return joyrad94Temp


def getVarWband(variablesToGet, tempDataSet,
                fileList, epoch='2001-01-01 00:00:00'):
    """
    Retrieves the desired radar variables from a list
    of radar files

    Parameters
    ----------
    variablesToGet: dictionary of the desired variables
    tempDataSet: empty xarray dataset
    fileList: list of files from the same day
    epoch: Time reference used by the radar software
        to define the starting point. The W-Band radar
        uses 2001-01-01 00:00:00 as starting reference time
        (default: 2001-01-01 00:00:00)

    Returns
    -------
    tempDataSet: xarray dataset containing the desired variables

    """

    for filePath in fileList:

        try:
            joyrad94NC = nc.Dataset(filePath)
            tempDSVar = getDataWband(variablesToGet, joyrad94NC, epoch)
            tempDataSet = xr.merge([tempDataSet, tempDSVar])

        except:
            print('ERROR some where'+filePath)
            tempDataSet = tempDataSet


    #grarad94[var].attrs = tempDSVar.attrs
    return tempDataSet

#----------------------------

#----------------------------
# This script is used for resampling the data from X and Ka-Band from METEK
# Author: Jose Dias Neto 
# OPTIMIce Emmy-Noether Group
# Institute for Geophysics and Meteorology
# University of Cologne
#----------------------------


import resampleLib as rspl
from sys import argv
import pandas as pd
import numpy as np
import xarray as xr
import glob
import os

scriptname, date,dataPath,dataPathOutput,Band = argv #, date,dataPath,dataPathOutput,Band
print(date)
date = pd.to_datetime(date)
#print(date)
#quit()
'''
input: 
date: date that you want to have processed
dataPath: path where the X-band data is stored
dataPathOutput: path where to put the resampled netcdf file
Band: either X or Ka
'''

#----------------------------
# This block defines the range reference grid.
# The reference grid is the same for all radars
#
beginRangeRef = 0 # starting height of the ref grid
endRangeRef = 12000 # ending height of the ref grid
rangeFreq = 36 # range resolution of the ref grid
rangeTolerance = 18 # tolerance for detecting the closest neighbour

rangeRef = np.arange(beginRangeRef, endRangeRef, rangeFreq)
#
#----------------------------

# time tolerance for detecting closest neighbour (seconds)
timeTolerance = '2S'
timeFreq = '4S'
# getting the time reference grid

timeRef = timeRef = pd.date_range(date, date+pd.offsets.Day(1)-pd.offsets.Second(1), freq=timeFreq)
# Height offset, it is set to 2.2 here because the height
# of W-Band is the reference
if Band == 'Ka':
	rangeOffset = 2.2
else:
	rangeOffset = 0.32
# defining the input file name
dataFilePath = '{path}/{year}/{month}/{day}/{date}_??????.znc'.format(path=dataPath,
																			year = date.strftime('%Y'),
																			month = date.strftime('%m'),
																			day = date.strftime('%d'), 
																			date = date.strftime('%Y%m%d'))

# retrieving a list of files from the same day
dataFileList = sorted(glob.glob(dataFilePath))
if Band == 'Ka':
	var2proc = ['Zg','RMSg','VELg','LDRg','SKWg']
else:
	var2proc = ['Zg','RMSg','VELg','SKWg']
if dataFileList:
	# now read in all available files
	try: # we have to do try here, because sometimes files are broken and then it doesn't work to use open_mfdataset
		data = xr.open_mfdataset(dataFileList)
		data = data[var2proc]
	except: 
		data = xr.Dataset()
		for f in dataFileList: # if one file is broken, loop through all the files and open individually, except for the one which is not working
			try: 
				dataSmall = xr.open_dataset(f)
				data = xr.merge([data,dataSmall[var2proc]])
			except:
				print('cannot open ',f)
	
	#- sometimes we have duplicates in time
	_, index_time = np.unique(data['time'], return_index=True)
	data = data.isel(time=index_time)
	data.time.attrs['units']='seconds since {0}'.format('1970-01-01 00:00:00 UTC')
	data = xr.decode_cf(data)
	#

	# simplistic spurious data filtering
	#joyrad10 = joyrad10.where(joyrad10['Zg']>0)

	
	# correcting the range offset
	data['range'] = data.range.values + rangeOffset

	# resample along range
	data = data.reindex({'range':rangeRef},method='nearest',tolerance=rangeTolerance)
	data =data.reindex({'time':timeRef},method='nearest',tolerance=timeTolerance)

	#- converting Zg to log:
	# converting Zg to log units
	if Band == 'Ka':
		convert = ['Zg','LDRg']
	else:
		convert = ['Zg']
	for var in convert:
		data[var] = 10*np.log10(data[var])
		data[var].attrs['units'] = 'dB'

	# defining the final output path + name
	outPutFileName = '{path}/{date}_mom_{band}-band.nc'.format(path=dataPathOutput,
																		date=date.strftime('%Y%m%d'),band=Band)
		     
	# saving the resampled data into a netCDF file
	print(outPutFileName)
	# if we already have the file, sometimes it won't overwrite it, so just remove the already existing one
	if os.path.exists(outPutFileName):
		os.remove(outPutFileName)
	encoding = {k:{'zlib': True} for k in data}
	data.to_netcdf(outPutFileName,encoding=encoding)
	data.close()
	print('done with resampling')
else:
	print('no files found ', dateStr)



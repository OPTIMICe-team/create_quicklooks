#----------------------------
# This script contains the functions used for 
# creating the quicklook plots
# Author: Jose Dias Neto 
# OPTIMIce Emmy-Noether Group
# Institute for Geophysics and Meteorology
# University of Cologne
#----------------------------


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt 
from sys import argv
import pandas as pd
import xarray as xr
import numpy as np


def plotLDRWKa(data35, data94, vmax, vmin,
            pathOut, date, varName,CEL=True):
    """
    It plots the resmpled LDR

    Parameters
    ----------
    data35: xarray dataset of the resampled Joyrad35
    data94: xarray dataset of the resampled wand-scan 
    vmax: maximum color value
    vmin: mininum color value
    pathOut: path to save the plot
    date: date of the plotting day
    varName: variable name in the xarray dataset
    CEL: if measurements are at 30°CEL
    Returns
    -------
    no returned value
    """
    
    fig, axes = plt.subplots(nrows=2, figsize=(18,12))
    radData = {'rad35':{'data':data35['LDR_ka'], 'axis':axes[0],'cbLabel':'LDR [dB]'},
               'rad94':{'data':data94['sLDR_w'], 'axis':axes[1],'cbLabel':'slanted LDR [dB]'}}
    for rad in radData.keys():           
        plot = radData[rad]['data'].plot(x='time',ax=radData[rad]['axis'], cmap='jet',
                               vmax=vmax, vmin=vmin,add_colorbar=False)
        
        radData[rad]['axis'].set_title(rad,fontsize=18)
        cb = plt.colorbar(plot,ax=radData[rad]['axis'])
        cb.set_label(radData[rad]['cbLabel'],fontsize=18)
        cb.ax.tick_params(labelsize=16)
        plt.setp(plot.axes.xaxis.get_majorticklabels(), rotation=0)
        radData[rad]['axis'].grid()
        radData[rad]['axis'].set_xlabel('')
        radData[rad]['axis'].tick_params(axis='y',labelsize=16)
        radData[rad]['axis'].tick_params(axis='x',labelsize=16)
        radData[rad]['axis'].set_ylabel('range [m]',fontsize=18)
        plt.tight_layout()  
 
    if CEL == True:
        fileName = ('_').join([date,varName+'_CEL.png'])
    else:
        fileName = ('_').join([date,varName+'.png'])
    filePathName = ('/').join([pathOut,fileName])
    plt.savefig(filePathName, format='png', dpi=200, bbox_inches='tight')

    #plt.show()
    plt.close()

    return None
def plotLDR(data35, vmax, vmin,
            pathOut, date, varName):
    """
    It plots the resmpled LDR

    Parameters
    ----------
    data35: xarray dataset of the resampled Joyrad35
    
    vmax: maximum color value
    vmin: mininum color value
    pathOut: path to save the plot
    date: date of the plotting day
    varName: variable name in the xarray dataset
    
    Returns
    -------
    no returned value
    """
    
    fig, axes = plt.subplots(nrows=1, figsize=(18,6))
    plot = data35['LDRg'].plot(x='time',ax=axes, cmap='jet',
                               vmax=vmax, vmin=vmin,add_colorbar=False)
        
    axes.set_title('LDR Ka',fontsize=18)
    cb = plt.colorbar(plot,ax=axes)
    cb.set_label('LDR [dB]',fontsize=18)
    cb.ax.tick_params(labelsize=16)
    plt.setp(plot.axes.xaxis.get_majorticklabels(), rotation=0)
    axes.grid()
    axes.set_xlabel('')
    axes.tick_params(axis='y',labelsize=16)
    axes.tick_params(axis='x',labelsize=16)
    axes.set_ylabel('range [m]',fontsize=18)
    plt.tight_layout()  
 
    fileName = ('_').join([date,varName+'.png'])
    filePathName = ('/').join([pathOut,fileName])
    plt.savefig(filePathName, format='png', dpi=200, bbox_inches='tight')

    #plt.show()
    plt.close()

    return None

def plotVar(data35, data94,
            vmax, vmin, pathOut, date,
            varName,units,CEL=True,data10=[],cmap='nipy_spectral'):
    """
    It plots dual panels of a given variable

    Parameters
    ----------
    data35: xarray dataset of the resampled Joyrad35
    data94: xarray dataset of the resampled Joyrad94
    vmax: maximum color value
    vmin: mininum color value
    pathOut: path to save the plot
    date: date of the plotting day
    varName: variable name in the xarray dataset
    optional: 
    data10: xarray dataset of the resampled Joyrad10
    CEL: if the measurements are taken from the tripex-pol-scan CEL measurements
    Returns
    -------
    no returned value
    """   
    if CEL == True:
        fig, axes = plt.subplots(nrows=2, figsize=(18,12))

        radData = {'rad35':{'data':data35, 'axis':axes[0],'cbLabel':varName+' '+units},
                   'rad94':{'data':data94, 'axis':axes[1],'cbLabel':varName+' '+units}}
    else:
        fig, axes = plt.subplots(nrows=3, figsize=(18,18))

        radData = {'rad10':{'data':data10, 'axis':axes[0],'cbLabel':varName+' '+units},
                   'rad35':{'data':data35, 'axis':axes[1],'cbLabel':varName+' '+units},
                   'rad94':{'data':data94, 'axis':axes[2],'cbLabel':varName+' '+units}}

    for rad in radData.keys():

        #plot = #radData[rad]['data'].T.plot(ax=radData[rad]['axis'],
                #                    cmap='jet', vmax=vmax, vmin=vmin,add_colorbar=False)
        plot = ax=radData[rad]['axis'].pcolormesh(radData[rad]['data'].time,
                                                    radData[rad]['data'].range,
                                                    radData[rad]['data'].T,cmap=cmap, vmax=vmax, vmin=vmin)
        radData[rad]['axis'].set_title(rad,fontsize=18)
        cb = plt.colorbar(plot,ax=radData[rad]['axis'])
        cb.set_label(radData[rad]['cbLabel'],fontsize=18)
        cb.ax.tick_params(labelsize=16)
        plt.setp(plot.axes.xaxis.get_majorticklabels(), rotation=0)
        radData[rad]['axis'].grid()
        radData[rad]['axis'].set_xlabel('')
        radData[rad]['axis'].tick_params(axis='y',labelsize=16)
        radData[rad]['axis'].tick_params(axis='x',labelsize=16)
        radData[rad]['axis'].set_ylabel('range [m]',fontsize=18)
        plt.tight_layout()

    if CEL == True:
        fileName = ('_').join([date,varName+'_CEL.png'])
    else:
        fileName = ('_').join([date,varName+'.png'])
    filePathName = ('/').join([pathOut,fileName])
    plt.savefig(filePathName, format='png', dpi=200, bbox_inches='tight')

    #plt.show()
    plt.close()

    return None


def plotDiffVar(diff3594,
                vmax, vmin, pathOut, date,
                varName,units, CEL=True,diff1035=[],cmap='nipy_spectral'):

    """
    It plots double panels differences of a given variable

    Parameters
    ----------
    diff1035: variable difference (radar-10 - radar-35)
    diff3594: variable difference (radar-35 - radar-94)
    vmax: maximum color value
    vmin: mininum color value
    pathOut: path to save the plot
    date: date of the plotting day
    varName: variable name in the xarray dataset

    Returns
    -------
    no returned value
    """
    if CEL == True:
        fig, axes = plt.subplots(nrows=1, figsize=(18,6))

        radData = {'diff_35_94':{'data':diff3594, 'axis':axes,'cbLabel':varName+' '+units},
                   }
    else:
        fig, axes = plt.subplots(nrows=2, figsize=(18,12))

        radData = {'diff_10_35':{'data':diff1035, 'axis':axes[0],'cbLabel':varName+' '+units},
                   'diff_35_94':{'data':diff3594, 'axis':axes[1],'cbLabel':varName+' '+units},
                   }

    for rad in radData.keys():

        #plot = radData[rad]['data'].T.plot(ax=radData[rad]['axis'],
         #                           cmap='nipy_spectral', vmax=vmax, vmin=vmin,add_colorbar=False)
        plot = radData[rad]['axis'].pcolormesh(radData[rad]['data'].time,
                                                radData[rad]['data'].range,
                                                radData[rad]['data'].T,cmap=cmap, vmax=vmax, vmin=vmin)

        if rad == 'diff_10_35' and varName == 'DWR':

            radData[rad]['axis'].set_title(rad + ' (Zg Ka - 0 dB offset)',fontsize=18)

        elif rad == 'diff_35_94' and varName == 'DWR':

            radData[rad]['axis'].set_title(rad + ' (Zg Ka - 0 dB, Ze W 0 dB [offset])',fontsize=18)


        else:
            radData[rad]['axis'].set_title(rad,fontsize=18)

        cb = plt.colorbar(plot,ax=radData[rad]['axis'])
        cb.set_label(radData[rad]['cbLabel'],fontsize=18)
        cb.ax.tick_params(labelsize=16)
        plt.setp(plot.axes.xaxis.get_majorticklabels(), rotation=0)
        radData[rad]['axis'].grid()
        radData[rad]['axis'].set_xlabel('')
        radData[rad]['axis'].tick_params(axis='y',labelsize=16)
        radData[rad]['axis'].tick_params(axis='x',labelsize=16)
        radData[rad]['axis'].set_ylabel('range [m]',fontsize=18)
        plt.tight_layout()
    if CEL == True:
        fileName = ('_').join([date,varName+'_CEL.png'])
    else:
        fileName = ('_').join([date,varName+'.png'])
    filePathName = ('/').join([pathOut,fileName])
    plt.savefig(filePathName, format='png', dpi=200, bbox_inches='tight')

    #plt.show()
    plt.close()

    return None

def getNewNipySpectral():

    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    numEnt = 15

    viridis = cm.get_cmap('nipy_spectral', 256)
    newcolors = viridis(np.linspace(0, 1, 256))

    colorSpace = np.linspace(198, 144, numEnt)/256
    colorTest=np.zeros((numEnt,4))
    colorTest[:,3] = 1
    colorTest[:,0]=colorSpace

    newcolors[- numEnt:, :] = colorTest
    newcmp = ListedColormap(newcolors)

    return newcmp

def plotPol(data,plotOutPath, strDate, plotID, colmap='gist_ncar'):
    fig, axes = plt.subplots(nrows=4, figsize=(18,24))
    radData = {'ZDR':{'data':data, 'axis':axes[0], 'lim':(-1,4),'cmap':colmap,'cbLabel':'ZDR [dB]'},
               'KDP':{'data':data, 'axis':axes[1], 'lim':(-1,4), 'cmap':colmap,'cbLabel':r'KDP [°km$^{-1}$]'},
               'sZDRmax':{'data':data, 'axis':axes[2], 'lim':(-1,4), 'cmap':colmap,'cbLabel':'sZDRmax [dB]'},
               'RHV':{'data':data, 'axis':axes[3], 'lim':(0.85,1.001), 'cmap':colmap+'_r','cbLabel':'RhoHV'}}
    for rad in radData.keys():
        plot = radData[rad]['data'][rad].T.plot(ax=radData[rad]['axis'],
                                           vmax=radData[rad]['lim'][1],
                                           vmin=radData[rad]['lim'][0],
                                           cmap=radData[rad]['cmap'],add_colorbar=False)
        cb = plt.colorbar(plot,ax=radData[rad]['axis'])
        cb.set_label(radData[rad]['cbLabel'],fontsize=18)
        cb.ax.tick_params(labelsize=16)
        radData[rad]['axis'].set_title(rad,fontsize=18)
        plt.setp(plot.axes.xaxis.get_majorticklabels(), rotation=0)
        radData[rad]['axis'].grid()
        radData[rad]['axis'].set_xlabel('')
        radData[rad]['axis'].tick_params(axis='y',labelsize=16)
        radData[rad]['axis'].tick_params(axis='x',labelsize=16)
        radData[rad]['axis'].set_ylabel('height [m]',fontsize=18)
        plt.tight_layout()
    plotFileName = ('_').join([strDate,plotID])
    filePathName = ('/').join([plotOutPath,plotFileName])
    plt.savefig(filePathName+'.png',dpi=200, bbox_inches='tight')
    plt.close()
    return None

def plot_RHI(data, variable_name, color_lim = [1, 2], colormap='gnuplot'):

    fig,ax = plt.subplots(figsize=(18, 10))
       
    plt.pcolormesh(data['range']*np.cos(np.deg2rad(data['elevation'])), data['range']*np.sin(np.deg2rad(data['elevation'])), variable, shading='auto')
    
    plt.axis('scaled')
    plt.clim(color_lim) 
    #plt.colorbar()
    plt.set_cmap(colormap)
    #plt.title('RHI: '+variable_name + ' - ' + time[0].strftime("%d/%m/%Y, %H:%M"))
    return fig

def getNewNipySpectral():

    from matplotlib import cm
    from matplotlib.colors import ListedColormap

    numEnt = 15

    viridis = cm.get_cmap('nipy_spectral', 256)
    newcolors = viridis(np.linspace(0, 1, 256))

    colorSpace = np.linspace(198, 144, numEnt)/256
    colorTest=np.zeros((numEnt,4))
    colorTest[:,3] = 1
    colorTest[:,0]=colorSpace

    newcolors[- numEnt:, :] = colorTest
    newcmp = ListedColormap(newcolors)

    return newcmp


#----------------------------
# This script is used for creating the plots.
# Author: Jose Dias Neto 
# OPTIMIce Emmy-Noether Group
# Institute for Geophysics and Meteorology
# University of Cologne
#----------------------------


import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
#----------------------------
# This script is used for plotting the quicklooks of triple frequency setup
# Author: Jose Dias Neto 
# OPTIMIce Emmy-Noether Group
# Institute for Geophysics and Meteorology
# University of Cologne
#----------------------------


from sys import argv
import pandas as pd
import xarray as xr
import numpy as np
import plottingLib as plib
import resampleLib as rsp
import os

scriptname, date, dataPath, dataPathOutput, emptyDataPath = argv #, date,dataPath,dataPathOutput,Band
print(date)
date = pd.to_datetime(date)
'''
input: 
date: date that you want to have processed
dataPath: path where the X-band data is stored
dataPathOutput: path where to put the plot
emptyDataPath: path to where there is a nc file with empty data in it
'''

#----------------------------
# This is the main processing block for
# for plotting the resampled data
#

print('plotting: {0}'.format(date))

# trying to oppen the resampled joyrad10 data
try:
	fileName10 = date.strftime('%Y%m%d')+'_mom_X-band.nc'
	filePath10 = ('/').join([dataPath, fileName10])
	data10 = xr.open_dataset(filePath10)

# reading an empty dataset in case joyrad10 does not exist
except:
	data10 = xr.open_dataset(emptyDataPath)
	# time tolerance for detecting closest neighbour (seconds)
	timeTolerance = '2S'
	timeFreq = '4S'
	timeRef = pd.date_range(date, date+pd.offsets.Day(1)-pd.offsets.Second(1), freq=timeFreq)
	data10=data10.reindex({'time':timeRef},method='nearest',tolerance='1S')
	print("couldn't open joyrad10 file at ", filePath10)
	# trying to oppen the resampled joyrad10 data
try:
	fileName35 = date.strftime('%Y%m%d')+'_mom_Ka-band.nc'
	filePath35 = ('/').join([dataPath, fileName35])
	data35 = xr.open_dataset(filePath35)

	# creating an empty dataset in case joyrad35 does not exist
except:
	data35 = xr.open_dataset(emptyDataPath)
	timeTolerance = '2S'
	timeFreq = '4S'
	timeRef = pd.date_range(date, date+pd.offsets.Day(1)-pd.offsets.Second(1), freq=timeFreq)
	data35=data35.reindex({'time':timeRef},method='nearest',tolerance='1S')
	
# trying to oppen the grarad94 orher 94 GHz radar
try:
	fileName94 = date.strftime('%Y%m%d')+'_ZEN_moments_wband_scan.nc'
	filePath94 = ('/').join([dataPath, fileName94])
	data94 = xr.open_dataset(filePath94)
	data94 = data94.rename({'Ze':'Zg','MDV':'VELg','WIDTH':'RMSg','sLDR':'sLDR_w','SK':'SKWg'})
# creating an empty dataset in case grarad does not exist
except:
	fileName94 = date.strftime('%Y%m%d')+'_ZEN_moments_wband_scan.nc'
	filePath94 = ('/').join([dataPath, fileName94])
	print('couldnt find data94 file at ',filePath94)
	data94 =xr.open_dataset(emptyDataPath)
	timeTolerance = '2S'
	timeFreq = '4S'
	timeRef = pd.date_range(date, date+pd.offsets.Day(1)-pd.offsets.Second(1), freq=timeFreq)
	data94=data94.reindex({'time':timeRef},method='nearest',tolerance='1S')
	
#---------------------------------------
# Use this block in case an Ze offset
# correction is needed
#
#data10['Zg'] = data10['Zg'] + offsetX
#data35['Zg'] = data35['Zg'] + offsetKa
#data94['Zg'] = data94['Zg'] + offsetW
#---------------------------------------
# defining the variable and the color range
# used by the plotting function
print(data10)
print(data35)
print(data94)
#quit()
variables = {'Zg':{'vmax':25, 'vmin':-35,'units':'[dB]'},
             'VELg':{'vmax':0, 'vmin':-3,'units':r'[ms$^{-1}$]'},
             'RMSg':{'vmax':0, 'vmin':1,'units':r'[ms$^{-1}$]'},
             'SKWg':{'vmax':1, 'vmin':-1,'units':r'[]'},
            }

# creating the triple panels plot

for var in variables.keys():

	plib.plotVar(data35[var], data94[var],
		    variables[var]['vmax'], variables[var]['vmin'],
		    dataPathOutput, date.strftime('%Y%m%d'), var,variables[var]['units'],CEL=False,data10=data10[var])
	print(var,' plotted ZEN')

# creating LDR plot

#plib.plotLDR(data35, -20, -35, dataPathOutput, date.strftime('%Y%m%d'), 'LDR_ka')
#print('ZEN LDR plotted')

# defining the color range and the name of the
# differences used by the plotting function
variables = {'Zg':{'vmax':20, 'vmin':-5, 'name':'DWR','units':'[dB]'},
             'VELg':{'vmax':0.3, 'vmin':-0.3, 'name':'DDV','units':r'[ms$^{-1}$]'},
             'RMSg':{'vmax':0.3, 'vmin':-0.3, 'name':'DSW','units':r'[ms$^{-1}$]'}
            }

# creating the difference plots
for var in variables.keys():
	diff1035 = data10[var] - data35[var]
	diff3594 = data35[var] - data94[var]

	diff1035.attrs['long_name']=variables[var]['name']+'-XKa'
	diff3594.attrs['long_name']=variables[var]['name']+'-KaW'

	plib.plotDiffVar(diff3594,
		        variables[var]['vmax'], variables[var]['vmin'],
		        dataPathOutput, date.strftime('%Y%m%d') , variables[var]['name'],variables[var]['units'],CEL=False,diff1035=diff1035)
print('plotted difference variable ZEN')
# closing all files

 

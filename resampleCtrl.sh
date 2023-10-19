# This script resamples all netcdf files of TODAY onto a common grid and then plots the quicklooks
# author: Leonie von Terzi

cd # go to home, makes it easier for the structure 

pathPro=/project/meteo/work/L.Terzi/radar_quicklooks/create_quicklooks # this is the path to all of your resampling and plotting scripts

#pathKaBand=
pathXBand=/archive/meteo/external-obs/juelich/joyrad10/

pathOutput=/scratch/l/L.Terzi/test_resampling_ouptut/resampled/
emptyDataPath=/scratch/l/L.Terzi/campaign_aux_data/tripex-pol/auxPlotData/noData2.nc

# this is for today, to test I am just going back a while to where I still have X-band data
#current_date=$(date +%Y%m%d)
current_date=20221206
echo $current_date



echo @@@@@@@@@@@@@@@@@@@@@@@
#date

echo Starting X-Band resampling
python3 $pathPro/resampleXKaBand.py $current_date $pathXBand $pathOutput X

#echo Starting Ka-Band resampling
#python3 $pathPro/resampleXKaBand.py  $current_date $pathXKa $pathOutput Ka

#echo Starting wband_scan
#python3 $pathPro/resampleWbandScan.py $argument:ZEN

echo Starting the plot routine
python3 $pathPro/tripex_pol_plots.py $current_date $pathOutput $pathOutput $emptyDataPath



echo finished
echo -----------------------


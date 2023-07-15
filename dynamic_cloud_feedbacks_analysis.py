'''
Produces plots used in dynamic cloud feedbacks paper
'''

import datetime
import numpy as np
# import matplotlib.pyplot as plt
# from netCDF4 import num2date
from scipy.ndimage import uniform_filter # uniform_filter_1d
from os.path import isfile
import _pickle as cPickle
# import pickle
# import os
# import matplotlib.colors as colors
# from scipy import interpolate
# import cartopy.crs as ccrs
# import cartopy.feature as feature
# from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import matplotlib.ticker as mticker
import bz2
# from matplotlib.patches import Patch
# from scipy.optimize import curve_fit
# from scipy.stats import mode as stats_mode
# from numpy.random import Generator, PCG64
import cf
import glob


# cmip6_hatch_dict = {'HadGEM3-GC31-LL' : '/',
#                     'HadGEM3-GC31-MM' : '\\',
#                     'BCC-CSM2-MR' : '/', 
#                     'BCC-ESM1' : '||',
#                     'CAMS-CSM1-0' : '-', 
#                     'FGOALS-f3-L' : '+',
#                     'CNRM-CM6-1' : 'x',
#                     'CNRM-EMS2-1' : 'o',
#                     'IPSL-CM6A-LR' : 'O',
#                     'MIROC6' : 'x-', 
#                     'UKESM1-0-LL' : '.',
#                     'MRI-ESM2-0' : '*',
#                     'GISS-E2-1-G' : '.O',
#                     'CESM2' : '\\||',
#                     'CESM2-WACCM' : '/||',
#                     'GFDL-AM4' : '\\-',
#                     'GFDL-CM4' : '/-',
#                     'SAM0-UNICON' :'o|',
#                     'Obs' : '*-'}
# colorlist = ['#e66101','#fdb863','#b2abd2','#5e3c99', 'k'] # From colorbrewer, colorblind friendly, greyscale friendly, color print friendly and lcd screen friendly :-)
# colorlist2 = ['#e66101','#b2abd2','#fdb863','#5e3c99', 'k'] # Order changed to maximise contrast if only using two colours.
# cmip6_color_dict = {'HadGEM3-GC31-LL' : colorlist[0],
#                     'HadGEM3-GC31-MM' : colorlist[1],
#                     'BCC-CSM2-MR' : colorlist[2], 
#                     'BCC-ESM1' : colorlist[3],
#                     'CAMS-CSM1-0' : colorlist[0], 
#                     'FGOALS-f3-L' : colorlist[1],
#                     'CNRM-CM6-1' : colorlist[2],
#                     'CNRM-EMS2-1' : colorlist[3],
#                     'IPSL-CM6A-LR' : colorlist[0],
#                     'MIROC6' : colorlist[1], 
#                     'UKESM1-0-LL' : colorlist[2],
#                     'MRI-ESM2-0' : colorlist[3],
#                     'GISS-E2-1-G' : colorlist[0],
#                     'CESM2' : colorlist[1],
#                     'CESM2-WACCM' : colorlist[2],
#                     'GFDL-AM4' : colorlist[3],
#                     'GFDL-CM4' : colorlist[0],
#                     'SAM0-UNICON' : colorlist[1],
#                     'Obs' : 'grey'}
# cmip6_resolution = {
#                     'HadGEM3-GC31-LL' : [1.25,1.875,85],
#                     'HadGEM3-GC31-MM' : [0.555,0.833,85],
#                     'BCC-CSM2-MR' : [1.125, 1.0, 46], 
#                     'BCC-ESM1' : [2.8, 2.8, 26],
#                     'CAMS-CSM1-0' : [1.125, 1, 31],
#                     'CanESM5' : [2.8, 2.8, 49],
#                     'E3SM-1-0' : [1.0, 1.0, 72],
#                     'FGOALS-f3-L' : [0.94, 0.94, 32],
#                     'CNRM-CM6-1' : [1.40,1.41,91],
#                     'CNRM-EMS2-1' : [1.40,1.41,91],
#                     'IPSL-CM6A-LR' : [1.27, 2.5, 79],
#                     'MIROC6' : [1.40, 1.40, 81], 
#                     'NorESM2-LM' : [2.0, 2.0, 32], 
#                     'TaiESM1' : [0.9, 1.25, 30], 
#                     'UKESM1-0-LL' : [1.25,1.875,85],
#                     'MRI-ESM2-0' : [1.12, 1.125, 80],
#                     'GISS-E2-1-G' : [2.0, 2.5, 40],
#                     'CESM2' : [0.94, 1.25, 32],
#                     'CESM2-WACCM' : [0.94, 1.25, 70],
#                     'GFDL-AM4' : [2.0, 2.5, 33],
#                     'GFDL-CM4' : [2.0, 2.5, 33],
#                     'SAM0-UNICON' : [0.94, 1.25, 30]    
#                    } # for filling in tables.
# stylelist = ['-', ':', '--']
# JRA_hybrid_level_A = np.array([0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 133.051011276943000000, 364.904148871589000000, 634.602716447362000000, 959.797167291774000000, 1347.680041655150000000, 1790.907395951100000000, 2294.841689948500000000, 2847.484777711760000000, 3468.871488118640000000, 4162.956462969160000000, 4891.880832504910000000, 5671.824239804080000000, 6476.712996385320000000, 7297.469894720490000000, 8122.159791249150000000, 8914.082201062340000000, 9656.181910501640000000, 10329.436177774600000000, 10912.638444238700000000, 11369.647830843200000000, 11695.371597470000000000, 11861.253087394800000000, 11855.434316349300000000, 11663.355365580300000000, 11285.404064494200000000, 10729.949405567900000000, 10014.615053510700000000, 9167.247035833100000000, 8226.244907704420000000, 7201.568980298280000000, 6088.673008533920000000, 4950.000000000000000000, 4000.000000000000000000, 3230.000000000000000000, 2610.000000000000000000, 2105.000000000000000000, 1700.000000000000000000, 1370.000000000000000000, 1105.000000000000000000, 893.000000000000000000, 720.000000000000000000, 581.000000000000000000, 469.000000000000000000, 377.000000000000000000, 301.000000000000000000, 237.000000000000000000, 182.000000000000000000, 136.000000000000000000, 97.000000000000000000, 65.000000000000000000, 39.000000000000000000, 20.000000000000000000, 0.000000000000000000])
# JRA_hybrid_level_B = np.array([1.000000000000000000, 0.997000000000000000, 0.994000000000000000, 0.989000000000000000, 0.982000000000000000, 0.972000000000000000, 0.960000000000000000, 0.946000000000000000, 0.926669489887231000, 0.904350958511284000, 0.879653972835526000, 0.851402028327082000, 0.819523199583449000, 0.785090926040489000, 0.748051583100515000, 0.709525152222882000, 0.668311285118814000, 0.624370435370308000, 0.580081191674951000, 0.534281757601959000, 0.488232870036147000, 0.442025301052795000, 0.395778402087509000, 0.350859177989377000, 0.307438180894984000, 0.265705638222254000, 0.225873615557613000, 0.189303521691568000, 0.155046284025300000, 0.124387469126052000, 0.096445656836507500, 0.072366446344196600, 0.052145959355057800, 0.035700505944321400, 0.022853849464893500, 0.013327529641668900, 0.006737550922955820, 0.002484310197017220, 0.000113269914660783, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000, 0.000000000000000000])
# plot_type='.png'
# plt.rcParams.update({'font.size': 8})
# my_dpi = 300
# amip_dict = {
#              'HadGEM3-GC31-LL' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/amip/r5i1p1f3/Amon/wap/gn/latest/wap_Amon_HadGEM3-GC31-LL_amip_r5i1p1f3_gn_197901-201412.nc',
#              'HadGEM3-GC31-MM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/amip/r1i1p1f3/Amon/wap/gn/latest/*.nc',
#              'BCC-CSM2-MR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/BCC/BCC-CSM2-MR/amip/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_BCC-CSM2-MR_amip_r1i1p1f1_gn_197901-201412.nc', # Can;t find areacella, so will need to try and code area at a later date
#              'BCC-ESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/BCC/BCC-ESM1/amip/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_BCC-ESM1_amip_r1i1p1f1_gn_197901-201412.nc', # Need to get areacella file
#              'CAMS-CSM1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CAMS/CAMS-CSM1-0/amip/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CAMS-CSM1-0_amip_r1i1p1f1_gn_197901-201412.nc', # No areacella file
#              'CanESM5' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CCCma/CanESM5/amip/r1i1p2f1/Amon/wap/gn/latest/wap*.nc', #No data but should exists according to website.
#              'FGOALS-f3-L' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CAS/FGOALS-f3-L/amip/r1i1p1f1/Amon/wap/gr/latest/wap_Amon_FGOALS-f3-L_amip_r1i1p1f1_gr_197901-201412.nc',# No areacella file
#              'CNRM-CM6-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/amip/r1i1p1f2/Amon/wap/gr/latest/wap_Amon_CNRM-CM6-1_amip_r1i1p1f2_gr*.nc',
#              'CNRM-EMS2-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/amip/r1i1p1f2/Amon/wap/gr/latest/wap_Amon_CNRM-ESM2-1_amip_r1i1p1f2_gr*.nc',
#              'IPSL-CM6A-LR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/amip/r1i1p1f1/Amon/wap/gr/latest/wap*.nc',
#              'MIROC6' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MIROC/MIROC6/amip/r1i1p1f1/Amon/wap/gn/latest/*.nc', # No areacella data # Need to fix code to get to work as wap is contained in multiple files, but rlut isn't.
#              'UKESM1-0-LL' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/amip/r1i1p1f4/Amon/wap/gn/latest/wap_Amon_UKESM1-0-LL_amip_r1i1p1f4_gn_197901-201412.nc',
#              'MRI-ESM2-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MRI/MRI-ESM2-0/amip/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_MRI-ESM2-0_amip_r1i1p1f1_gn_197901-201412.nc',
#              'GISS-E2-1-G' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/wap/gn/latest/*.nc',
#              'CESM2' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCAR/CESM2/amip/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CESM2_amip_r1i1p1f1_gn_195001-201412.nc',
#              'CESM2-WACCM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCAR/CESM2-WACCM/amip/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CESM2-WACCM_amip_r1i1p1f1_gn_195001-201412.nc',
#              'GFDL-AM4' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NOAA-GFDL/GFDL-AM4/amip/r1i1p1f1/Amon/wap/gr1/latest/wap_Amon_GFDL-AM4_amip_r1i1p1f1_gr1_198001-201412.nc',
#              'GFDL-CM4' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/amip/r1i1p1f1/Amon/wap/gr1/latest/*.nc',
#              'SAM0-UNICON' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/SNU/SAM0-UNICON/amip/r1i1p1f1/Amon/wap/gn/latest/*.nc',
#              'NorESM2-LM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCC/NorESM2-LM/amip/r1i1p2f1/Amon/wap/gn/latest/wap*.nc', 
#              'E3SM-1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/E3SM-Project/E3SM-1-0/amip/r2i1p1f1/Amon/wap/gr/latest/*.nc',# 
#              'TaiESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/AS-RCEC/TaiESM1/amip/r1i1p1f1/Amon/wap/gn/latest/wap_*.nc' 
#              }
# amip_p4k_dict = {
#                  'BCC-CSM2-MR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/BCC/BCC-CSM2-MR/amip-p4K/r1i1p1f1/Amon/wap/gn/latest/wap*.nc', # Can;t find areacella,  No data but should exists according to website.
#                  'CESM2': '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/NCAR/CESM2/amip-p4K/r1i1p1f1/Amon/wap/gn/latest/*.nc', 
#                  'CNRM-CM6-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/CNRM-CERFACS/CNRM-CM6-1/amip-p4K/r1i1p1f2/Amon/wap/gr/latest/wap*.nc',# No data but should exists according to website.
#                  'CanESM5' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/CCCma/CanESM5/amip-p4K/r1i1p2f1/Amon/wap/gn/latest/wap*.nc', #No data but should exists according to website.
#                  'E3SM-1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/E3SM-Project/E3SM-1-0/amip-p4K/r2i1p1f1/Amon/wap/gr/latest/*.nc',# 
#                  'GFDL-CM4' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/NOAA-GFDL/GFDL-CM4/amip-p4K/r1i1p1f1/Amon/wap/gr1/latest/wap_Amon_GFDL-CM4_amip-p4K_r1i1p1f1_gr1_197901-201412.nc', # Exists according to website - may have to download.
#                  'GISS-E2-1-G' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/NASA-GISS/GISS-E2-1-G/amip-p4K/r1i1p1f1/Amon/wap/gn/latest/wap*.nc',# Exists according to website - may have to download.
#                  'HadGEM3-GC31-LL' :'/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/MOHC/HadGEM3-GC31-LL/amip-p4K/r5i1p1f3/Amon/wap/gn/latest/wap_Amon_HadGEM3-GC31-LL_amip-p4K*.nc',
#                  'IPSL-CM6A-LR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/IPSL/IPSL-CM6A-LR/amip-p4K/r1i1p1f1/Amon/wap/gr/latest/wap_*.nc',
#                  'MIROC6' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/MIROC/MIROC6/amip-p4K/r1i1p1f1/Amon/wap/gn/latest/wap*.nc', # No data but should exists according to website.
#                  'MRI-ESM2-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/MRI/MRI-ESM2-0/amip-p4K/r1i1p1f1/Amon/wap/gn/latest/*.nc',
#                  'NorESM2-LM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/NCC/NorESM2-LM/amip-p4K/r1i1p2f1/Amon/wap/gn/latest/wap*.nc', 
#                  'TaiESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CFMIP/AS-RCEC/TaiESM1/amip-p4K/r1i1p1f1/Amon/wap/gn/latest/wap*.nc' # Exists according to website, but not on CEDA.
#                 }
# picontrol_dict = {
#                   'HadGEM3-GC31-LL' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Emon/wap/gn/latest/wap_Emon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn*.nc', # Can't get cf-python regridding to work on this dataset.
# #                  'HadGEM3-GC31-MM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/piControl/r1i1p1f1/Emon/wap/gn/latest/*.nc', # wap is available on model levels, but pressure on levels is not, so can't get 500 hPa vertical velocity
#                   'BCC-CSM2-MR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/BCC/BCC-CSM2-MR/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_BCC-CSM2-MR_piControl_r1i1p1f1_gn_*.nc', # Can;t find areacella, so will need to try and code area at a later date
#                   'BCC-ESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/BCC/BCC-ESM1/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_BCC-ESM1_piControl_r1i1p1f1_gn*.nc',# Need to get areacella file
#                   'CAMS-CSM1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CAMS/CAMS-CSM1-0/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CAMS-CSM1-0_piControl_r1i1p1f1_gn*.nc',# No areacella file
#                   'CanESM5' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CCCma/CanESM5/piControl/r1i1p2f1/Amon/wap/gn/latest/wap*.nc', #No data but should exists according to website.
#                   'FGOALS-f3-L' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CAS/FGOALS-f3-L/piControl/r1i1p1f1/Amon/wap/gr/latest/wap_Amon_FGOALS-f3-L_piControl_r1i1p1*.nc', # No areacella file # NB wap files are missing, but this helps find other files and code later points to personal copy of wap files
#                   'CNRM-CM6-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/piControl/r1i1p1f2/Amon/wap/gr/latest/wap_Amon_CNRM-CM6-1_piControl_r1i1p1f2_gr*',
#                   'CNRM-EMS2-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/piControl/r1i1p1f2/Amon/wap/gr/latest/wap_Amon_CNRM-ESM2-1_piControl_r1i1p1f2_gr*.nc',
#                   'IPSL-CM6A-LR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/piControl/r1i1p1f1/Amon/wap/gr/latest/wap_Amon_IPSL-CM6A-LR_piControl_r1i1p1f1_gr*.nc',
#                   'MIROC6' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MIROC/MIROC6/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_MIROC6_piControl_r1i1p1f1_gn*.nc', # No area cella data
#                   'UKESM1-0-LL' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/piControl/r1i1p1f2/Emon/wap/gn/latest/wap_Emon_UKESM1-0-LL_piControl_r1i1p1f2_gn*.nc',
#                   'MRI-ESM2-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MRI/MRI-ESM2-0/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_MRI-ESM2-0_piControl_r1i1p1f1_gn*.nc',
#                   'GISS-E2-1-G' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_GISS-E2-1-G_piControl_r1i1p1f1_gn*.nc',
#                   'CESM2' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCAR/CESM2/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CESM2_piControl_r1i1p1f1_gn*.nc',
#                   'CESM2-WACCM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCAR/CESM2-WACCM/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CESM2-WACCM_piControl_r1i1p1f1_gn*.nc',
#                   'GFDL-CM4' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/piControl/r1i1p1f1/Amon/wap/gr1/latest/wap_Amon_GFDL-CM4_piControl_r1i1p1f1_gr*.nc',
#                   'NorESM2-LM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCC/NorESM2-LM/piControl/r1i1p1f1/Amon/wap/gn/latest/wap*.nc', 
#                   'E3SM-1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/E3SM-Project/E3SM-1-0/piControl/r1i1p1f1/Amon/wap/gr/latest/*.nc', 
#                   'TaiESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/AS-RCEC/TaiESM1/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_*.nc', 
#                   'SAM0-UNICON' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/SNU/SAM0-UNICON/piControl/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_SAM0-UNICON_piControl_r1i1p1f1_gn*.nc' # wap missing, but point to this location for other variables and point to personal copy of wap files in function.
#                  }
# abrupt4co2_dict = {
#                    'HadGEM3-GC31-LL' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/abrupt-4xCO2/r1i1p1f3/Amon/wap/gn/latest/wap_Amon_HadGEM3-GC31-LL_abrupt-4xCO2_r1i1p1f3_*.nc',
#                    'HadGEM3-GC31-MM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/abrupt-4xCO2/r1i1p1f3/Amon/wap/gn/latest/*.nc',
#                    'BCC-CSM2-MR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/BCC/BCC-CSM2-MR/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_BCC-CSM2-MR_abrupt-4xCO2_r1i1p1f1_gn_*.nc',# Can;t find areacella, so will need to try and code area at a later date
#                    'BCC-ESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/BCC/BCC-ESM1/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_BCC-ESM1_abrupt-4xCO2_r1i1p1f1*.nc',# Need to get areacella file
#                    'CanESM5' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CCCma/CanESM5/abrupt-4xCO2/r1i1p2f1/Amon/wap/gn/latest/wap*.nc', #No data but should exists according to website.
#                    'CAMS-CSM1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CAMS/CAMS-CSM1-0/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CAMS-CSM1-0_abrupt-4xCO2_r1i1p1f1_gn*.nc', # No areacella file
# #                   'FGOALS-f3-L' : '', # wap missing
#                    'CNRM-CM6-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CNRM-CERFACS/CNRM-CM6-1/abrupt-4xCO2/r1i1p1f2/Amon/wap/gr/latest/wap_Amon_CNRM-CM6-1_abrupt-4xCO2_r1i1p1f2_gr*.nc',
#                    'CNRM-EMS2-1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/CNRM-CERFACS/CNRM-ESM2-1/abrupt-4xCO2/r1i1p1f2/Amon/wap/gr/latest/wap_Amon_CNRM-ESM2-1_abrupt-4xCO2_r1i1p1f2_gr*.nc',
#                    'E3SM-1-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/E3SM-Project/E3SM-1-0/abrupt-4xCO2/r1i1p1f1/Amon/wap/gr/latest/*.nc', 
#                    'IPSL-CM6A-LR' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/IPSL/IPSL-CM6A-LR/abrupt-4xCO2/r1i1p1f1/Amon/wap/gr/latest/wap_Amon_IPSL-CM6A-LR_abrupt-4xCO2_r1i1p1f1_gr*.nc',
#                    'MIROC6' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MIROC/MIROC6/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_MIROC6_abrupt-4xCO2_r1i1p1f1_gn*.nc', #  No areacella data.
#                    'UKESM1-0-LL' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/abrupt-4xCO2/r1i1p1f2/Amon/wap/gn/latest/wap_Amon_UKESM1-0-LL_abrupt-4xCO2_r1i1p1f2_gn*.nc',
#                    'MRI-ESM2-0' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MRI/MRI-ESM2-0/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_MRI-ESM2-0_abrupt-4xCO2_r1i1p1f1_gn*.nc',
#                    'GISS-E2-1-G' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_GISS-E2-1-G_abrupt-4xCO2_r1i1p1f1_gn*.nc',
# #                   'CESM2' : '', # WAP missing
#                    'CESM2-WACCM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCAR/CESM2-WACCM/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_CESM2-WACCM_abrupt-4xCO2_r1i1p1f1_gn*.nc',
#                    'GFDL-CM4' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NOAA-GFDL/GFDL-CM4/abrupt-4xCO2/r1i1p1f1/Amon/wap/gr1/latest/wap_Amon_GFDL-CM4_abrupt-4xCO2_r1i1p1f1_gr*.nc', # area weighting not work
#                    'NorESM2-LM' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/NCC/NorESM2-LM/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap*.nc', 
#                    'TaiESM1' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/AS-RCEC/TaiESM1/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_*.nc', 
#                    'SAM0-UNICON' : '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/SNU/SAM0-UNICON/abrupt-4xCO2/r1i1p1f1/Amon/wap/gn/latest/wap_Amon_SAM0-UNICON_abrupt-4xCO2_r1i1p1f1_gn*.nc'
#                    }


# def calc_jra55_plev(surf_pressure, model_levels):
#     '''
#     Calculates pressure on hybrid sigma-pressure levels

#     Use equations on page 16 and 17 of JRA55 handbook.
#     '''
#     surf_pressure = np.array(surf_pressure)
#     surf_pressure_shape = surf_pressure.shape
#     surf_pressure = surf_pressure.flatten()
#     model_layers = np.arange(model_levels[0]-1, model_levels[-1]+1)
#     n_levels  = model_levels.size
#     surf_pressure = np.repeat(surf_pressure.T,n_levels+1).reshape(surf_pressure.T.shape+(n_levels+1,)).T
#     p_layers = JRA_hybrid_level_A[model_layers][:,None] + (JRA_hybrid_level_B[model_layers][:,None] * surf_pressure)
# #    print('p_Layers=', p_layers)
#     one_over_delta_p = 1.0/(p_layers[:-1]-p_layers[1:])
#     p_levels = np.exp(one_over_delta_p*((p_layers[:-1]*np.log(p_layers[:-1])) -(p_layers[1:]*np.log(p_layers[1:])))-1)
#     p_levels = p_levels.reshape((n_levels,)+surf_pressure_shape)
#     return p_levels


def match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_SYN', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(2005, 2015)):
    '''
    spatial_av_scale is in degrees (i.e. default 1 corresponds to 1 degree)
    time_av_scale is hours, (but default 1 corresponds to instantaneous data)
    '''
    if int(lon_min) == lon_min: lon_min=int(lon_min)
    if int(lon_max) == lon_max: lon_max=int(lon_max)
    if int(lat_min) == lat_min: lat_min=int(lat_min)
    if int(lat_max) == lat_max: lat_max=int(lat_max)
    pkl_filename1 = '/home/users/phill/w500_cre_pkldir/w500_cre_dist_'+w500_source+'_'+rad_source+'_space_av'+str(int(spatial_av_scale))+'_time_av'+str(int(time_av_scale))+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_year'+str(yearlist[0])+'to'+str(yearlist[-1])+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'area_weighted.pbz2'
    print('pkl_filename1=', pkl_filename1)
    if isfile(pkl_filename1):
        print('Reading '+pkl_filename1)
        with bz2.BZ2File(pkl_filename1, 'rb') as fp:
            data = cPickle.load(fp)
    else:
        if w500_source == 'CombinedReanalyses':
            data = {}
            era5_data = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source=rad_source, w500_bins=w500_bins, cre_bins=cre_bins, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
            jra55_data = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source=rad_source, w500_bins=w500_bins, cre_bins=cre_bins, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
            merra2_data = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source=rad_source, w500_bins=w500_bins, cre_bins=cre_bins, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
            for k in era5_data.keys():
                data.update({k : {}})
                for k2 in ['w500_hist', 'w500_hist_lw', 'sw_clr_sum', 'sw_cre_sum', 'lw_clr_sum', 'lw_cre_sum', 'net_clr_sum', 'net_cre_sum', 'ratio_clr_sum', 'ratio_cre_sum', 'sw_clr2_sum', 'sw_cre2_sum', 'sw_clr_sum_sq', 'sw_cre_sum_sq', 'lw_clr_sum_sq', 'lw_cre_sum_sq', 'net_clr_sum_sq', 'net_cre_sum_sq', 'ratio_clr_sum_sq', 'ratio_cre_sum_sq', 'sw_clr2_sum_sq', 'sw_cre2_sum_sq', 'clfr_sum', 'clfr_sum_sq', 'high_clfr_sum', 'high_clfr_sum_sq', 'midhigh_clfr_sum', 'midhigh_clfr_sum_sq', 'midlow_clfr_sum', 'midlow_clfr_sum_sq', 'low_clfr_sum', 'low_clfr_sum_sq', 'clfr2_sum', 'clfr2_sum_sq', 'high_clfr2_sum', 'high_clfr2_sum_sq', 'midhigh_clfr2_sum', 'midhigh_clfr2_sum_sq', 'midlow_clfr2_sum', 'midlow_clfr2_sum_sq', 'low_clfr2_sum', 'low_clfr2_sum_sq', 'cod_sum', 'cod_sum_sq', 'high_cod_sum', 'high_cod_sum_sq', 'midhigh_cod_sum', 'midhigh_cod_sum_sq', 'midlow_cod_sum', 'midlow_cod_sum_sq', 'low_cod_sum', 'low_cod_sum_sq', 'cod2_sum', 'cod2_sum_sq', 'high_cod2_sum', 'high_cod2_sum_sq', 'midhigh_cod2_sum', 'midhigh_cod2_sum_sq', 'midlow_cod2_sum', 'midlow_cod2_sum_sq', 'low_cod2_sum', 'low_cod2_sum_sq', 'cprice_sum', 'cprice_sum_sq', 'high_cprice_sum', 'high_cprice_sum_sq', 'midhigh_cprice_sum', 'midhigh_cprice_sum_sq', 'midlow_cprice_sum', 'midlow_cprice_sum_sq', 'low_cprice_sum', 'low_cprice_sum_sq', 'cprice2_sum', 'cprice2_sum_sq', 'high_cprice2_sum', 'high_cprice2_sum_sq', 'midhigh_cprice2_sum', 'midhigh_cprice2_sum_sq', 'midlow_cprice2_sum', 'midlow_cprice2_sum_sq', 'low_cprice2_sum', 'low_cprice2_sum_sq', 'cprwat_sum', 'cprwat_sum_sq', 'high_cprwat_sum', 'high_cprwat_sum_sq', 'midhigh_cprwat_sum', 'midhigh_cprwat_sum_sq', 'midlow_cprwat_sum', 'midlow_cprwat_sum_sq', 'low_cprwat_sum', 'low_cprwat_sum_sq', 'cprwat2_sum', 'cprwat2_sum_sq', 'high_cprwat2_sum', 'high_cprwat2_sum_sq', 'midhigh_cprwat2_sum', 'midhigh_cprwat2_sum_sq', 'midlow_cprwat2_sum', 'midlow_cprwat2_sum_sq', 'low_cprwat2_sum', 'low_cprwat2_sum_sq', 'log_cod_sum', 'log_cod_sum_sq', 'log_high_cod_sum', 'log_high_cod_sum_sq', 'log_midhigh_cod_sum', 'log_midhigh_cod_sum_sq', 'log_midlow_cod_sum', 'log_midlow_cod_sum_sq', 'log_low_cod_sum', 'log_low_cod_sum_sq', 'log_cod2_sum', 'log_cod2_sum_sq', 'log_high_cod2_sum', 'log_high_cod2_sum_sq', 'log_midhigh_cod2_sum', 'log_midhigh_cod2_sum_sq', 'log_midlow_cod2_sum', 'log_midlow_cod2_sum_sq', 'log_low_cod2_sum', 'log_low_cod2_sum_sq', 'ice_clfr_sum', 'ice_clfr_sum_sq', 'ice_high_clfr_sum', 'ice_high_clfr_sum_sq', 'ice_midhigh_clfr_sum', 'ice_midhigh_clfr_sum_sq', 'ice_midlow_clfr_sum', 'ice_midlow_clfr_sum_sq', 'ice_low_clfr_sum', 'ice_low_clfr_sum_sq', 'ice_clfr2_sum', 'ice_clfr2_sum_sq', 'ice_high_clfr2_sum', 'ice_high_clfr2_sum_sq', 'ice_midhigh_clfr2_sum', 'ice_midhigh_clfr2_sum_sq', 'ice_midlow_clfr2_sum', 'ice_midlow_clfr2_sum_sq', 'ice_low_clfr2_sum', 'ice_low_clfr2_sum_sq', 'liq_clfr_sum', 'liq_clfr_sum_sq', 'liq_high_clfr_sum', 'liq_high_clfr_sum_sq', 'liq_midhigh_clfr_sum', 'liq_midhigh_clfr_sum_sq', 'liq_midlow_clfr_sum', 'liq_midlow_clfr_sum_sq', 'liq_low_clfr_sum', 'liq_low_clfr_sum_sq', 'liq_clfr2_sum', 'liq_clfr2_sum_sq', 'liq_high_clfr2_sum', 'liq_high_clfr2_sum_sq', 'liq_midhigh_clfr2_sum', 'liq_midhigh_clfr2_sum_sq', 'liq_midlow_clfr2_sum', 'liq_midlow_clfr2_sum_sq', 'liq_low_clfr2_sum', 'liq_low_clfr2_sum_sq', 'sw_cre_hist', 'lw_cre_hist', 'net_cre_hist', 'sw_cre_adj_sum', 'sw_clr_adj_sum', 'sw_cre_adj2_sum', 'lw_cre_adj_sum', 'lw_clr_adj_sum', 'lw_cre_adj2_sum', 'sw_cre_adj_sum_sq', 'sw_clr_adj_sum_sq', 'sw_cre_adj2_sum_sq', 'lw_cre_adj_sum_sq', 'lw_clr_adj_sum_sq', 'lw_cre_adj2_sum_sq', 'sw_cre_adj_hist', 'lw_cre_adj_hist', 'sw_cre_adj2_hist', 'lw_cre_adj2_hist']:
                    data[k].update({k2 : era5_data[k][k2]+merra2_data[k][k2]+jra55_data[k][k2]})
            data = calc_rad_stats(data)
        else:        
            if w500_source == 'ERA5': # ERA5 data is 0.25 degrees and hourly instantaneous, on the hour, lat lons are centres of gridpoints and are on .0, 0.25, etc, so this includes the points centred at 30N(S) which extend from 29.875N(S) to 30.125N(S). Longitudes go from -180 to 180 and latitudes go from 30 to -30
                w500_spatial_av_scale = int(spatial_av_scale * 4)
                w500_time_av_scale = time_av_scale
                w500_lat = np.arange(lat_min,lat_max+0.00001, 0.25)
            elif w500_source == 'MERRA2': # MERRA2 data is 0.5 degrees and hourly instantaneous. Regridded data has latitudes centred on 0.25 and 0.75 from 30 to -30 and longitudes going from 0 to 360.
                w500_spatial_av_scale = int(spatial_av_scale * 2)
                w500_time_av_scale = time_av_scale
                w500_lat = np.arange(lat_min+0.25, lat_max-0.2,0.5)
            elif w500_source == 'JRA55':# JRA55 data is 0.5 degrees. vertical velocities are 6-hourly instantaneous, rad fluxes are 3 hour averages from 0-3 and 3-6 hours into the forecast - we just use the 0-3 average to match to the vertical velocity. Regridded data has latitudes centred on 0.25 and 0.75 from 30 to -30 and longitudes going from 0 to 360.
                w500_spatial_av_scale = int(spatial_av_scale * 2)
                w500_lat = np.arange(lat_min+0.25, lat_max-0.2,0.5)
                if time_av_scale == 1:
                    w500_time_av_scale = time_av_scale
                else:
                    w500_time_av_scale = int(time_av_scale/6)
            else:
                print('*****************ERROR****************')
                print('Source for w500 not recognised')
                return
            if rad_source == 'ERA5': # ERA5 data is 0.25 degrees and hourly instantaneous
                rad_spatial_av_scale = spatial_av_scale * 4
                rad_time_av_scale = time_av_scale
                rad_lat = np.arange(lat_min,lat_max+0.00001, 0.25)
            elif rad_source == 'MERRA2': # MERRA2 data is 0.5 degrees and hourly instantaneous
                rad_spatial_av_scale = spatial_av_scale * 2
                rad_lat = np.arange(lat_min+0.25, lat_max-0.2,0.5)
                rad_time_av_scale = time_av_scale
            elif rad_source == 'JRA55':# JRA55 data is 0.5 degrees and 6-hourly instantaneous
                rad_spatial_av_scale = spatial_av_scale * 2
                rad_lat = np.arange(lat_min+0.25, lat_max-0.2,0.5)
                if time_av_scale == 1:
                    rad_time_av_scale = time_av_scale
                else:
                    rad_time_av_scale = int(time_av_scale/6)
            elif rad_source == 'CERES_SYN':# ceres-syn data is 1.0 degrees and hourly mean, lat goes from -30 to 30.
                rad_spatial_av_scale = spatial_av_scale
                rad_time_av_scale = time_av_scale
                rad_lat = np.arange(lat_min+0.5, lat_max-0.4,1)
            elif rad_source == 'CERES_EBAF':# ceres-ebaf data is 1.0 degrees and monthly mean, global
                if time_av_scale < 720:
                    print('*****************ERROR****************')
                    print('CERES-EBAF data is not available at this temporal resolution')
                    return
                rad_spatial_av_scale = spatial_av_scale
                rad_time_av_scale = int(time_av_scale / 720)
                rad_lat = np.arange(lat_min+0.5, lat_max-0.4,1)
            else:
                print('*****************ERROR****************')
                print('Source for rad data not recognised')
                return
            data = {'Ann' : {}, 'DJF' : {}, 'MAM' : {}, 'JJA' : {}, 'SON' : {}, 'Jan' : {}, 'Feb' : {}, 'Mar' : {}, 'Apr' : {}, 'May' : {}, 'Jun' : {}, 'Jul' : {}, 'Aug' : {}, 'Sep' : {}, 'Oct' : {}, 'Nov' : {}, 'Dec' : {}}
            for k1 in data.keys():
                for k2 in ['w500_hist', 'w500_hist_lw', 'sw_clr_sum', 'sw_cre_sum', 'lw_clr_sum', 'lw_cre_sum', 'net_clr_sum', 'net_cre_sum', 'ratio_clr_sum', 'ratio_cre_sum', 'sw_clr2_sum', 'sw_cre2_sum', 'sw_clr_sum_sq', 'sw_cre_sum_sq', 'lw_clr_sum_sq', 'lw_cre_sum_sq', 'net_clr_sum_sq', 'net_cre_sum_sq', 'ratio_clr_sum_sq', 'ratio_cre_sum_sq', 'sw_clr2_sum_sq', 'sw_cre2_sum_sq', 'clfr_sum', 'clfr_sum_sq', 'high_clfr_sum', 'high_clfr_sum_sq', 'midhigh_clfr_sum', 'midhigh_clfr_sum_sq', 'midlow_clfr_sum', 'midlow_clfr_sum_sq', 'low_clfr_sum', 'low_clfr_sum_sq', 'clfr2_sum', 'clfr2_sum_sq', 'high_clfr2_sum', 'high_clfr2_sum_sq', 'midhigh_clfr2_sum', 'midhigh_clfr2_sum_sq', 'midlow_clfr2_sum', 'midlow_clfr2_sum_sq', 'low_clfr2_sum', 'low_clfr2_sum_sq', 'cod_sum', 'cod_sum_sq', 'high_cod_sum', 'high_cod_sum_sq', 'midhigh_cod_sum', 'midhigh_cod_sum_sq', 'midlow_cod_sum', 'midlow_cod_sum_sq', 'low_cod_sum', 'low_cod_sum_sq', 'cod2_sum', 'cod2_sum_sq', 'high_cod2_sum', 'high_cod2_sum_sq', 'midhigh_cod2_sum', 'midhigh_cod2_sum_sq', 'midlow_cod2_sum', 'midlow_cod2_sum_sq', 'low_cod2_sum', 'low_cod2_sum_sq', 'cprice_sum', 'cprice_sum_sq', 'high_cprice_sum', 'high_cprice_sum_sq', 'midhigh_cprice_sum', 'midhigh_cprice_sum_sq', 'midlow_cprice_sum', 'midlow_cprice_sum_sq', 'low_cprice_sum', 'low_cprice_sum_sq', 'cprice2_sum', 'cprice2_sum_sq', 'high_cprice2_sum', 'high_cprice2_sum_sq', 'midhigh_cprice2_sum', 'midhigh_cprice2_sum_sq', 'midlow_cprice2_sum', 'midlow_cprice2_sum_sq', 'low_cprice2_sum', 'low_cprice2_sum_sq', 'cprwat_sum', 'cprwat_sum_sq', 'high_cprwat_sum', 'high_cprwat_sum_sq', 'midhigh_cprwat_sum', 'midhigh_cprwat_sum_sq', 'midlow_cprwat_sum', 'midlow_cprwat_sum_sq', 'low_cprwat_sum', 'low_cprwat_sum_sq', 'cprwat2_sum', 'cprwat2_sum_sq', 'high_cprwat2_sum', 'high_cprwat2_sum_sq', 'midhigh_cprwat2_sum', 'midhigh_cprwat2_sum_sq', 'midlow_cprwat2_sum', 'midlow_cprwat2_sum_sq', 'low_cprwat2_sum', 'low_cprwat2_sum_sq', 'log_cod_sum', 'log_cod_sum_sq', 'log_high_cod_sum', 'log_high_cod_sum_sq', 'log_midhigh_cod_sum', 'log_midhigh_cod_sum_sq', 'log_midlow_cod_sum', 'log_midlow_cod_sum_sq', 'log_low_cod_sum', 'log_low_cod_sum_sq', 'log_cod2_sum', 'log_cod2_sum_sq', 'log_high_cod2_sum', 'log_high_cod2_sum_sq', 'log_midhigh_cod2_sum', 'log_midhigh_cod2_sum_sq', 'log_midlow_cod2_sum', 'log_midlow_cod2_sum_sq', 'log_low_cod2_sum', 'log_low_cod2_sum_sq', 'ice_clfr_sum', 'ice_clfr_sum_sq', 'ice_high_clfr_sum', 'ice_high_clfr_sum_sq', 'ice_midhigh_clfr_sum', 'ice_midhigh_clfr_sum_sq', 'ice_midlow_clfr_sum', 'ice_midlow_clfr_sum_sq', 'ice_low_clfr_sum', 'ice_low_clfr_sum_sq', 'ice_clfr2_sum', 'ice_clfr2_sum_sq', 'ice_high_clfr2_sum', 'ice_high_clfr2_sum_sq', 'ice_midhigh_clfr2_sum', 'ice_midhigh_clfr2_sum_sq', 'ice_midlow_clfr2_sum', 'ice_midlow_clfr2_sum_sq', 'ice_low_clfr2_sum', 'ice_low_clfr2_sum_sq', 'liq_clfr_sum', 'liq_clfr_sum_sq', 'liq_high_clfr_sum', 'liq_high_clfr_sum_sq', 'liq_midhigh_clfr_sum', 'liq_midhigh_clfr_sum_sq', 'liq_midlow_clfr_sum', 'liq_midlow_clfr_sum_sq', 'liq_low_clfr_sum', 'liq_low_clfr_sum_sq', 'liq_clfr2_sum', 'liq_clfr2_sum_sq', 'liq_high_clfr2_sum', 'liq_high_clfr2_sum_sq', 'liq_midhigh_clfr2_sum', 'liq_midhigh_clfr2_sum_sq', 'liq_midlow_clfr2_sum', 'liq_midlow_clfr2_sum_sq', 'liq_low_clfr2_sum', 'liq_low_clfr2_sum_sq', 'sw_cre_adj_sum', 'sw_clr_adj_sum', 'sw_cre_adj2_sum', 'lw_cre_adj_sum', 'lw_clr_adj_sum', 'lw_cre_adj2_sum', 'sw_cre_adj_sum_sq', 'sw_clr_adj_sum_sq', 'sw_cre_adj2_sum_sq', 'lw_cre_adj_sum_sq', 'lw_clr_adj_sum_sq', 'lw_cre_adj2_sum_sq', 'sw_cre_adj_hist', 'lw_cre_adj_hist', 'sw_cre_adj2_hist', 'lw_cre_adj2_hist']: # NB sw_all_sum and lw_all_sum are zero because they can be calculated from sw_cre_sum and sw_clr_sum. Should delete sw_all_sum and lw_all_sum from the code really.
                    data[k1].update({k2:np.zeros(w500_bins.size-1)})
                for k2 in ['sw_cre_hist', 'lw_cre_hist', 'net_cre_hist', 'sw_cre_adj_hist', 'lw_cre_adj_hist', 'sw_cre_adj2_hist', 'lw_cre_adj2_hist']:
                    data[k1].update({k2:np.zeros((w500_bins.size-1, cre_bins.size-1)).astype('float32')})
            for year in yearlist: 
                print('yearlist=', yearlist)
                pkl_filename2 = '/home/users/phill/w500_cre_pkldir/w500_cre_dist_'+w500_source+'_'+rad_source+'_space_av'+str(int(spatial_av_scale))+'_time_av'+str(int(time_av_scale))+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_year'+str(year)+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_v2area_weighted.pbz2'
                print('pkl_filename2=', pkl_filename2)
                if isfile(pkl_filename2):
                    print('Reading '+pkl_filename2)
                    with bz2.BZ2File(pkl_filename2, 'rb') as fp:
                        incr_data = cPickle.load(fp)
                else:
                    w500, month_w500 = read_w500_data(w500_source, year,lon_max, lon_min, lat_max, lat_min)
                    print('w500.shape=', w500.shape)
                    rad_data, month_rad = read_rad_data(rad_source, year,lon_max, lon_min, lat_max, lat_min)
                    if (w500_source == 'JRA55') & (rad_source == 'CERES_SYN') & (time_av_scale == 1):
                        for kk in rad_data.keys():
                            rad_data[kk] = rad_data[kk][::6,:,:]
                        month_rad = month_rad[::6]
                    new_lat = np.arange(lat_min, lat_max, spatial_av_scale)+spatial_av_scale/2
                    incr_data = incr_match_omega500_rad_reanalyses_obs(w500,rad_data, w500_time_av_scale, w500_spatial_av_scale, rad_time_av_scale, rad_spatial_av_scale, w500_bins, cre_bins, month_rad, w500_lat=w500_lat, rad_lat=rad_lat, new_lat=new_lat)
                    with bz2.BZ2File(pkl_filename2.replace('_v2area_weighted.pkl','_v2area_weighted.pbz2'), 'w') as fp:   
                        cPickle.dump(incr_data, fp)                
                for k1 in incr_data.keys():
                    for k2 in incr_data[k1].keys():
                        data[k1][k2] += incr_data[k1][k2]
                        incr_data[k1][k2]=0
            data = calc_rad_stats(data)
            with bz2.BZ2File(pkl_filename1, 'w') as fp:   
                cPickle.dump(data, fp)                
    return data


def calc_rad_stats(data):
    '''
    Calculates mean and errors from existing data for toa sw and lw fluxes.
    '''
    for kk in data.keys():
        for mean_var in ['sw_clr_mean', 'sw_cre_mean', 'sw_clr_adj_mean', 'sw_cre_adj_mean', 'sw_cre_adj2_mean', 'lw_clr_mean', 'lw_cre_mean', 'lw_clr_adj_mean', 'lw_cre_adj_mean', 'lw_cre_adj2_mean', 'net_clr_mean', 'net_cre_mean', 'ratio_clr_mean', 'ratio_cre_mean', 'sw_clr2_mean', 'sw_cre2_mean']:
            data[kk][mean_var] =  data[kk][mean_var.replace('mean', 'sum')] / data[kk]['w500_hist']
        for rad_var in ['sw_cre', 'lw_cre', 'net_cre', 'ratio_cre', 'sw_cre2']:
            data[kk][rad_var+'_std'] = np.sqrt((data[kk][rad_var+'_sum_sq'] / data[kk]['w500_hist'])-(data[kk][rad_var+'_mean']**2))
            data[kk][rad_var+'_err'] = data[kk][rad_var+'_std'] / np.sqrt(data[kk]['w500_hist'])
    return data


def read_w500_data(w500_source, year,lon_max, lon_min, lat_max, lat_min, regrid=True, plev=500):
    if w500_source == 'ERA5':
        w500_filenames = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/ERA5/omega500/omega500_hourly_tropics_*.nc')
        ff = cf.read('/gws/nopw/j04/circulates_vol2/PHill/ERA5/omega500/omega500_hourly_tropics_2009.nc', select='lagrangian_tendency_of_air_pressure')[0]
        lon = ff.coord('long_name=longitude').array
        lon = np.roll(lon, int(lon.size/2))
        lon[lon < 0.0] += 360.
        lat = ff.coord('long_name=latitude').array
        ind_lon = np.where((lon <= lon_max) & (lon >= lon_min))[0]
        ind_lat = np.where((lat <= lat_max) & (lat >= lat_min))[0]
        w500_filenames = [f for f in w500_filenames if int(f[-7:-3]) == year]
        ff = cf.read(w500_filenames[0], select='lagrangian_tendency_of_air_pressure')[0]
        month = np.array([(datetime.datetime(1900,1,1,0,0,0)+datetime.timedelta(hours = int(h))).month for h in ff.coord('long_name=time').array])
        w500 = ff.array[:,ind_lat,:]*36*24 # Convert from Pa s-1 to hPa day$^{-1}$
        w500 = np.roll(w500, int(lon.size/2), axis=2)[:,:,ind_lon] # CHange from lon axis going from -180 to 180 to 0 to -180 (360) for consistency with CERES
    elif w500_source == 'MERRA2':
        filelist = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/MERRA2/OMEGA500_native/MERRA2_OMEGA500*.nc4')
        filelist = [f for f in filelist if f[-8:-4] == str(year)]
        ff = cf.read(filelist[0], select='omega_at_500_hPa')[0]
        lon = ff.coord('longitude').array
        lon = np.roll(lon, int(lon.size/2))
        lon[lon < 0.0] += 360.
        lat = ff.coord('latitude').array
        ind_lon = np.where((lon <= lon_max) & (lon >= lon_min))[0]
        ind_lat = np.where((lat <= lat_max) & (lat >= lat_min))[0]
        month = np.array([(datetime.datetime(year,1,1,0,30,0)+datetime.timedelta(minutes = int(m))).month for m in ff.coord('time').array])
        w500 = ff.array*36*24 # Convert from Pa s-1 to hPa day$^{-1}$
        w500 = (np.roll(w500, int(lon.size/2), axis=2))[:,ind_lat,:][:,:,ind_lon]
        if regrid:
            new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min+0.25, lon_max+0.01-0.25, 0.5), 'degreesE'))
            new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min+0.25, lat_max+0.01-0.25, 0.5), 'degreesN'))
            w500_regridded = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            w500 = w500_regridded[:,::-1,:]*36*24 # Convert from Pa s-1 to hPa day$^{-1}$
    elif w500_source == 'JRA55':
        filelist = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/vert_vel_native/anl_mdl_039_vvel_reg_tl319*.nc')
        print('filelist=', filelist)
        filelist = [f for f in filelist if int(f[-18:-14]) == year]
        print('filelist=', filelist)
        ff = cf.read(filelist[0], select='ncvar%VVEL_GDS4_HYBL')[0]
        ff2 = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/surf_press_native/anl_surf_001_pres_reg_tl319_'+str(year)+'.nc', select='ncvar%PRES_GDS4_SFC')[0]
        month = np.array([(datetime.datetime(1800,1,1,0,0,0)+datetime.timedelta(hours = int(h))).month for h in ff.coord('time').array])      
        levels = np.arange(16,35) # Hardwired as can't work out how to get this from file with cf-python.
        if regrid:
            new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min+0.25, lon_max+0.01-0.25, 0.5), 'degreesE'))
            new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min+0.25, lat_max+0.01-0.25, 0.5), 'degreesN'))
            w500_regridded = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            w500 = w500_regridded[:,:,::-1,:]*36*24 # Convert from Pa s-1 to hPa day$^{-1}$
            surf_pressure = ff2.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array[:,::-1,:]
        else:
            lon = ff.coord('longitude').array # Assume longitudes are gridbox centres as this seems to be the case for latitudes.
            lat = ff.coord('latitude').array # Latitudes seem to correspond to gridbox centres.
            ind_lon = np.where((lon <= lon_max) & (lon >= lon_min))[0]
            ind_lat = np.where((lat <= 30.) & (lat >= -30.))[0]
            ff = ff[:,:,ind_lat,:][:,:,:,ind_lon]
            w500 = ff.array*36*24 # Convert from Pa s-1 to hPa day$^{-1}$
            lon2 = ff2.coord('longitude').array # Assume longitudes are gridbox centres as this seems to be the case for latitudes.
            lat2 = ff2.coord('latitude').array # Latitudes seem to correspond to gridbox centres.
            ind_lon2 = np.where((lon2 <= lon_max) & (lon2 >= lon_min))[0]
            ind_lat2 = np.where((lat2 <= 30.) & (lat2 >= -30.))[0]
            surf_pressure = ff2.array[:,ind_lat2,:][:,:,ind_lon2]
        pressure = calc_jra55_plev(surf_pressure, levels)
#       Next two lines use level nearest to 500 hPa, probably should interpolate to 500 hPa instead, but that is difficult todo efficiently with pressure differing from gridbox to gridbox.
        ind_lev = np.argmin(abs(pressure.reshape(pressure.shape[0],pressure.shape[1]*pressure.shape[2]*pressure.shape[3])-(plev*100.)), axis=0)
        w500 = np.swapaxes(w500,0,1).reshape(pressure.shape[0],pressure.shape[1]*pressure.shape[2]*pressure.shape[3])[ind_lev,np.arange(pressure.shape[1]*pressure.shape[2]*pressure.shape[3])].reshape(pressure.shape[1],pressure.shape[2],pressure.shape[3])
    return w500, month


def read_rad_data(rad_source, year,lon_max, lon_min, lat_max, lat_min, regrid=True):
    rad_data = {}
    if rad_source == 'ERA5':
        olr_filename = '/gws/nopw/j04/circulates_vol2/PHill/ERA5/OLR/top_net_thermal_radiation_hourly_tropics_'+str(year)+'.nc'
        olr_clr_filename = '/gws/nopw/j04/circulates_vol2/PHill/ERA5/OLR/top_net_thermal_radiation_clear_sky_hourly_tropics_'+str(year)+'.nc'
        net_sw_filename = '/gws/nopw/j04/circulates_vol2/PHill/ERA5/OSR/top_net_solar_radiation_hourly_tropics_'+str(year)+'.nc'
        net_sw_clr_filename = '/gws/nopw/j04/circulates_vol2/PHill/ERA5/OSR/top_net_solar_radiation_clear_sky_hourly_tropics_'+str(year)+'.nc'
        sw_inc_filename = '/gws/nopw/j04/circulates_vol2/PHill/ERA5/OSR/toa_incident_solar_radiation_hourly_tropics_'+str(year)+'.nc'
        ff = cf.read(olr_filename, select='toa_outgoing_longwave_flux')[0]
        month = np.array([(datetime.datetime(1900,1,1,0,0,0)+datetime.timedelta(hours = int(h))).month for h in ff.coord('long_name=time').array])
        lat = ff.coord('long_name=latitude').array#  ERA5 lat lons are centres of gridpoints and are on .0, 0.25, etc, so this includes the points centred at 30N(S) whcih extend from 29.875N(S) to 30.125N(S). CERES-SYN lat
        ind = np.where((lat <= lat_max) & (lat >= lat_min))[0]
        lon = ff.coord('long_name=longitude').array
        lon = np.roll(lon, int(lon.size/2))
        lon[lon < 0.0] += 360. # Make ERA5 longitudes go from 0 - 360 instead of -180 to 180. Makes it easier to extract Pacific ocean
        ind_lon = np.where((lon <= lon_max) & (lon >= lon_min))[0]
        lw_all = -ff[:,ind,:].array/3600 # COnvert accumulated energy (J m-2) over one hour to flux (W m$^{-2}$)
        rad_data.update({'lw_all' : np.roll(lw_all, int(lon.size/2), axis=2)[:,:,ind_lon]}) # CHange from lon axis going from -180 to 180 to 0 to -180 (360) for consistency with CERES
        lw_clr = -cf.read(olr_clr_filename, select='long_name=Top net thermal radiation, clear sky')[0].array[:,ind,:]/3600 # COnvert accumulated energy (J m-2) over one hour to flux (W m$^{-2}$)
        rad_data.update({'lw_clr' : np.roll(lw_clr, int(lon.size/2), axis=2)[:,:,ind_lon]}) # 
        sw_all = (cf.read(sw_inc_filename, select='long_name=TOA incident solar radiation')[0].array[:,ind,:]-cf.read(net_sw_filename, select='toa_net_upward_shortwave_flux')[0].array[:,ind,:])/3600 # COnvert accumulated energy (J m-2) over one hour to flux (W m$^{-2}$)
        rad_data.update({'sw_all' : np.roll(sw_all, int(lon.size/2), axis=2)[:,:,ind_lon]}) # CHange from lon axis going from -180 to 180 to 0 to -180 (360) for consistency with CERES
        sw_clr = (cf.read(sw_inc_filename, select='long_name=TOA incident solar radiation')[0].array[:,ind,:]-cf.read(net_sw_clr_filename, select='long_name=Top net solar radiation, clear sky')[0].array[:,ind,:])/3600 # COnvert accumulated energy (J m-2) over one hour to flux (W m$^{-2}$)
        rad_data.update({'sw_clr' : np.roll(sw_clr, int(lon.size/2), axis=2)[:,:,ind_lon]})
        rad_data.update({'lw_clr_mask' : np.zeros(rad_data['lw_clr'].shape)})
    elif rad_source == 'MERRA2':
        sw_inc_filename = '/gws/nopw/j04/circulates_vol2/PHill/MERRA2/OSR_native/MERRA2_SWTDN_tavg1_2d_rad_Nx_'+str(year)+'.nc4'
        sw_net_filename = '/gws/nopw/j04/circulates_vol2/PHill/MERRA2/OSR_native/MERRA2_SWTNT_tavg1_2d_rad_Nx_'+str(year)+'.nc4'
        sw_net_clr_filename = '/gws/nopw/j04/circulates_vol2/PHill/MERRA2/OSR_clr_native/MERRA2_SWTNTCLR_tavg1_2d_rad_Nx_'+str(year)+'.nc4'
        lw_net_filename = '/gws/nopw/j04/circulates_vol2/PHill/MERRA2/OLR_native/MERRA2_OLR_tavg1_2d_rad_Nx_'+str(year)+'.nc4'
        lw_net_clr_filename = '/gws/nopw/j04/circulates_vol2/PHill/MERRA2/OLR_clr_native/MERRA2_OLR_clr_tavg1_2d_rad_Nx_'+str(year)+'.nc4'
        ff = cf.read(lw_net_filename, select='upwelling_longwave_flux_at_toa')[0]
        month = np.array([(datetime.datetime(year,1,1,0,30,0)+datetime.timedelta(minutes = int(m))).month for m in ff.coord('time').array])
        if regrid:
            new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min+0.25, lon_max+0.01-0.25, 0.5), 'degreesE'))
            new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min+0.25, lat_max+0.01-0.25, 0.5), 'degreesN'))
            lw_all = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            ff = cf.read(sw_inc_filename, select='toa_incoming_shortwave_flux')[0] - cf.read(sw_net_filename, select='toa_net_downward_shortwave_flux')[0]
            sw_all = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array               
            ff = cf.read(lw_net_clr_filename, select='upwelling_longwave_flux_at_toa_assuming_clear_sky')[0]
            lw_clr = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            ff = cf.read(sw_inc_filename, select='toa_incoming_shortwave_flux')[0]-cf.read(sw_net_clr_filename, select='toa_net_downward_shortwave_flux_assuming_clear_sky')[0]
            sw_clr = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array             
        else:
            lat = ff.coord('latitude').array
            lon = ff.coord('longitude').array
            lon = np.roll(lon, int(lon.size/2))
            lon[lon < 0.0] += 360. # Make MERRA2 longitudes go from 0 - 360 instead of -180 to 180. Makes it easier to extract Pacific ocean
#        n_time = ncfile.variables['time'][:].size
            ind_lon = np.where((lon <= lon_max) & (lon >= lon_min))[0]
            ind_lat = np.where((lat <= 30.) & (lat >= -30.))[0]
            lw_all = np.roll(ff.array, int(lon.size/2),axis=2)[:,ind_lat,:][:,:,ind_lon]
            lw_clr = np.roll(cf.read(lw_net_clr_filename, select='upwelling_longwave_flux_at_toa_assuming_clear_sky')[0].array, int(lon.size/2),axis=2)[:,ind_lat,:][:,:,ind_lon]
            sw_all = cf.read(sw_inc_filename, select='toa_incoming_shortwave_flux')[0].array - cf.read(sw_net_filename, select='toa_net_downward_shortwave_flux')[0].array 
            sw_all = np.roll(sw_all, int(lon.size/2),axis=2)[:,ind_lat,:][:,:,ind_lon]
            sw_clr =  cf.read(sw_inc_filename, select='toa_incoming_shortwave_flux')[0].array-cf.read(sw_net_clr_filename, select='toa_net_downward_shortwave_flux_assuming_clear_sky')[0].array 
            sw_clr = np.roll(sw_clr, int(lon.size/2),axis=2)[:,ind_lat,:][:,:,ind_lon]
        rad_data.update({'lw_all' : lw_all})
        rad_data.update({'sw_all' : sw_all})
        rad_data.update({'lw_clr' : lw_clr})
        rad_data.update({'sw_clr' : sw_clr})
        rad_data.update({'lw_clr_mask' : np.zeros(rad_data['lw_clr'].shape)})
    elif rad_source == 'JRA55':
        ff = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_ulwrf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Upward long wave radiation flux')[0]
        month = np.array([(datetime.datetime(1800,1,1,0,0,0)+datetime.timedelta(hours = int(h))).month for h in ff.coord('time').array])
        if regrid:
            new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min+0.25, lon_max+0.01-0.25, 0.5), 'degreesE'))
            new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min+0.25, lat_max+0.01-0.25, 0.5), 'degreesN'))
            lw_all = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            ff = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_uswrf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Upward solar radiation flux')[0]
            sw_all = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            ff = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_csulf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Clear sky upward long wave radiation flux')[0]
            lw_clr = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
            ff = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_csusf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Clear sky upward solar radiation flux')[0]
            sw_clr = ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array
        else:
            lon = ff.coord('longitude').array # Assume longitudes are gridbox centres as this seems to be the case for latitudes.
            lat =  ff.coord('latitude').array# Latitudes seem to correspond to gridbox centres.
            ind_lon = np.where((lon <= lon_max) & (lon >= lon_min))[0]
            ind_lat = np.where((lat <= 30.) & (lat >= -30.))[0]
            lw_all = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_ulwrf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Upward long wave radiation flux')[0].array[:,0,ind_lat,:][:,:,ind_lon] # 
            lw_clr = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_csulf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Clear sky upward long wave radiation flux')[0].array[:,0,ind_lat,:][:,:,ind_lon]
            sw_all = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_uswrf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Upward solar radiation flux')[0].array[:,0,ind_lat,:][:,:,ind_lon]
            sw_clr = cf.read('/gws/nopw/j04/circulates_vol2/PHill/JRA-55/toa_rad_native/fcst_phy2m_212_csusf_reg_tl319_'+str(year)+'_hill540426.nc', select='long_name=Clear sky upward solar radiation flux')[0].array[:,0,ind_lat,:][:,:,ind_lon]
        rad_data.update({'lw_all' : lw_all})
        rad_data.update({'sw_all' : sw_all})
        rad_data.update({'lw_clr' : lw_clr})
        rad_data.update({'sw_clr' : sw_clr})
        rad_data.update({'lw_clr_mask' : np.zeros(rad_data['lw_clr'].shape)})
    elif rad_source == 'CERES_SYN':
        filenames_osr = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CERES_SYN/OSR/OSR_CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Tropics_20*.nc')
        filenames_olr = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CERES_SYN/OLR/OLR_CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Tropics_20*.nc')
        filenames_clfr = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CERES_SYN/CLFR/clfr_CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Tropics_20*.nc')
        filenames_cod = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CERES_SYN/COD/COD_CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Tropics_20*.nc')
        filenames_cpr = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CERES_SYN/CPR/CPR_CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Tropics_20*.nc')
        filenames_phase = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CERES_SYN/PHASE/PHASE_CERES_SYN1deg-1H_Terra-Aqua-MODIS_Ed4.1_Tropics_20*.nc')
        filename_osr = [f for f in filenames_osr if int(f[-7:-3]) == year][0]
        filename_olr = [f for f in filenames_olr if int(f[-7:-3]) == year][0]
        filename_clfr = [f for f in filenames_clfr if int(f[-7:-3]) == year][0]
        filename_cod = [f for f in filenames_cod if int(f[-7:-3]) == year][0]
        filename_cpr = [f for f in filenames_cpr if int(f[-7:-3]) == year][0]
        filename_phase = [f for f in filenames_phase if int(f[-7:-3]) == year][0]
        ff_ceres_sw = cf.read(filename_osr, select='Adjusted All-Sky Profile Fluxes Shortwave Flux Up - TOA')[0]
        month = np.array([(datetime.datetime(2000,3,1,0,0,0)+datetime.timedelta(days = int(d))).month for d in ff_ceres_sw.coord('time').array])
        ind3 = np.where((ff_ceres_sw.coord('latitude').array <= lat_max) & (ff_ceres_sw.coord('latitude').array >= lat_min))[0]
        ind_lon_ceres = np.where((ff_ceres_sw.coord('longitude')[:] <= lon_max) & (ff_ceres_sw.coord('longitude').array >= lon_min))[0]
        print('ind_lon_ceres=', ind_lon_ceres)
        rad_data.update({'sw_clr' : cf.read(filename_osr, select='Observed TOA Shortwave Flux - Clear-sky')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]}) # FLip latitude axis for consistency with reanalyses
        rad_data.update({'sw_all' : cf.read(filename_osr, select='Observed TOA Shortwave Flux - All-sky')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'sw_clr_adj' : cf.read(filename_osr, select='Adjusted Clear-Sky Profile Fluxes Shortwave Flux Up - TOA')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]}) # FLip latitude axis for consistency with reanalyses
        rad_data.update({'sw_all_adj' : cf.read(filename_osr, select='Adjusted All-Sky Profile Fluxes Shortwave Flux Up - TOA')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'lw_clr_mask' : cf.read(filename_olr, select='Observed TOA Longwave Flux - Clear-sky')[0].array.mask.astype(float)[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        lw_clr = cf.read(filename_olr, select='Observed TOA Longwave Flux - Clear-sky')[0].array.data[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]
        lw_clr[lw_clr < 0.] = 0.
        rad_data.update({'lw_clr' : lw_clr})
        rad_data.update({'lw_all' : cf.read(filename_olr, select='Observed TOA Longwave Flux - All-sky')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'lw_clr_adj' : cf.read(filename_olr, select='Adjusted Clear-Sky Profile Fluxes Longwave Flux Up - TOA')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'lw_all_adj' : cf.read(filename_olr, select='Adjusted All-Sky Profile Fluxes Longwave Flux Up - TOA')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Total clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'high_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'midhigh_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Mid-High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'midlow_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Mid-Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'low_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        tot_phase = cf.read(filename_phase, select='Cloud Particle Phase - Total clouds')[0]
        tot_phase.override_units('km', inplace=True)
        tot_phase = tot_phase.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:].data
        high_phase = cf.read(filename_phase, select='Cloud Particle Phase - High clouds')[0]
        high_phase.override_units('km', inplace=True)
        high_phase = high_phase.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:].data
        mid_high_phase = cf.read(filename_phase, select='Cloud Particle Phase - Mid-High clouds')[0]
        mid_high_phase.override_units('km', inplace=True)
        mid_high_phase = mid_high_phase.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:].data
        mid_low_phase = cf.read(filename_phase, select='Cloud Particle Phase - Mid-Low clouds')[0]
        mid_low_phase.override_units('km', inplace=True)
        mid_low_phase = mid_low_phase.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:].data
        low_phase = cf.read(filename_phase, select='Cloud Particle Phase - Low clouds')[0]
        low_phase.override_units('km', inplace=True)
        low_phase = low_phase.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:].data
        rad_data.update({'ice_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Total clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (tot_phase - 1.0)})
        rad_data.update({'ice_high_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (high_phase - 1.0)})
        rad_data.update({'ice_midhigh_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Mid-High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (mid_high_phase - 1.0)})
        rad_data.update({'ice_midlow_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Mid-Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (mid_low_phase - 1.0)})
        rad_data.update({'ice_low_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (low_phase - 1.0)})
        rad_data.update({'liq_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Total clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (2.0 - tot_phase)})
        rad_data.update({'liq_high_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (2.0 - high_phase)})
        rad_data.update({'liq_midhigh_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Mid-High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (2.0 - mid_high_phase)})
        rad_data.update({'liq_midlow_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Mid-Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (2.0 - mid_low_phase)})
        rad_data.update({'liq_low_clfr' : cf.read(filename_clfr, select='Cloud Area Fraction - Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:] * (2.0 - low_phase)})
        tot_cod = cf.read(filename_cod, select='Cloud Visible Optical Depth - Total clouds')[0]
        tot_cod.override_units('km', inplace=True)
        tot_cod = tot_cod.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]
        high_cod = cf.read(filename_cod, select='Cloud Visible Optical Depth - High clouds')[0]
        high_cod.override_units('km', inplace=True)
        high_cod = high_cod.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]
        mid_high_cod = cf.read(filename_cod, select='Cloud Visible Optical Depth - Mid-High clouds')[0]
        mid_high_cod.override_units('km', inplace=True)
        mid_high_cod = mid_high_cod.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]
        mid_low_cod = cf.read(filename_cod, select='Cloud Visible Optical Depth - Mid-Low clouds')[0]
        mid_low_cod.override_units('km', inplace=True)
        mid_low_cod = mid_low_cod.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]
        low_cod = cf.read(filename_cod, select='Cloud Visible Optical Depth - Low clouds')[0]
        low_cod.override_units('km', inplace=True)
        low_cod = low_cod.array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]
        rad_data.update({'cod' : tot_cod})
        rad_data.update({'high_cod' : high_cod})
        rad_data.update({'midhigh_cod' : mid_high_cod})
        rad_data.update({'midlow_cod' : mid_low_cod})
        rad_data.update({'low_cod' : low_cod})
        rad_data.update({'cprwat' : cf.read(filename_cpr, select='Water Particle Radius - Total clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'high_cprwat' : cf.read(filename_cpr, select='Water Particle Radius - High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'midhigh_cprwat' : cf.read(filename_cpr, select='Water Particle Radius - Mid-High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'midlow_cprwat' : cf.read(filename_cpr, select='Water Particle Radius - Mid-Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'low_cprwat' : cf.read(filename_cpr, select='Water Particle Radius - Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'cprice' : cf.read(filename_cpr, select='Ice Particle Radius - Total clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'high_cprice' : cf.read(filename_cpr, select='Ice Particle Radius - High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'midhigh_cprice' : cf.read(filename_cpr, select='Ice Particle Radius - Mid-High clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'midlow_cprice' : cf.read(filename_cpr, select='Ice Particle Radius - Mid-Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'low_cprice' : cf.read(filename_cpr, select='Ice Particle Radius - Low clouds')[0].array[:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
    elif rad_source == 'CERES_EBAF':
        filename = '/gws/nopw/j04/circulates_vol2/PHill/CERES_EBAF_Ed4.1_Subset_200101-202012.nc'
        ff = cf.read(filename, select='Cloud Area Fraction - Daytime-and-Nighttime')[0]
        ceres_year = np.array([(datetime.datetime(2000,3,1,0,0,0)+datetime.timedelta(days = int(d))).year for d in ff.coord('long_name=time').array])
        time_ind = np.where(ceres_year == year)[0]
        print('year, time_ind=', year, time_ind)
        month = np.array([(datetime.datetime(2000,3,1,0,0,0)+datetime.timedelta(days = int(d))).month for d in ff.coord('long_name=time').array])
        month = month[time_ind]
        ind3 = np.where((ff.coord('latitude').array <= lat_max) & (ff.coord('latitude').array >= lat_min))[0]
        ind_lon_ceres = np.where((ff.coord('longitude').array <= lon_max) & (ff.coord('longitude').array >= lon_min))[0]
        rad_data.update({'sw_clr' : cf.read(filename, select='TOA Shortwave Flux - Clear-Sky (for cloud-free areas of region)')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]}) # FLip latitude axis for consistency with reanalyses
        rad_data.update({'sw_all' : cf.read(filename, select='TOA Shortwave Flux - All-Sky')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'sw_clr_adj' : cf.read(filename, select='TOA Shortwave Flux - Clear-Sky (for total region)')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]}) # FLip latitude axis for consistency with reanalyses
        rad_data.update({'sw_all_adj' : np.zeros(1)-9999})
        rad_data.update({'lw_clr_mask' : np.zeros(rad_data['sw_all'].shape)})
        rad_data.update({'lw_clr' : cf.read(filename, select='TOA Longwave Flux - Clear-Sky (for cloud-free areas of region)')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'lw_all' : cf.read(filename, select='TOA Longwave Flux - All-Sky')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'lw_clr_adj' : cf.read(filename, select='TOA Longwave Flux - Clear-Sky (for total region)')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        rad_data.update({'lw_all_adj' : np.zeros(1)-9999})
        rad_data.update({'clfr' : cf.read(filename, select='Cloud Area Fraction - Daytime-and-Nighttime')[0].array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        cod = cf.read(filename, select='Cloud Visible Optical Depth - Daytime')[0]
        cod.override_units('km', inplace=True)
        rad_data.update({'cod' : cod.array[time_ind,:,:][:,ind3,:][:,:,ind_lon_ceres][:,::-1,:]})
        for k in ['high_clfr', 'midhigh_clfr', 'midlow_clfr', 'low_clfr', 'ice_clfr', 'ice_high_clfr', 'ice_midhigh_clfr', 'ice_midlow_clfr', 'ice_low_clfr', 'liq_clfr', 'liq_high_clfr', 'liq_midhigh_clfr', 'liq_midlow_clfr', 'liq_low_clfr', 'high_cod', 'midhigh_cod', 'high_clfr', 'midhigh_clfr', 'midlow_clfr', 'low_clfr', 'ice_clfr', 'ice_high_clfr', 'ice_midhigh_clfr', 'ice_midlow_clfr', 'ice_low_clfr', 'liq_clfr', 'liq_high_clfr', 'liq_midhigh_clfr', 'liq_midlow_clfr', 'liq_low_clfr', 'high_cod', 'midhigh_cod', 'midlow_cod', 'low_cod', 'cprwat', 'high_cprwat', 'midhigh_cprwat', 'midlow_cprwat', 'low_cprwat', 'cprice', 'high_cprice', 'midhigh_cprice', 'midlow_cprice', 'low_cprice']:
            rad_data.update({k : np.zeros(1)-9999})
    return rad_data, month
    


def incr_match_omega500_rad_reanalyses_obs(w500,rad_data, w500_time_av_scale, w500_spatial_av_scale, rad_time_av_scale, rad_spatial_av_scale, w500_bins, cre_bins, month, w500_lat=np.arange(-30,30.01, 0.25), rad_lat=np.arange(-29.5,29.6,1), new_lat=np.arange(-30, 30)+0.5):
    month = month[int(rad_time_av_scale/2)::rad_time_av_scale]
    n_lat = w500.shape[1]
    n_lon = w500.shape[2]
    area_weights = np.cos(np.pi*w500_lat/180)
    if w500_lat.min() == -30: # centred on edges of domain, so use half of edge gridboxes.
        area_weights_smooth = 0.5*(uniform_filter(area_weights, w500_spatial_av_scale+1)+uniform_filter(area_weights, w500_spatial_av_scale-1))[int(w500_spatial_av_scale/2):1+n_lat-int(w500_spatial_av_scale/2):int(w500_spatial_av_scale)]
        print('w500.shape=', w500.shape)
        print('area_weights.shape=', area_weights.shape)
        w500 = 0.5*(uniform_filter(w500*area_weights[None,:,None], (w500_time_av_scale,w500_spatial_av_scale+1,w500_spatial_av_scale+1), mode='wrap')+uniform_filter(w500*area_weights[None,:,None], (w500_time_av_scale,w500_spatial_av_scale-1, w500_spatial_av_scale-1), mode='wrap'))[int(w500_time_av_scale/2)::w500_time_av_scale,int(w500_spatial_av_scale/2):1+n_lat-int(w500_spatial_av_scale/2):int(w500_spatial_av_scale),int(w500_spatial_av_scale/2):1+n_lon-int(w500_spatial_av_scale/2):int(w500_spatial_av_scale)]#  average w500 to CERES-SYN spatial scale.
    else:
        area_weights_smooth = (uniform_filter(area_weights, w500_spatial_av_scale))[int(w500_spatial_av_scale/2):1+n_lat-int(w500_spatial_av_scale/2):int(w500_spatial_av_scale)]
        w500 = uniform_filter(w500*area_weights[None,:,None], (w500_time_av_scale,w500_spatial_av_scale+1,w500_spatial_av_scale+1), mode='wrap')[int(w500_time_av_scale/2)::w500_time_av_scale,int(w500_spatial_av_scale/2):1+n_lat-int(w500_spatial_av_scale/2):int(w500_spatial_av_scale),int(w500_spatial_av_scale/2):1+n_lon-int(w500_spatial_av_scale/2):int(w500_spatial_av_scale)]#  average w500 to CERES-SYN spatial scale.
    w500 = w500 / area_weights_smooth[None,:,None]
    print('After averaging, w500.shape=', w500.shape)
#       ERA5 data is instantaneous on the hour, CERES-SYN is on the half hour, an (I think) it's an average over that hour.
#        sw_clr, sw_all, lw_clr, lw_all = ([] for __ in range(4))
#   Add logs of cods, as apparently should take logarithm of these before averaging
    if 'clfr' in rad_data.keys():
        rad_data.update({'log_cod' : np.log(rad_data['cod'])})
        rad_data.update({'log_high_cod' : np.log(rad_data['high_cod'])})
        rad_data.update({'log_midhigh_cod' : np.log(rad_data['midhigh_cod'])})
        rad_data.update({'log_midlow_cod' : np.log(rad_data['midlow_cod'])})
        rad_data.update({'log_low_cod' : np.log(rad_data['low_cod'])})
        cld_weights_dict={'cod' : 'clfr',
                          'high_cod' : 'high_clfr',
                          'midhigh_cod' : 'midhigh_clfr',
                          'midlow_cod' : 'midlow_clfr',
                          'low_cod' : 'low_clfr',
                          'log_cod' : 'clfr',
                          'log_high_cod' : 'high_clfr',
                          'log_midhigh_cod' : 'midhigh_clfr',
                          'log_midlow_cod' : 'midlow_clfr',
                          'log_low_cod' : 'low_clfr',
                          'cprice' : 'ice_clfr',
                          'high_cprice' : 'ice_high_clfr',
                          'midhigh_cprice' : 'ice_midhigh_clfr',
                          'midlow_cprice' : 'ice_midlow_clfr',
                          'low_cprice' : 'ice_low_clfr',
                          'cprwat' : 'liq_clfr',
                          'high_cprwat' : 'liq_high_clfr',
                          'midhigh_cprwat' : 'liq_midhigh_clfr',
                          'midlow_cprwat' : 'liq_midlow_clfr',
                          'low_cprwat' : 'liq_low_clfr'
                         }
    n_lat = rad_data['lw_clr'].shape[1]
    n_lon = rad_data['lw_clr'].shape[2]
    area_weights = np.cos(np.pi*rad_lat/180)
    av_area_weights =(uniform_filter(area_weights, rad_spatial_av_scale))[int(rad_spatial_av_scale/2):1+n_lat-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale)]
    for kk in ['cod', 'high_cod', 'midhigh_cod', 'midlow_cod', 'low_cod', 'cprice', 'high_cprice', 'midhigh_cprice', 'midlow_cprice', 'low_cprice', 'cprwat', 'high_cprwat', 'midhigh_cprwat', 'midlow_cprwat', 'low_cprwat', 'log_cod', 'log_high_cod', 'log_midhigh_cod', 'log_midlow_cod', 'log_low_cod']: # These should be weighted by clfr
        if kk in rad_data.keys():
            print('kk=', kk)
            print('np.max(rad_data[kk])=', np.max(rad_data[kk]))
            if ((np.max(rad_data[kk]) != -9999) & (np.max(rad_data[kk]) == np.max(rad_data[kk]))):
                weights = rad_data[cld_weights_dict[kk]]*area_weights[None,:,None]
                rad_data[kk] = uniform_filter(rad_data[kk].data*weights,(rad_time_av_scale, rad_spatial_av_scale, rad_spatial_av_scale), mode='wrap')[int(rad_time_av_scale/2)::rad_time_av_scale,int(rad_spatial_av_scale/2):1+n_lat-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale),int(rad_spatial_av_scale/2):1+n_lon-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale)]
                av_weights = uniform_filter(weights,(rad_time_av_scale, rad_spatial_av_scale, rad_spatial_av_scale), mode='wrap')[int(rad_time_av_scale/2)::rad_time_av_scale,int(rad_spatial_av_scale/2):1+n_lat-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale),int(rad_spatial_av_scale/2):1+n_lon-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale)]
                rad_data[kk] = rad_data[kk] / av_weights
    for kk in ['lw_clr_mask', 'lw_clr', 'lw_all', 'lw_clr_adj', 'lw_all_adj', 'sw_clr', 'sw_all', 'sw_clr_adj', 'sw_all_adj', 'clfr', 'high_clfr', 'midhigh_clfr', 'midlow_clfr', 'low_clfr', 'ice_clfr', 'ice_high_clfr', 'ice_midhigh_clfr', 'ice_midlow_clfr', 'ice_low_clfr', 'liq_clfr', 'liq_high_clfr', 'liq_midhigh_clfr', 'liq_midlow_clfr', 'liq_low_clfr']:
        if kk in rad_data.keys():
            if ((np.max(rad_data[kk]) != -9999) & (np.max(rad_data[kk]) == np.max(rad_data[kk]))):
                rad_data[kk] = uniform_filter(rad_data[kk],(rad_time_av_scale, rad_spatial_av_scale, rad_spatial_av_scale), mode='wrap')[int(rad_time_av_scale/2)::rad_time_av_scale,int(rad_spatial_av_scale/2):1+n_lat-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale),int(rad_spatial_av_scale/2):1+n_lon-int(rad_spatial_av_scale/2):int(rad_spatial_av_scale)]
                rad_data[kk] = rad_data[kk] / av_area_weights[None,:,None]
    print("After averagomg, rad_data['lw_clr'].shape=",rad_data['lw_clr'].shape) 
    rad_data['lw_clr'] = rad_data['lw_clr'] / (1.0-rad_data['lw_clr_mask'])
    rad_data['lw_clr'][rad_data['lw_clr_mask'] > 0.25] = -999 # if more than 25% of data are missing than treat average as missing
    rad_data['sw_cre'] = rad_data['sw_clr'] - rad_data['sw_all']
    rad_data['sw_cre_adj'] = rad_data['sw_clr_adj'] - rad_data['sw_all_adj']
    rad_data['sw_cre_adj2'] = rad_data['sw_clr_adj'] - rad_data['sw_all']
    rad_data['lw_cre'] = rad_data['lw_clr'] - rad_data['lw_all']
    rad_data['lw_cre_adj'] = rad_data['lw_clr_adj'] - rad_data['lw_all_adj']
    rad_data['lw_cre_adj2'] = rad_data['lw_clr_adj'] - rad_data['lw_all']
    rad_data['net_clr'] = rad_data['sw_clr']+rad_data['lw_clr']
    rad_data['net_cre'] = rad_data['sw_cre']+rad_data['lw_cre']
    rad_data['ratio_clr'] = -rad_data['sw_clr']/rad_data['lw_clr']
    rad_data['ratio_cre'] = -(rad_data['sw_clr']-rad_data['sw_all'])/(rad_data['lw_clr'] - rad_data['lw_all'])
    time_ind = {'Ann' : np.where(month == month)[0],
                'DJF' : np.where((month % 12 //3 +1) == 1)[0],
                'MAM' : np.where((month % 12 //3 +1) == 2)[0],
                'JJA' : np.where((month % 12 //3 +1) == 3)[0], 
                'SON' : np.where((month % 12 //3 +1) == 4)[0],
                'Jan' : np.where(month == 1)[0],
                'Feb' : np.where(month == 2)[0],
                'Mar' : np.where(month == 3)[0],
                'Apr' : np.where(month == 4)[0],
                'May' : np.where(month == 5)[0],
                'Jun' : np.where(month == 6)[0],
                'Jul' : np.where(month == 7)[0],
                'Aug' : np.where(month == 8)[0],
                'Sep' : np.where(month == 9)[0],
                'Oct' : np.where(month == 10)[0],
                'Nov' : np.where(month == 11)[0],
                'Dec' : np.where(month == 12)[0]}
    data_incr = {'Ann' : {}, 'DJF' : {}, 'MAM' : {}, 'JJA' : {}, 'SON' : {}, 'Jan' : {}, 'Feb' : {}, 'Mar' : {}, 'Apr' : {}, 'May' : {}, 'Jun' : {}, 'Jul' : {}, 'Aug' : {}, 'Sep' : {}, 'Oct' : {}, 'Nov' : {}, 'Dec' : {}}
    area_weights_2d = np.repeat(np.cos(np.pi*new_lat/180)[:,None],w500.shape[2], axis=1)
    area_weights_2d = area_weights_2d/area_weights_2d.sum()
    for k1 in data_incr.keys():
        area_weights = np.repeat(area_weights_2d[None,:,:], time_ind[k1].size, axis=0)
        data_incr[k1].update({'w500_hist' : np.histogram(w500[time_ind[k1],:,:].flatten(), bins=w500_bins, weights=area_weights.flatten())[0]})
        data_incr[k1].update({'w500_hist_lw' : np.histogram(w500[time_ind[k1],:,:][rad_data['lw_clr'][time_ind[k1],:,:] >= 0.], bins=w500_bins, weights=area_weights[rad_data['lw_clr'][time_ind[k1],:,:] >= 0.].flatten())[0]})
        for k2 in ['lw_clr', 'lw_cre', 'net_clr', 'net_cre', 'ratio_clr', 'ratio_cre']:
            data_incr[k1].update({k2+'_sum' : np.histogram(w500[time_ind[k1],:,:][rad_data['lw_clr'][time_ind[k1],:,:] >= 0.].flatten(), bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights)[rad_data['lw_clr'][time_ind[k1],:,:] >= 0.].flatten())[0]})
            data_incr[k1].update({k2+'_sum_sq' : np.histogram(w500[time_ind[k1],:,:][rad_data['lw_clr'][time_ind[k1],:,:] >= 0.].flatten(), bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights)[rad_data['lw_clr'][time_ind[k1],:,:] >= 0.].flatten()**2)[0]})
        for k2 in ['sw_clr', 'sw_cre', 'clfr', 'high_clfr', 'midhigh_clfr', 'midlow_clfr', 'low_clfr', 'ice_clfr', 'ice_high_clfr', 'ice_midhigh_clfr', 'ice_midlow_clfr', 'ice_low_clfr', 'liq_clfr', 'liq_high_clfr', 'liq_midhigh_clfr', 'liq_midlow_clfr', 'liq_low_clfr']:
            if k2 in rad_data.keys():
                if rad_data[k2].size > 1:
                    data_incr[k1].update({k2+'_sum' : np.histogram(w500[time_ind[k1],:,:].flatten(), bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights).flatten())[0]})
                    data_incr[k1].update({k2+'_sum_sq' : np.histogram(w500[time_ind[k1],:,:].flatten(), bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights).flatten()**2)[0]})
                    data_incr[k1].update({k2+'2_sum'  : np.histogram(w500[time_ind[k1],:,:][rad_data['lw_clr'][time_ind[k1],:,:] >= 0.], bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights)[rad_data['lw_clr'][time_ind[k1],:,:] >= 0.])[0]})
                    data_incr[k1].update({k2+'2_sum_sq' : np.histogram(w500[time_ind[k1],:,:][rad_data['lw_clr'][time_ind[k1],:,:] >= 0.], bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights)[rad_data['lw_clr'][time_ind[k1],:,:] >= 0.]**2)[0]})
                else:
                    data_incr[k1].update({k2+'_sum' : np.zeros(1)-9999})
                    data_incr[k1].update({k2+'_sum_sq' : np.zeros(1)-9999})
                    data_incr[k1].update({k2+'2_sum'  : np.zeros(1)-9999})
                    data_incr[k1].update({k2+'2_sum_sq' : np.zeros(1)-9999})
        for k2 in ['sw_cre_adj', 'sw_cre_adj2', 'sw_clr_adj', 'lw_clr_adj', 'lw_cre_adj', 'lw_cre_adj2']:
            if k2 in rad_data.keys():
                data_incr[k1].update({k2+'_sum' : np.histogram(w500[time_ind[k1],:,:].flatten(), bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights).flatten())[0]})
                data_incr[k1].update({k2+'_sum_sq' : np.histogram(w500[time_ind[k1],:,:].flatten(), bins=w500_bins, weights=(rad_data[k2][time_ind[k1],:,:]*area_weights).flatten()**2)[0]})
        for k2 in ['cod', 'high_cod', 'midhigh_cod', 'midlow_cod', 'low_cod', 'cprice', 'high_cprice', 'midhigh_cprice', 'midlow_cprice', 'low_cprice', 'cprwat', 'high_cprwat', 'midhigh_cprwat', 'midlow_cprwat', 'low_cprwat', 'log_cod', 'log_high_cod', 'log_midhigh_cod', 'log_midlow_cod', 'log_low_cod']:
            if k2 in rad_data.keys():
                if rad_data[k2].size > 1:
                    clfr_weights = rad_data[cld_weights_dict[k2]]
                    data_incr[k1].update({k2+'_sum' : np.histogram(w500[time_ind[k1],:,:][np.isfinite(rad_data[k2][time_ind[k1],:,:])], bins=w500_bins, weights=((rad_data[k2]*clfr_weights)[time_ind[k1],:,:]*area_weights)[np.isfinite(rad_data[k2][time_ind[k1],:,:])])[0]})
                    data_incr[k1].update({k2+'_sum_sq' : np.histogram(w500[time_ind[k1],:,:][np.isfinite(rad_data[k2][time_ind[k1],:,:])], bins=w500_bins, weights=((rad_data[k2]*clfr_weights)[time_ind[k1],:,:]*area_weights)[np.isfinite(rad_data[k2][time_ind[k1],:,:])]**2)[0]})
                    data_incr[k1].update({k2+'2_sum'  : np.histogram(w500[time_ind[k1],:,:][(rad_data['lw_clr'][time_ind[k1],:,:] >= 0.) & (np.isfinite(rad_data[k2][time_ind[k1],:,:]))], bins=w500_bins, weights=((rad_data[k2]*clfr_weights)[time_ind[k1],:,:]*area_weights)[(rad_data['lw_clr'][time_ind[k1],:,:] >= 0.) & (np.isfinite(rad_data[k2][time_ind[k1],:,:]))])[0]})
                    data_incr[k1].update({k2+'2_sum_sq' : np.histogram(w500[time_ind[k1],:,:][(rad_data['lw_clr'][time_ind[k1],:,:] >= 0.) & (np.isfinite(rad_data[k2][time_ind[k1],:,:]))], bins=w500_bins, weights=((rad_data[k2]*clfr_weights)[time_ind[k1],:,:]*area_weights)[(rad_data['lw_clr'][time_ind[k1],:,:] >= 0.) & (np.isfinite(rad_data[k2][time_ind[k1],:,:]))]**2)[0]})
                else:
                    data_incr[k1].update({k2+'_sum' : np.zeros(1)-9999})
                    data_incr[k1].update({k2+'_sum_sq' : np.zeros(1)-9999})
                    data_incr[k1].update({k2+'2_sum'  : np.zeros(1)-9999})
                    data_incr[k1].update({k2+'2_sum_sq' : np.zeros(1)-9999})
        for k2 in ['sw_cre', 'lw_cre', 'net_cre', 'sw_cre_adj', 'lw_cre_adj', 'sw_cre_adj2', 'lw_cre_adj2']:
            data_incr[k1].update({k2+'_hist' : np.histogram2d(w500[time_ind[k1],:,:].flatten(), rad_data[k2][time_ind[k1],:,:].flatten(), bins=(w500_bins, cre_bins), weights=area_weights.flatten())[0]})
    return data_incr



# def get_cmip6_dist(spatial_av_scale=2.0, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, experiment='AMIP', yearlist=range(2001,2015)):
#     '''
#     Get omega500 and CRE as a function of omega500 for AMIP CMIP6 models

#     Only MOHC provides wap at timescales other than Amon 
#     '''
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     if experiment == 'AMIP':
#         climate_dict = amip_dict
#     elif experiment == 'AMIP+4K':
#         climate_dict = amip_p4k_dict
#     elif experiment == 'PiControl':
#         climate_dict = picontrol_dict
#     elif experiment == 'abrupt4CO2':
#         climate_dict = abrupt4co2_dict
#     else:
#         STOP
#     w500_hist, w500_sw_cre_hist, w500_lw_cre_hist, sw_clr_sum, sw_cre_sum, sw_cre_sum_sq, sw_all_sum, lw_clr_sum, lw_cre_sum, lw_cre_sum_sq, lw_all_sum = ({} for __ in range(11))
#     print('climate_dict.keys()=', climate_dict.keys())
#     for kk in climate_dict.keys():
#         w500_hist.update({kk : np.zeros(w500_bins.size-1)})
#         w500_sw_cre_hist.update({kk : np.zeros((w500_bins.size-1, cre_bins.size-1))})
#         w500_lw_cre_hist.update({kk : np.zeros((w500_bins.size-1, cre_bins.size-1))})
#         sw_clr_sum.update({kk : np.zeros(w500_bins.size-1)})
#         sw_cre_sum_sq.update({kk : np.zeros(w500_bins.size-1)})
#         sw_cre_sum.update({kk : np.zeros(w500_bins.size-1)})
#         sw_all_sum.update({kk : np.zeros(w500_bins.size-1)})
#         lw_clr_sum.update({kk : np.zeros(w500_bins.size-1)})
#         lw_cre_sum.update({kk : np.zeros(w500_bins.size-1)})
#         lw_cre_sum_sq.update({kk : np.zeros(w500_bins.size-1)})
#         lw_all_sum.update({kk : np.zeros(w500_bins.size-1)})
#         pkl_filename = '/home/users/phill/w500_cre_pkldir/CMIP6_data_'+experiment+'_'+kk+'_year'+str(yearlist[0])+'-'+str(yearlist[-1])+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_v2area_weighted.pbz2'
#         if isfile(pkl_filename):
#             print('Reading '+pkl_filename)
#             with bz2.BZ2File(pkl_filename, 'rb') as fp:
#                 w500_hist[kk], w500_sw_cre_hist[kk], w500_lw_cre_hist[kk], sw_clr_sum[kk], sw_cre_sum[kk], sw_cre_sum_sq[kk], sw_all_sum[kk], lw_clr_sum[kk], lw_cre_sum[kk], lw_cre_sum_sq[kk], lw_all_sum[kk] = cPickle.load(fp)
#         else:      
#             wap_filelist = glob.glob(climate_dict[kk])
#             print('kk,wap_filelist=', kk,wap_filelist)
#             print('climate_dict[kk]=', climate_dict[kk])
#             olr_filelist = glob.glob(climate_dict[kk].replace('wap', 'rlut').replace('Emon', 'Amon'))
#             olr_clr_filelist = glob.glob(climate_dict[kk].replace('wap', 'rlutcs').replace('Emon', 'Amon'))
#             osr_filelist = glob.glob(climate_dict[kk].replace('wap', 'rsut').replace('Emon', 'Amon'))
#             osr_clr_filelist = glob.glob(climate_dict[kk].replace('wap', 'rsutcs').replace('Emon', 'Amon'))
#             w500, olr, olr_clr, osr, osr_clr = ([] for __ in range(5))
#             ind_list, [wap_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist] = get_matched_time_ind(wap_filelist, [olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist], yearlist=yearlist)
#             for filename in wap_filelist:
#                 ff = cf.read(filename, select='lagrangian_tendency_of_air_pressure')[0]
#                 new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min, lon_max-0.01, 2)+1, 'degreesE'))
#                 new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min, lat_max-0.01, 2)+1, 'degreesN'))
#                 area_weights = np.repeat(np.cos(np.pi*new_lat.array[:,None]/180),new_lon.size, axis=1)
#                 area_weights = area_weights/area_weights.sum()
#                 try:
#                     pressure = ff.coord('air_pressure').array
#                     ind_p = np.argmin(abs(pressure-50000.))
#                     w500_temp = 24*6*6*ff[:,ind_p,:,:]
#                     w500 += [w500_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#                 except:
#                     if filename == '/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/piControl/r1i1p1f2/Emon/wap/gn/latest/wap_Emon_UKESM1-0-LL_piControl_r1i1p1f2_gn_270001-274912.nc':
#                         pressure = np.concatenate((cf.read('/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/piControl/r1i1p1f2/AERmon/pfull/gn/latest/pfull_AERmon_UKESM1-0-LL_piControl_r1i1p1f2_gn_270001-270912.nc', select='air_pressure')[0].array, cf.read('/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/piControl/r1i1p1f2/AERmon/pfull/gn/latest/pfull_AERmon_UKESM1-0-LL_piControl_r1i1p1f2_gn_271001-274912.nc', select='air_pressure')[0].array), axis=0)# HadGEM3-GC31-LL piControl stores variables in different files.
#                     else:
#                         pressure = cf.read(filename.replace('Emon', 'AERmon').replace('wap', 'pfull'), select='air_pressure')[0].array # HadGEM3-GC31-LL piControl stores variables in different files.
#                     pressure_temp = np.swapaxes(pressure, 0,1).reshape(85,int(pressure.size/85))
#                     ind = np.argmin(abs(pressure_temp-50000), axis=0)
#                     print('filename=', filename)
#                     w500_temp2 = 24*6*6*cf.read(filename, select='lagrangian_tendency_of_air_pressure')[0].array
#                     print('w500_temp2.shape=', w500_temp2.shape)
#                     w500_temp2 = np.swapaxes(w500_temp2, 0,1).reshape(85,int(w500_temp2.size/85))[ind,np.arange(int(w500_temp2.size/85))].reshape(w500_temp2.shape[0],w500_temp2.shape[2],w500_temp2.shape[3])
#                     w500_temp = cf.read(glob.glob(abrupt4co2_dict[kk])[0], select='lagrangian_tendency_of_air_pressure')[0][:w500_temp2.shape[0],0,:,:]
#                     print('w500_temp.shape=', w500_temp.shape)
#                     w500_temp[:,0,:,:] = w500_temp2[:,None,:,:]
#                 w500 += [w500_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             w500 = np.concatenate(w500, axis=0)
#             print('w500.shape=', w500.shape)
#             print('ind_list[0]=', ind_list[0])
#             w500 = w500[ind_list[0],:,:]
#             print('w500.shape=', w500.shape)
#             area_weights = np.repeat(area_weights[None,:,:], ind_list[0].size, axis=0)
#             w500_hist[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=area_weights.flatten()) 
#             for filename in olr_filelist:     
#                 olr_temp = cf.read(filename, select='toa_outgoing_longwave_flux')[0]
#                 olr += [olr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             olr = np.concatenate(olr, axis=0)[ind_list[1],:,:]
#             lw_all_sum[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=olr.flatten()*area_weights.flatten())
#             for filename in olr_clr_filelist:         
#                 olr_clr_temp = cf.read(filename, select='toa_outgoing_longwave_flux_assuming_clear_sky')[0]
#                 olr_clr += [olr_clr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             olr_clr = np.concatenate(olr_clr, axis=0)[ind_list[2],:,:]
#             lw_clr_sum[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=olr_clr.flatten()*area_weights.flatten())
#             for filename in osr_filelist:          
#                 osr_temp = cf.read(filename, select='toa_outgoing_shortwave_flux')[0]
#                 osr += [osr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             osr = np.concatenate(osr, axis=0)[ind_list[3],:,:]
#             sw_all_sum[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=osr.flatten()*area_weights.flatten())
#             for filename in osr_clr_filelist:         
#                 osr_clr_temp = cf.read(filename, select='toa_outgoing_shortwave_flux_assuming_clear_sky')[0]
#                 osr_clr += [osr_clr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             osr_clr = np.concatenate(osr_clr, axis=0)[ind_list[4],:,:]
#             sw_clr_sum[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=osr_clr.flatten()*area_weights.flatten())
#             sw_cre_sum[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=(osr_clr-osr).flatten()*area_weights.flatten())
#             sw_cre_sum_sq[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=((osr_clr-osr).flatten()**2)*area_weights.flatten()) 
#             lw_cre_sum[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=(olr_clr-olr).flatten()*area_weights.flatten())
#             lw_cre_sum_sq[kk], _ = np.histogram(w500.flatten(), bins=w500_bins, weights=((olr_clr-olr).flatten()**2)*area_weights.flatten())
#             w500_sw_cre_hist[kk] = np.histogram2d(w500.flatten(), (osr_clr-osr).flatten(), bins=(w500_bins, cre_bins), weights=area_weights.flatten())[0]
#             w500_lw_cre_hist[kk] = np.histogram2d(w500.flatten(), (olr_clr-olr).flatten(), bins=(w500_bins, cre_bins), weights=area_weights.flatten())[0]
#             with bz2.BZ2File(pkl_filename, 'w') as fp:   
#                 cPickle.dump([w500_hist[kk], w500_sw_cre_hist[kk], w500_lw_cre_hist[kk], sw_clr_sum[kk], sw_cre_sum[kk], sw_cre_sum_sq[kk], sw_all_sum[kk], lw_clr_sum[kk], lw_cre_sum[kk], lw_cre_sum_sq[kk], lw_all_sum[kk]], fp, protocol=4)
#     return w500_hist, w500_sw_cre_hist, w500_lw_cre_hist, sw_clr_sum, sw_cre_sum, sw_cre_sum_sq, sw_all_sum, lw_clr_sum, lw_cre_sum, lw_cre_sum_sq, lw_all_sum


# def get_matched_time_ind(wap_filelist, filelist_list, yearlist=range(2001,2015)):
#     time_vals = []
#     filename_vals = []
#     print('Start of get matched_time_ind, wap_filelist=', wap_filelist)
#     for filelist in [wap_filelist,]+ filelist_list:
#         time_vals_temp = np.zeros(0)
#         filename_vals_temp = np.zeros(0)
#         for filename in filelist:
#             print('filename=', filename)
#             ff = cf.read(filename)[-1]
#             nctime = ff.coord('time').array
#             t_unit = ff.coord('time').units
#             try:
#                 t_cal = ff.coord('time').calendar
#             except AttributeError : # Attribute doesn't exist:
#                 t_cal = u"gregorian" # or standard
#             temp = num2date(nctime,units = t_unit,calendar = t_cal)
#             time_vals_temp = np.concatenate((time_vals_temp, num2date(nctime,units = t_unit,calendar = t_cal)))
#             filename_vals_temp = np.concatenate((filename_vals_temp, np.repeat(filename, nctime.size)))
#         time_vals += [np.array(time_vals_temp)]
#         filename_vals += [filename_vals_temp]
#         print('filelist=', filelist)
#         print('time_vals_temp=', time_vals_temp)
#     if 'piControl' in wap_filelist[0]:
#         all_times = np.array([t for t in time_vals[0] if ((t in time_vals[1]) & (t in time_vals[2]) & (t in time_vals[3]) & (t in time_vals[4]))])[:1800] # first 150 years that are available in all files
#     elif 'abrupt-4xCO2' in wap_filelist[0]:
#        all_times = np.array([t for t in time_vals[0] if ((t in time_vals[1]) & (t in time_vals[2]) & (t in time_vals[3]) & (t in time_vals[4]))])[:1800] # First 150 years that are available in all files
#     elif 'amip' in wap_filelist[0]:
#        all_times = np.array([t for t in time_vals[0] if ((t in time_vals[1]) & (t in time_vals[2]) & (t in time_vals[3]) & (t in time_vals[4]) & (t.year in yearlist))]) # Years are meaningful for AMIP
#     ind_list = []
#     necessary_files = []
#     print('all_times=', all_times)
#     print('time_vals=', time_vals)
#     for i in range(len(filelist_list)+1):
#         print('i, time_vals[i][0], time_vals[i][-1]=', i, time_vals[i][0], time_vals[i][-1])
#         ind_list += [np.intersect1d(all_times, time_vals[i], return_indices=True)[2]] # Index for time dimension for each diagnostic
#         print('ind_list=', ind_list)
#         necessary_files += [np.unique(filename_vals[i][ind_list[i]])]
#         print('necessary_files=', necessary_files)
#         ind_list[i] -= np.where(filename_vals[i] == necessary_files[i][0])[0][0]
#     return ind_list, necessary_files
            

# def compare_reanalyses(yearlist=[2005], w500_bins=np.arange(-700,700.01,2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, show_plots=True):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     saveroot_year = str(yearlist[0])+'-'+str(yearlist[-1])+'_lon{:.1f}'.format(lon_min)+'to{:.1f}'.format(lon_max)+'_lat{:.1f}'.format(lat_min)+'to{:.1f}'.format(lat_max)
#     saveroot_year.replace('.', 'pt')
#     merra2_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='MERRA2', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='ERA5', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_vs_ceres_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='JRA55', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     w500_data = [era5_one_deg_hourly, merra2_one_deg_hourly, jra55_one_deg_hourly]
#     w500_cre_data = w500_data + [era5_vs_ceres_one_deg_hourly,merra2_vs_ceres_one_deg_hourly,jra55_vs_ceres_one_deg_hourly]
#     reanalysis_comparison_plots(w500_data, w500_cre_data, saveroot='onedeg_hourly_'+saveroot_year, title='One degree hourly', year_range=str(yearlist[0])+'-'+str(yearlist[-1]), show_plots=show_plots)
#     merra2_one_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='MERRA2', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_one_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_one_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='ERA5', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_vs_ceres_one_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_one_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='JRA55', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_one_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     w500_data = [era5_one_deg_daily, merra2_one_deg_daily, jra55_one_deg_daily]
#     w500_cre_data  = w500_data + [era5_vs_ceres_one_deg_daily,merra2_vs_ceres_one_deg_daily,jra55_vs_ceres_one_deg_daily]
#     reanalysis_comparison_plots(w500_data,w500_cre_data, saveroot='onedeg_daily_'+saveroot_year, title='One degree daily', year_range=str(yearlist[0])+'-'+str(yearlist[-1]), show_plots=show_plots)
#     merra2_two_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='MERRA2', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_two_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_two_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='ERA5', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist) # temporarily use era5-ceres-syn as proxy for era5 as w500 is from the same source.
#     era5_vs_ceres_two_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_two_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='JRA55', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_two_deg_daily = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     w500_data = [era5_two_deg_daily, merra2_two_deg_daily, jra55_two_deg_daily]
#     w500_cre_data = w500_data + [era5_vs_ceres_two_deg_daily,merra2_vs_ceres_two_deg_daily,jra55_vs_ceres_two_deg_daily]
#     reanalysis_comparison_plots(w500_data, w500_cre_data, saveroot='twodeg_daily_'+saveroot_year, title='Two degree daily', year_range=str(yearlist[0])+'-'+str(yearlist[-1]), show_plots=show_plots)
# #    return
#     merra2_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='MERRA2', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='ERA5', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist) 
#     era5_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='JRA55', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     w500_data = [era5_two_deg_monthly, merra2_two_deg_monthly, jra55_two_deg_monthly]
#     w500_cre_data = w500_data + [era5_vs_ceres_two_deg_monthly,merra2_vs_ceres_two_deg_monthly,jra55_vs_ceres_two_deg_monthly]
#     reanalysis_comparison_plots(w500_data, w500_cre_data, saveroot='twodeg_monthly_'+saveroot_year, title='Two degree monthly', year_range=str(yearlist[0])+'-'+str(yearlist[-1]), show_plots=show_plots)


# def reanalysis_comparison_plots(w500_data, w500_cre_data, w500_bins=np.arange(-700,700.01,2), saveroot='twodeg_daily', title='Two degree daily', year_range='2001-2020', w500_legend=['ERA5', 'MERRA2', 'JRA55'], w500_cre_legend=['ERA5', 'MERRA2', 'JRA55', 'ERA5-CERES', 'MERRA2-CERES', 'JRA55-CERES'], show_plots=False, label_mode=True, xlim=[-300.,300.]):
#     w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
#     for kk in ['Ann']:
# #    for k in ['Ann', 'DJF', 'MAM', 'JJA', 'SON']:
# #       w500 distribution plot
#         legend_with_mean = []
#         for ii,datum in enumerate(w500_data):
#             plt.plot(w500_bins_mid,datum[kk]['w500_hist']/datum[kk]['w500_hist'].sum(), linewidth=4.0, color=colorlist[ii % 4], linestyle=stylelist[ii % 3])
#             legend_with_mean += [w500_legend[ii]+' {:.2f}'.format(np.sum(datum[kk]['w500_hist']*abs(w500_bins_mid))/np.sum(datum[kk]['w500_hist']))]
#         plt.legend(legend_with_mean)
#         plt.title(title+' '+kk+' '+year_range)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.ylabel('Probability Density')
#         plt.gca().set_ylim(bottom=0)
#         plt.xlim(xlim)
#         plt.grid(color='lightgrey')
#         plt.savefig('/home/users/phill/images/CIRCULATES/omega500_reanalyses_comparison_'+saveroot+'_'+kk+plot_type, dpi=my_dpi)
#         if show_plots:
#             plt.show()
#         else:
#             plt.close('all')
# #       cre vs w500 plots
#         rad_dict = {'sw_cre_mean' : 'SW',
#                     'lw_cre_mean' : 'LW',
#                     'net_cre_mean' : 'net'
#                    }
#         for jj,k2 in enumerate(rad_dict.keys()):
#             fig = plt.figure(jj)
#             legend_with_mean = []
#             for ii,datum in enumerate(w500_cre_data):
#                 plt.plot(w500_bins_mid,datum[k][k2], linewidth=4.0, color=colorlist[ii % 4], linestyle=stylelist[ii % 3])
#                 legend_with_mean += [w500_cre_legend[ii]+' {:.2f}'.format(np.sum(datum[k][k2.replace('mean', 'sum')])/np.sum(datum[k]['w500_hist']))]
#                 if label_mode:
#                     plt.scatter(w500_bins_mid[np.argmax(datum[k]['w500_hist'])], datum[k][k2][np.argmax(datum[k]['w500_hist'])], color=colorlist[ii % 4], linestyle=stylelist[ii % 3], marker='*')
#             plt.legend(legend_with_mean)
#             plt.title(title+' '+k+' '+year_range)
#             plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#             plt.ylabel('TOA '+rad_dict[k2]+' CRE (W m$^{-2}$)')
#             plt.xlim(xlim)
#             plt.grid(color='lightgrey')
#             plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_'+rad_dict[k2]+'cre_reanalyses_comparison_'+saveroot+'_'+k+plot_type, dpi=my_dpi)
#         if show_plots:
#             plt.show()
#         else:
#             plt.close('all')
#         cld_dict = {'clfr_sum' : 'Total Cloud Fraction (%)',
#                     'high_clfr_sum' : 'High Cloud Fraction (%)',
#                     'midhigh_clfr_sum' : 'Midhigh Cloud Fraction (%)',
#                     'midlow_clfr_sum' : 'Midlow Cloud Fraction (%)',
#                     'low_clfr_sum' : 'Low Cloud Fraction (%)',
#                     'cod_sum' : 'Total Cloud Optical Depth',
#                     'high_cod_sum' : 'High Cloud Optical Depth',
#                     'midhigh_cod_sum' : 'Midhigh Cloud Optical Depth',
#                     'midlow_cod_sum' : 'Midlow Cloud Optical Depth',
#                     'low_cod_sum' : 'Low Cloud Optical Depth',
#                     'cprice_sum' : 'Total Cloud Ice Particle Radius',
#                     'high_cprice_sum' : 'High Cloud Ice Particle Radius',
#                     'midhigh_cprice_sum' : 'Midhigh Cloud Ice Particle Radius',
#                     'midlow_cprice_sum' : 'Midlow Cloud Ice Particle Radius',
#                     'low_cprice_sum' : 'Low Cloud Ice Particle Radius',
#                     'cprwat_sum' : 'Total Cloud Wat Particle Radius',
#                     'high_cprwat_sum' : 'High Cloud Wat Particle Radius',
#                     'midhigh_cprwat_sum' : 'Midhigh Cloud Wat Particle Radius',
#                     'midlow_cprwat_sum' : 'Midlow Cloud Wat Particle Radius',
#                     'low_cprwat_sum' : 'Low Cloud Wat Particle Radius'
#                    }
#         cld_range_dict={'clfr_sum' : [0,100],
#                         'high_clfr_sum' : [0,100],
#                         'midhigh_clfr_sum' : [0,100],
#                         'midlow_clfr_sum' : [0,100],
#                         'low_clfr_sum' : [0,100],
#                         'cod_sum' : [0,30],
#                         'high_cod_sum' : [0,30],
#                         'midhigh_cod_sum' : [0,30],
#                         'midlow_cod_sum' : [0,30],
#                         'low_cod_sum' : [0,30],
#                         'cprice_sum' : [0,40],
#                         'high_cprice_sum' : [0,40],
#                         'midhigh_cprice_sum' : [0,40],
#                         'midlow_cprice_sum' : [0,40],
#                         'low_cprice_sum' : [0,40],
#                         'cprwat_sum' : [0,20],
#                         'high_cprwat_sum' : [0,20],
#                         'midhigh_cprwat_sum' : [0,20],
#                         'midlow_cprwat_sum' : [0,20],
#                         'low_cprwat_sum' : [0,20]
#                        }
#         cld_divisor_dict={'clfr_sum' : 'w500_hist',
#                           'high_clfr_sum' : 'w500_hist',
#                           'midhigh_clfr_sum' : 'w500_hist',
#                           'midlow_clfr_sum' : 'w500_hist',
#                           'low_clfr_sum' : 'w500_hist',
#                           'cod_sum' : 'clfr_sum',
#                           'high_cod_sum' : 'high_clfr_sum',
#                           'midhigh_cod_sum' : 'midhigh_clfr_sum',
#                           'midlow_cod_sum' : 'midlow_clfr_sum',
#                           'low_cod_sum' : 'low_clfr_sum',
#                           'cprice_sum' : 'ice_clfr_sum',
#                           'high_cprice_sum' : 'ice_high_clfr_sum',
#                           'midhigh_cprice_sum' : 'ice_midhigh_clfr_sum',
#                           'midlow_cprice_sum' : 'ice_midlow_clfr_sum',
#                           'low_cprice_sum' : 'ice_low_clfr_sum',
#                           'cprwat_sum' : 'liq_clfr_sum',
#                           'high_cprwat_sum' : 'liq_high_clfr_sum',
#                           'midhigh_cprwat_sum' : 'liq_midhigh_clfr_sum',
#                           'midlow_cprwat_sum' : 'liq_midlow_clfr_sum',
#                           'low_cprwat_sum' : 'liq_low_clfr_sum'
#                          }
#         for jj,k2 in enumerate(cld_dict.keys()):
#             fig  = plt.figure(jj)
#             legend_with_mean = []
#             for ii, datum in enumerate(w500_cre_data):
#                 divisor = datum[k][cld_divisor_dict[k2]]
#                 divisor2 = datum[k][cld_divisor_dict[k2].replace('clfr', 'clfr2').replace('hist', 'hist_lw')]
#                 if np.max(abs(datum[k][k2])) > 0:
#                     print('w500_cre_legend[ii],datum[k][k2]', w500_cre_legend[ii],datum[k][k2])
#                     plt.plot(w500_bins_mid,datum[k][k2]/divisor, linewidth=4.0, color=colorlist[ii % 4], linestyle=stylelist[ii % 3])
#                     legend_with_mean += [w500_cre_legend[ii]+' {:.2f}'.format(np.sum(datum[k][k2])/np.sum(divisor))]
#                     plt.plot(w500_bins_mid,datum[k][k2.replace('_sum', '2_sum')]/divisor2, linewidth=4.0)
#                     legend_with_mean += [w500_cre_legend[ii]+'2 {:.2f}'.format(np.sum(datum[k][k2.replace('_sum', '2_sum')])/np.sum(divisor2))]
#                 plt.legend(legend_with_mean)
#                 plt.title(title+' '+k+' '+year_range)
#                 plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#                 plt.ylabel(cld_dict[k2])
#                 plt.xlim(xlim)
#                 plt.ylim(cld_range_dict[k2])
#                 plt.grid(color='lightgrey')
#                 plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_'+k2+'_reanalyses_comparison_'+saveroot+'_'+k+plot_type, dpi=my_dpi)
#         if show_plots:
#             plt.show()
#         else:
#             plt.close('all')
# #    return
#     colorlist_seas=['k', '#e66101','#fdb863','#b2abd2','#5e3c99']
#     for ii, datum in enumerate(w500_cre_data):
#         legend_with_mean = []
#         for jj,k in enumerate(['Ann', 'DJF', 'MAM', 'JJA', 'SON']):
#             plt.plot(w500_bins_mid,datum[k]['w500_hist']/datum[k]['w500_hist'].sum(), linewidth=4.0, color=colorlist_seas[jj])
#             legend_with_mean += [k+' {:.2f}'.format(np.sum(datum[k]['w500_hist']*abs(w500_bins_mid))/np.sum(datum[k]['w500_hist']))]
#         plt.legend(legend_with_mean)
#         print('ii=', ii)
#         print('len(w500_cre_data)=', len(w500_cre_data))
#         print('w500_cre_legend=', w500_cre_legend)
#         plt.title(title+' '+w500_cre_legend[ii]+' '+year_range)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.ylabel('Probability Density')
#         plt.gca().set_ylim(bottom=0)
#         plt.xlim(xlim)
#         plt.grid(color='lightgrey')
#         plt.savefig('/home/users/phill/images/CIRCULATES/omega500_reanalyses_comparison_'+saveroot+'_'+w500_cre_legend[ii]+plot_type, dpi=my_dpi)
#         if show_plots:
#             plt.show()
#         else:
#             plt.close('all')
#         for ll,k2 in enumerate(rad_dict.keys()):
#             fig = plt.figure(ll)
#             legend_with_mean = []
#             for jj,k in enumerate(['Ann', 'DJF', 'MAM', 'JJA', 'SON']):
#                 plt.plot(w500_bins_mid,datum[k][k2], linewidth=4.0, color=colorlist_seas[jj])
#                 legend_with_mean += [k+' {:.2f}'.format(np.sum(datum[k][k2.replace('mean', 'sum')])/np.sum(datum[k]['w500_hist']))]
#                 if label_mode:
#                     print('k=', k)
#                     print('k2=', k2)
#                     print("datum[k]['w500_hist']=", datum[k]['w500_hist'])
#                     print("np.argmax(datum[k]['w500_hist'])=", np.argmax(datum[k]['w500_hist']))
#                     print("w500_bins_mid[np.argmax(datum[k]['w500_hist'])]=", w500_bins_mid[np.argmax(datum[k]['w500_hist'])])
#                     print("datum[k][k2][np.argmax(datum[k]['w500_hist'])]=", datum[k][k2][np.argmax(datum[k]['w500_hist'])])
#                     plt.scatter(w500_bins_mid[np.argmax(datum[k]['w500_hist'])], datum[k][k2][np.argmax(datum[k]['w500_hist'])], color=colorlist_seas[jj], marker='*')
#             plt.legend(legend_with_mean)
#             plt.title(title+' '+w500_cre_legend[ii]+' '+year_range)
#             plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#             plt.ylabel('TOA '+rad_dict[k2]+' CRE (W m$^{-2}$)')
#             plt.xlim(xlim)
#             plt.grid(color='lightgrey')
#             plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_'+rad_dict[k2]+'_cre_reanalyses_comparison_'+saveroot+'_'+w500_cre_legend[ii]+plot_type, dpi=my_dpi)
#         if show_plots:
#             plt.show()
#         else:
#             plt.close('all')
#         legend_with_mean = []
#         if 'clfr_sum' in datum['Ann'].keys():
#             for ll,k2 in enumerate(cld_dict.keys()):
#                 fig  = plt.figure(ll)
#                 legend_with_mean = []
#                 for jj,k in enumerate(['Ann', 'DJF', 'MAM', 'JJA', 'SON']):
#                     divisor = datum[k][cld_divisor_dict[k2]]
#                     plt.plot(w500_bins_mid,datum[k][k2]/divisor, linewidth=4.0, color=colorlist_seas[jj])
#                     legend_with_mean += [k+' {:.2f}'.format(np.sum(datum[k][k2])/np.sum(divisor))]
#                 plt.legend(legend_with_mean)
#                 plt.title(title+' '+w500_cre_legend[ii]+' '+year_range)
#                 plt.ylabel(cld_dict[k2])
#                 plt.xlim(xlim)
#                 plt.ylim(cld_range_dict[k2])
#                 plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#                 plt.grid(color='lightgrey')
#                 plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_'+k2+'_reanalyses_comparison_'+saveroot+'_'+w500_cre_legend[ii]+plot_type, dpi=my_dpi)
#             if show_plots:
#                 plt.show()
#             else:
#                 plt.close('all')
# #   Now plot histograms of CRE vs w500
#     rad_dict = {'sw_cre_hist' : 'SW',
#                 'lw_cre_hist' : 'LW',
#                 'net_cre_hist' : 'net'
#                 }
# #    for k in ['Ann', 'DJF', 'MAM', 'JJA', 'SON']:
#     for k in ['Ann']:
#         for ii,k2 in enumerate(rad_dict.keys()):
#             for jj,datum in enumerate(w500_cre_data):
#                 fig = plt.figure(ii*len(w500_cre_data)+jj)
#                 plt.pcolormesh(w500_bins_mid, cre_bins_mid, ((datum[k][k2].T/datum[k][k2].sum(axis=1))))
#                 plt.title(title+' '+k+' '+year_range)
#                 plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#                 plt.ylabel('TOA '+rad_dict[k2]+' CRE (W m$^{-2}$)')
#                 plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_'+rad_dict[k2]+'cre_reanalyses_hist_comparison_'+saveroot+'_'+k+plot_type, dpi=my_dpi)
#         if show_plots:
#             plt.show()
#         else:
#             plt.close('all')


# def compare_reanalysis_sampling(w500_bins=np.arange(-700,700.01,2), show_plots=True):
#     merra2_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='MERRA2', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(1981,2021))
#     merra2_one_deg_hourly21c = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='MERRA2', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(2001,2020))
# #    era5_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='ERA5', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(1981,2021))
#     era5_one_deg_hourly21c = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='ERA5', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(2001,2021))
#     jra55_one_deg_hourly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='JRA55', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(1981,2021))
#     jra55_one_deg_hourly21c = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='JRA55', w500_bins=w500_bins, spatial_av_scale=1, time_av_scale=1, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(2001,2021))
# #    w500_data = [era5_one_deg_hourly, merra2_one_deg_hourly, jra55_one_deg_hourly,era5_one_deg_hourly21c,merra2_one_deg_hourly21c,jra55_one_deg_hourly21]
#     w500_data = [merra2_one_deg_hourly, jra55_one_deg_hourly,era5_one_deg_hourly21c,merra2_one_deg_hourly21c,jra55_one_deg_hourly21]
# #    w500_legend=['ERA5 1981-2020', 'MERRA2 1981-2020', 'JRA55 1981-2020', 'ERA5 2001-2020', 'MERRA2 2001-2020', 'JRA55 2001-2020']
#     w500_legend=['MERRA2 1981-2020', 'JRA55 1981-2020', 'ERA5 2001-2020', 'MERRA2 2001-2020', 'JRA55 2001-2020']
#     reanalysis_comparison_plots(w500_data, w500_data, saveroot='onedeg_hourly_sampling_comparison', title='One degree hourly', year_range='', w500_legend=w500_legend, w500_cre_legend=w500_legend, show_plots=show_plots)


# def plot_reanalysis_timseries(yearlist=range(2001,2021), w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), spatial_av_scale=2, time_av_scale=24, data2='None', time_res='bimonthly', n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, show_plots=False):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
# #    merra2_data = get_reanalysis_timeseries(yearlist, 'MERRA2', 'CERES_SYN', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, w500_bins=w500_bins)
#     pkl_filename = '/home/users/phill/w500_cre_pkldir/reanalysis_timeseries_space_av'+str(int(spatial_av_scale))+'_time_av'+str(int(time_av_scale))+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_year'+str(yearlist[0])+'to'+str(yearlist[-1])+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'n_bootstrap'+str(n_bootstrap)+'_v2area_weighted.pkl'
#     if isfile(pkl_filename):
#         print('Reading '+pkl_filename)
#         with open(pkl_filename, 'rb') as fp:
#             era5_data, merra2_data, jra55_data, tot_data = cPickle.load(fp)
#     else:
#         era5_data = get_reanalysis_timeseries(yearlist, 'ERA5', 'CERES_SYN', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, w500_bins=w500_bins, cre_bins=cre_bins, n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#         merra2_data = get_reanalysis_timeseries(yearlist, 'MERRA2', 'CERES_SYN', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, w500_bins=w500_bins, n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#         jra55_data = get_reanalysis_timeseries(yearlist, 'JRA55', 'CERES_SYN', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, w500_bins=w500_bins, n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#         tot_data = get_reanalysis_timeseries(yearlist, 'CombinedReanalyses', 'CERES_SYN', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, w500_bins=w500_bins, n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#         with open(pkl_filename, 'wb') as fp:   
#             cPickle.dump([era5_data, merra2_data, jra55_data, tot_data], fp, protocol=4)
         
#     ax2_data = -9999
#     if data2 == 'ENSO':
#         if ((time_res == 'bimonthly') | (time_res == 'bimonthly Oct-Mar')):
#             year, bimonthly_enso_index = read_meiv2_data(yearlist)
#             ax2_label='ENSO index'
#             ax2_data = bimonthly_enso_index.flatten()
#         else:
#             print('ENSO Index is only at bimonthly timescales')
#     elif data2 == 'SST':
#         ostia_sst = read_ostia_mean_sst()
#         ax2_label='Mean SST'
#         if ((time_res == 'bimonthly') | (time_res == 'bimonthly Oct-Mar')):
#             ax2_data = ostia_sst['bimonthly_tseries']
#         elif time_res == 'monthly':
#             ax2_data = ostia_sst['monthly_tseries']
#         elif time_res == 'annual':
#             ax2_data = ostia_sst['annual_tseries']
#     elif data2 == 'w500':
#         ax2_label='Mean circulation strength'
#         if ((time_res == 'bimonthly') | (time_res == 'bimonthly Oct-Mar')):
#             ax2_data = era5_data['bimonthly_tseries_w500']
#         elif time_res == 'monthly':
#             ax2_data = era5_data['monthly_tseries_w500']
#         elif time_res == 'annual':
#             ax2_data = era5_data['annual_tseries_w500']
#     elif data2 == 'None':
#         pass
#     else:
#         print('Unable to recognise secondary data name')
#         return 
#     if time_res == 'bimonthly':
#         w500_key = 'bimonthly_tseries_w500'
#         sw_cre_key = 'bimonthly_tseries_sw_cre_param'
#         lw_cre_key = 'bimonthly_tseries_lw_cre_param'
#         timeseries_val = np.arange(yearlist[0], yearlist[-1]+1, 1./12)
#     elif time_res == 'bimonthly Oct-Mar':
#         w500_key = 'bimonthly_tseries_w500'
#         sw_cre_key = 'bimonthly_tseries_sw_cre_param'
#         lw_cre_key = 'bimonthly_tseries_lw_cre_param'
#         timeseries_val = np.arange(yearlist[0], yearlist[-1]+1, 1./12)
#         ind = np.where(((timeseries_val % 1) > 0.8) | ((timeseries_val % 1) < 0.2)) # 0.166666 corresponds to Feb-Mar, 0.75 corresponds to Sept-Oct
#         timeseries_val = timeseries_val[ind]
#         ax2_data = ax2_data[ind]
#         for kk in ['bimonthly_tseries_w500', 'bimonthly_tseries_sw_cre_param', 'bimonthly_tseries_lw_cre_param', 'bimonthly_tseries_sw_cre_bootstrap_param', 'bimonthly_tseries_lw_cre_bootstrap_param']:
#             era5_data[kk] = era5_data[kk][ind]
#             jra55_data[kk] = jra55_data[kk][ind]
#             merra2_data[kk] = merra2_data[kk][ind]
#             tot_data[kk] = tot_data[kk][ind]
#     elif time_res == 'monthly':
#         w500_key = 'monthly_tseries_w500'
#         sw_cre_key = 'monthly_tseries_sw_cre_param'
#         lw_cre_key = 'monthly_tseries_lw_cre_param'
#         timeseries_val = np.arange(yearlist[0], yearlist[-1]+1, 1./12)
#     elif time_res == 'annual':
#         w500_key = 'annual_tseries_w500'
#         sw_cre_key = 'annual_tseries_sw_cre_param'
#         lw_cre_key = 'annual_tseries_lw_cre_param'
#         timeseries_val = np.arange(yearlist[0], yearlist[-1]+1)
#     else:
#         print('Unable to recognise time resolution')
#         return
#     fig = plt.figure(0)
#     ax1 = fig.add_subplot(111)
#     plt.plot(timeseries_val, era5_data[w500_key], 'r-*')
#     plt.plot(timeseries_val, merra2_data[w500_key], 'g-*')
#     plt.plot(timeseries_val, jra55_data[w500_key], 'b-*')
#     ax1.legend(['ERA5', 'MERRA2', 'JRA55'])
#     ax1.set_ylabel('Mean Circulation Strength (hPa day$^{-1}$)')
#     ax1.set_xlabel('Year')
#     if data2 != 'None':
#         ax2 = ax1.twinx()
#         ax2.set_ylabel(ax2_label)
#         plt.plot(timeseries_val, ax2_data, 'k->')
#         ax2.legend([ax2_label])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/reanalyses_circ_strength_and_'+data2+'_'+time_res.replace(' ', '')+'_timeseries'+plot_type, dpi=my_dpi)
#     if show_plots:
#         plt.show()
#     else:
#         plt.close('all')
# #    return era5_data, merra2_data, jra55_data, bimonthly_enso_index
#     if data2 != 'None':
#         plot_circ_correlations(ax2_data, ax2_label, 'Mean Circulation Strength (hPa day$^{-1}$)', era5_data[w500_key][1:], merra2_data[w500_key][1:], jra55_data[w500_key][1:], 'circ_strength_and_'+data2+'_'+time_res.replace(' ', '')+'_scatter'+plot_type, dpi=my_dpi)
#     fig = plt.figure(0)
#     ax1 = fig.add_subplot(111)
#     plt.plot(timeseries_val, era5_data[sw_cre_key][:,0].flatten(), 'r-*')
#     plt.plot(timeseries_val, merra2_data[sw_cre_key][:,0].flatten(), 'g-*')
#     plt.plot(timeseries_val, jra55_data[sw_cre_key][:,0].flatten(), 'b-*')
#     ax1.legend(['ERA5', 'MERRA2', 'JRA55'])
#     ax1.set_ylabel('SW CRE v circ grad')
#     ax1.set_xlabel('Year')
#     if data2 != 'None':
#         ax2 = ax1.twinx()
#         ax2.set_ylabel(ax2_label)
#         plt.plot(timeseries_val, ax2_data, 'k->')
#         ax2.legend([ax2_label])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/reanalyses_sw_cre_grad_and_enso_'+time_res.replace(' ', '')+'_timeseries'+plot_type, dpi=my_dpi)
# #    return era5_data, merra2_data, jra55_data, bimonthly_enso_index
#     if data2 != 'None':
#         plot_circ_correlations(ax2_data, ax2_label, 'SW CRE v circ grad', era5_data[sw_cre_key][:,0].flatten()[1:], merra2_data[sw_cre_key][:,0].flatten()[1:], jra55_data[sw_cre_key][:,0].flatten()[1:], 'sw_cre_grad_and_'+data2+'_'+time_res.replace(' ', '')+'_scatter'+plot_type, dpi=my_dpi)
#     fig = plt.figure(0)
#     ax1 = fig.add_subplot(111)
#     plt.plot(timeseries_val, era5_data[lw_cre_key][:,0].flatten(), 'r-*')
#     plt.plot(timeseries_val, merra2_data[lw_cre_key][:,0].flatten(), 'g-*')
#     plt.plot(timeseries_val, jra55_data[lw_cre_key][:,0].flatten(), 'b-*')
#     ax1.legend(['ERA5', 'MERRA2', 'JRA55'])
#     ax1.set_ylabel('LW CRE v circ grad')
#     ax1.set_xlabel('Year')
#     if data2 != 'None':
#         ax2 = ax1.twinx()
#         ax2.set_ylabel(ax2_label)
#         plt.plot(timeseries_val, ax2_data, 'k->')
#         ax2.legend([ax2_label])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/reanalyses_lw_cre_grad_and_enso_'+time_res.replace(' ', '')+'_timeseries'+plot_type, dpi=my_dpi)
# #    return era5_data, merra2_data, jra55_data, bimonthly_enso_index
#     if data2 != 'None':
#         plot_circ_correlations(ax2_data, ax2_label, 'LW CRE v circ grad', era5_data[lw_cre_key][:,0].flatten()[1:], merra2_data[lw_cre_key][:,0].flatten()[1:], jra55_data[lw_cre_key][:,0].flatten()[1:], 'lw_cre_grad_and_'+data2+'_'+time_res.replace(' ', '')+'_scatter'+plot_type, dpi=my_dpi)
#     fig = plt.figure(0)
#     ax1 = fig.add_subplot(111)
#     plt.plot(timeseries_val, era5_data[sw_cre_key][:,1].flatten(), 'r-*')
#     plt.plot(timeseries_val, merra2_data[sw_cre_key][:,1].flatten(), 'g-*')
#     plt.plot(timeseries_val, jra55_data[sw_cre_key][:,1].flatten(), 'b-*')
#     ax1.legend(['ERA5', 'MERRA2', 'JRA55'])
#     ax1.set_ylabel('SW CRE v circ const')
#     ax1.set_xlabel('Year')
#     if data2 != 'None':
#         ax2 = ax1.twinx()
#         ax2.set_ylabel(ax2_label)
#         plt.plot(timeseries_val, ax2_data, 'k->')
#         ax2.legend([ax2_label])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/reanalyses_sw_cre_intercept_and_enso_'+time_res.replace(' ', '')+'_timeseries'+plot_type, dpi=my_dpi)
# #    return era5_data, merra2_data, jra55_data, bimonthly_enso_index
#     if data2 != 'None':
#         plot_circ_correlations(ax2_data, ax2_label, 'SW CRE v circ const', era5_data[sw_cre_key][:,1].flatten()[1:], merra2_data[sw_cre_key][:,1].flatten()[1:], jra55_data[sw_cre_key][:,1].flatten()[1:], 'sw_cre_intercept_and_'+data2+'_'+time_res.replace(' ', '')+'_scatter'+plot_type, dpi=my_dpi)
#     fig = plt.figure(0)
#     ax1 = fig.add_subplot(111)
#     plt.plot(timeseries_val, era5_data[lw_cre_key][:,1].flatten(), 'r-*')
#     plt.plot(timeseries_val, merra2_data[lw_cre_key][:,1].flatten(), 'g-*')
#     plt.plot(timeseries_val, jra55_data[lw_cre_key][:,1].flatten(), 'b-*')
#     ax1.legend(['ERA5', 'MERRA2', 'JRA55'])
#     ax1.set_ylabel('LW CRE v circ const')
#     ax1.set_xlabel('Year')
#     if data2 != 'None':
#         ax2 = ax1.twinx()
#         ax2.set_ylabel(ax2_label)
#         plt.plot(timeseries_val, ax2_data, 'k->')
#         ax2.legend([ax2_label])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/reanalyses_lw_cre_intercept_and_enso_'+time_res.replace(' ', '')+'_timeseries'+plot_type, dpi=my_dpi)
# #    return era5_data, merra2_data, jra55_data, bimonthly_enso_index
#     if data2 != 'None':
#         plot_circ_correlations(ax2_data, ax2_label, 'LW CRE v circ const', era5_data[lw_cre_key][:,1].flatten()[1:], merra2_data[lw_cre_key][:,1].flatten()[1:], jra55_data[lw_cre_key][:,1].flatten()[1:], 'lw_cre_intercept_and_'+data2+'_'+time_res.replace(' ', '')+'_scatter'+plot_type, dpi=my_dpi)
# #    return tot_data, era5_data, merra2_data, jra55_data, ax2_data
#     plot_circ_correlations2(ax2_data, ax2_label, tot_data, era5_data, merra2_data, jra55_data, '/home/users/phill/images/CIRCULATES/reanalyses_lw_cre_params_vs_'+data2+'_'+time_res.replace(' ', '_')+'.png', dpi=300, varname=time_res.replace(' Oct-Mar', '')+'_tseries_lw_cre', region='LW')
#     plot_circ_correlations2(ax2_data, ax2_label, tot_data, era5_data, merra2_data, jra55_data, '/home/users/phill/images/CIRCULATES/reanalyses_sw_cre_params_vs_'+data2+'_'+time_res.replace(' ', '_')+'.png', dpi=300, varname=time_res.replace(' Oct-Mar', '')+'_tseries_sw_cre', region='SW')
#     return tot_data, era5_data, merra2_data, jra55_data, ax2_data


# def get_reanalysis_timeseries(yearlist, w500_source, rad_source, spatial_av_scale=2, time_av_scale=24, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, n_bootstrap=2):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     data = {}
#     for k in ['annual_tseries_w500','monthly_tseries_w500', 'bimonthly_tseries_w500', 'annual_tseries_sw_cre_param', 'monthly_tseries_sw_cre_param', 'bimonthly_tseries_sw_cre_param', 'annual_tseries_lw_cre_param', 'monthly_tseries_lw_cre_param', 'bimonthly_tseries_lw_cre_param', 'annual_tseries_sw_cre_bootstrap_param', 'monthly_tseries_sw_cre_bootstrap_param', 'bimonthly_tseries_sw_cre_bootstrap_param', 'annual_tseries_lw_cre_bootstrap_param', 'monthly_tseries_lw_cre_bootstrap_param', 'bimonthly_tseries_lw_cre_bootstrap_param']:
#         data.update({k : []})
#     w500_bins_mid = 0.5*(w500_bins[:-1] + w500_bins[1:])
#     cre_bins_mid = 0.5*(cre_bins[:-1] + cre_bins[1:])
#     fig = plt.figure(0)
#     ax = fig.add_subplot(111)
#     fig = plt.figure(1)
#     ax = fig.add_subplot(111)
#     for year in yearlist:
#         print('year=', year)
#         temp =  match_omega500_rad_reanalyses_obs(w500_source=w500_source, rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=[year])
#         if year > 2001:
#             prev_year =  match_omega500_rad_reanalyses_obs(w500_source=w500_source, rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=[year-1])
#         else:
#             prev_year = {'Dec': {'w500_hist' : np.zeros(w500_bins_mid.size)+np.nan,
#                                  'sw_cre_sum' : np.zeros(w500_bins_mid.size)+np.nan,                            
#                                  'lw_cre_sum' : np.zeros(w500_bins_mid.size)+np.nan,
#                                  'sw_cre_hist' : np.zeros((w500_bins_mid.size, cre_bins_mid.size))+np.nan,                            
#                                  'lw_cre_hist' : np.zeros((w500_bins_mid.size, cre_bins_mid.size))+np.nan
#                         }}
#         data['annual_tseries_w500'] += [np.sum(abs(w500_bins_mid)*temp['Ann']['w500_hist'])/np.sum(temp['Ann']['w500_hist'])]
#         data['monthly_tseries_w500'] += [np.sum(abs(w500_bins_mid)*temp[month]['w500_hist'])/np.sum(temp[month]['w500_hist']) for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
#         data['bimonthly_tseries_w500'] += [np.sum(abs(w500_bins_mid)*(temp['Jan']['w500_hist']+prev_year['Dec']['w500_hist']))/np.sum((temp['Jan']['w500_hist']+prev_year['Dec']['w500_hist']))]
#         data['bimonthly_tseries_w500'] += [np.sum(abs(w500_bins_mid)*(temp[month[0]]['w500_hist']+temp[month[1]]['w500_hist']))/np.sum((temp[month[0]]['w500_hist']+temp[month[1]]['w500_hist'])) for month in [['Jan', 'Feb'], ['Feb', 'Mar'], ['Mar', 'Apr'], ['Apr', 'May'], ['May', 'Jun'], ['Jun', 'Jul'], ['Jul', 'Aug'], ['Aug', 'Sep'], ['Sep', 'Oct'], ['Oct', 'Nov'], ['Nov', 'Dec']]]
#         ann_param = fit_w500_cre_exp_flat2(temp['Ann'], w500_bins, cre_bins, w500_source=w500_source, rad_source=rad_source+'_ANN', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, n_bootstrap=n_bootstrap, yearlist=[year], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#         fig = plt.figure(0)
#         plt.plot(w500_bins_mid, temp['Ann']['sw_cre_mean'], label=str(year))
#         fit = 'A'
#         plt.plot(w500_bins_mid, neg_exp_func_full2(w500_bins_mid, ann_param['SW'][fit]['param'][0], ann_param['SW'][fit]['param'][1], ann_param['SW'][fit]['param'][2], ann_param['SW'][fit]['param'][3]), label=str(year)+' fit')
#         data['annual_tseries_sw_cre_param'] += [ann_param['SW']['A']['param']]
#         data['annual_tseries_lw_cre_param'] += [ann_param['LW']['A']['param']]
#         data['annual_tseries_sw_cre_bootstrap_param'] += [ann_param['SW']['A']['bootstrap_param']]
#         data['annual_tseries_lw_cre_bootstrap_param'] += [ann_param['LW']['A']['bootstrap_param']]
#         for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
#             monthly_param = fit_w500_cre_exp_flat2(temp[month], w500_bins, cre_bins, w500_source=w500_source, rad_source=rad_source+'_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, yearlist=[year], n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#             data['monthly_tseries_sw_cre_param'] += [monthly_param['SW']['A']['param']]
#             data['monthly_tseries_lw_cre_param'] += [monthly_param['LW']['A']['param']]
#             data['monthly_tseries_sw_cre_bootstrap_param'] += [monthly_param['SW']['A']['bootstrap_param']]
#             data['monthly_tseries_lw_cre_bootstrap_param'] += [monthly_param['LW']['A']['bootstrap_param']]
#         print('temp.keys()=', temp.keys())
#         print("temp['Jan'].keys()=", temp['Jan'].keys())
#         print('prev_year.keys()=', prev_year.keys())
#         print("prev_year['Dec'].keys()=", prev_year['Dec'].keys())
#         temp2 = {'sw_cre_mean' : (temp['Jan']['sw_cre_sum']+prev_year['Dec']['sw_cre_sum']) / (temp['Jan']['w500_hist']+prev_year['Dec']['w500_hist']),
#                  'lw_cre_mean' : (temp['Jan']['lw_cre_sum']+prev_year['Dec']['lw_cre_sum']) / (temp['Jan']['w500_hist']+prev_year['Dec']['w500_hist']),
#                  'sw_cre_hist' : temp['Jan']['sw_cre_hist']+prev_year['Dec']['sw_cre_hist'],
#                  'lw_cre_hist' : temp['Jan']['lw_cre_hist']+prev_year['Dec']['lw_cre_hist']
#                 }
#         if np.nanmax(prev_year['Dec']['sw_cre_hist']) != np.nanmax(prev_year['Dec']['sw_cre_hist']): # previous year data doesn't exist, so temp2 here has NaNs, which mess up the fit
#             temp_sw = [np.ones(4)+np.nan]
#             temp_lw = [np.ones(4)+np.nan]
#             bootstrap_temp_sw = [np.ones(np.array(monthly_param['SW']['A']['bootstrap_param']).shape)+np.nan]
#             bootstrap_temp_lw = [np.ones(np.array(monthly_param['SW']['A']['bootstrap_param']).shape)+np.nan]
#         else:
#             bimonthly_param = fit_w500_cre_exp_flat2(temp2, w500_bins, cre_bins, w500_source=w500_source, rad_source=rad_source+'_'+'DecJan', spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, yearlist=[year], n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#             temp_sw = [bimonthly_param['SW']['A']['param']]
#             temp_lw = [bimonthly_param['LW']['A']['param']]
#             bootstrap_temp_sw = [bimonthly_param['SW']['A']['bootstrap_param']]
#             bootstrap_temp_lw = [bimonthly_param['LW']['A']['bootstrap_param']]
#         for months in [['Jan', 'Feb'], ['Feb', 'Mar'], ['Mar', 'Apr'], ['Apr', 'May'], ['May', 'Jun'], ['Jun', 'Jul'], ['Jul', 'Aug'], ['Aug', 'Sep'], ['Sep', 'Oct'], ['Oct', 'Nov'], ['Nov', 'Dec']]:
#             temp2 = {'sw_cre_mean' : (temp[months[0]]['sw_cre_sum']+temp[months[1]]['sw_cre_sum']) / (temp[months[0]]['w500_hist']+temp[months[1]]['w500_hist']),
#                      'lw_cre_mean' : (temp[months[0]]['lw_cre_sum']+temp[months[1]]['lw_cre_sum']) / (temp[months[0]]['w500_hist']+temp[months[1]]['w500_hist']),
#                      'sw_cre_hist' : temp[months[0]]['sw_cre_hist']+temp[months[1]]['sw_cre_hist'],
#                      'lw_cre_hist' : temp[months[0]]['lw_cre_hist']+temp[months[1]]['lw_cre_hist']
#                     }
#             bimonthly_param = fit_w500_cre_exp_flat2(temp2, w500_bins, cre_bins, w500_source=w500_source, rad_source=rad_source+'_'+months[0]+months[1], spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, yearlist=[year], n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#             print("bimonthly_param['SW']['A']['param'].shape=", bimonthly_param['SW']['A']['param'].shape)
#             print("temp_sw[0].shape=", temp_sw[0].shape)
#             temp_sw += [bimonthly_param['SW']['A']['param']]
#             temp_lw += [bimonthly_param['LW']['A']['param']]
#             bootstrap_temp_sw += [bimonthly_param['SW']['A']['bootstrap_param']]
#             bootstrap_temp_lw += [bimonthly_param['LW']['A']['bootstrap_param']]
#         data['bimonthly_tseries_sw_cre_param'] += [[temp_sw]]
#         data['bimonthly_tseries_lw_cre_param'] += [[temp_lw]]
#         data['bimonthly_tseries_sw_cre_bootstrap_param'] += [[bootstrap_temp_sw]]
#         data['bimonthly_tseries_lw_cre_bootstrap_param'] += [[bootstrap_temp_lw]]
#     fig = plt.figure(0)
#     plt.xlabel('Circulation Regime ('+chr(969)+'500, hPa day$^{-1}$)')
#     plt.ylabel('TOA SW CRE (W m$^{-2}$)')
#     plt.legend(loc=0)
#     plt.grid(color='lightgrey')
#     plt.xlim([-300,300])
#     plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_sw_cre_'+w500_source+'vs'+rad_source+'_fit_comparison_'+str(yearlist[0])+'to_'+str(yearlist[-1])+plot_type, dpi=my_dpi)
#     fig = plt.figure(1)
#     plt.xlabel('Circulation Regime ('+chr(969)+'500, hPa day$^{-1}$)')
#     plt.ylabel('TOA LW CRE (W m$^{-2}$)')
#     plt.legend(loc=0)
#     plt.grid(color='lightgrey')
#     plt.xlim([-300,300])
#     plt.savefig('/home/users/phill/images/CIRCULATES/omega500_vs_lw_cre_'+w500_source+'vs'+rad_source+'_fit_comparison_'+str(yearlist[0])+'to_'+str(yearlist[-1])+plot_type, dpi=my_dpi)
#     plt.show()
#     for kk in data.keys():
#         data[kk] = np.array(data[kk])
#         print('kk,data[kk].shape=', kk, data[kk].shape)
#     for kk in ['monthly_tseries_sw_cre_param', 'bimonthly_tseries_sw_cre_param', 'monthly_tseries_lw_cre_param', 'bimonthly_tseries_lw_cre_param']:
#         data[kk] = data[kk].reshape(len(yearlist)*12,4)
#     for kk in ['monthly_tseries_sw_cre_bootstrap_param', 'bimonthly_tseries_sw_cre_bootstrap_param', 'monthly_tseries_lw_cre_bootstrap_param', 'bimonthly_tseries_lw_cre_bootstrap_param']:
#         data[kk] = data[kk].reshape(len(yearlist)*12,n_bootstrap,4)
#     return data
    

# def combined_reanalysis_w500_cre_fit(era5_data, merra2_data, jra55_data, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), spatial_av_scale=1, time_av_scale=24, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=range(2001,2021), n_bootstrap=2, month='ANN', show_plots=False, fitting_func=neg_exp_func_full2, rad_source='CERES_SYN'):
#     '''
#     Does fit for combination of reanalyses and each individually for uncertainty

#     Does fit for CRE calculated using model-like clear-sky. If CERES-SYN is the 
#     source, does 2 fits, both using calculated clear-sky but using observed and
#     calculated all-sky

#     sw_cre_hist etc use observed clear-sky, sw_cre_adj_hist etc use calculated
#     clear and all-sky, sw_cre_adj2_hist use calculated clear and observed
#     all-sky
#     '''
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     w500_bins_mid = 0.5*(w500_bins[:-1]+w500_bins[1:])
#     cre_bins_mid = 0.5*(cre_bins[:-1]+cre_bins[1:])
#     tot_data = {}
#     for kk in ['sw_cre_hist', 'sw_cre_sum', 'lw_cre_hist', 'lw_cre_sum', 'w500_hist', 'w500_hist_lw', 'sw_cre_adj_hist', 'lw_cre_adj_hist', 'sw_cre_adj_sum', 'lw_cre_adj_sum', 'sw_cre_adj2_hist', 'lw_cre_adj2_hist', 'sw_cre_adj2_sum', 'lw_cre_adj2_sum']: # Check w500_hist_lw and adj2 variables  will work for CERES_EBAF
#         tot_data.update({kk: era5_data[kk] + merra2_data[kk] + jra55_data[kk]})
#     for kk in ['sw_cre_mean', 'lw_cre_mean', 'sw_cre_adj_mean', 'lw_cre_adj_mean', 'sw_cre_adj2_mean', 'lw_cre_adj2_mean']:# Check adj2 variables  will work for CERES_EBAF
#         tot_data.update({kk: np.nanmean((era5_data[kk][:,None], merra2_data[kk][:,None], jra55_data[kk][:,None]), axis=0)[:,0]})
#     tot_data_param = fit_w500_cre_exp_flat2(tot_data, w500_bins, cre_bins, w500_source='CombinedReanalyses', rad_source=rad_source+'_adj2_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj2_hist', lw_cre_hist='lw_cre_adj2_hist')
#     era5_data_param = fit_w500_cre_exp_flat2(era5_data, w500_bins, cre_bins, w500_source='ERA5', rad_source=rad_source+'_adj2_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj2_hist', lw_cre_hist='lw_cre_adj2_hist')
#     jra55_data_param = fit_w500_cre_exp_flat2(jra55_data, w500_bins, cre_bins, w500_source='JRA55', rad_source=rad_source+'_adj2_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj2_hist', lw_cre_hist='lw_cre_adj2_hist')
#     merra2_data_param = fit_w500_cre_exp_flat2(merra2_data, w500_bins, cre_bins, w500_source='MERRA2', rad_source=rad_source+'_adj2_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj2_hist', lw_cre_hist='lw_cre_adj2_hist')
#     if rad_source == 'CERES_SYN': # Use calculated all-sky as estimate for another source of uncertainty
#         tot_data_param2 = fit_w500_cre_exp_flat2(tot_data, w500_bins, cre_bins, w500_source='CombinedReanalyses', rad_source=rad_source+'_adj_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj_hist', lw_cre_hist='lw_cre_adj_hist')
#         era5_data_param2 = fit_w500_cre_exp_flat2(era5_data, w500_bins, cre_bins, w500_source='ERA5', rad_source=rad_source+'_adj_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj_hist', lw_cre_hist='lw_cre_adj_hist')
#         jra55_data_param2 = fit_w500_cre_exp_flat2(jra55_data, w500_bins, cre_bins, w500_source='JRA55', rad_source=rad_source+'_adj_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj_hist', lw_cre_hist='lw_cre_adj_hist')
#         merra2_data_param2 = fit_w500_cre_exp_flat2(merra2_data, w500_bins, cre_bins, w500_source='MERRA2', rad_source=rad_source+'_adj_'+month, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, fitting_func=fitting_func, sw_cre_hist='sw_cre_adj_hist', lw_cre_hist='lw_cre_adj_hist')
#     tot_data_param.update({'Circ Intensity' : (tot_data['w500_hist']*w500_bins_mid)[w500_bins_mid > 0.].sum()/tot_data['w500_hist'][w500_bins_mid > 0].sum()-(tot_data['w500_hist']*w500_bins_mid)[w500_bins_mid < 0.].sum()/tot_data['w500_hist'][w500_bins_mid < 0].sum()})
#     tot_data_param.update({'Circ mav' : np.sum(tot_data['w500_hist']*abs(w500_bins_mid))/np.sum(tot_data['w500_hist'])})
#     tot_data_param.update({'Circ Mode' : w500_bins_mid[np.argmax(tot_data['w500_hist'])]})
#     era5_data_param.update({'Circ Intensity' : (era5_data['w500_hist']*w500_bins_mid)[w500_bins_mid > 0.].sum()/era5_data['w500_hist'][w500_bins_mid > 0].sum()-(era5_data['w500_hist']*w500_bins_mid)[w500_bins_mid < 0.].sum()/era5_data['w500_hist'][w500_bins_mid < 0].sum()})
#     era5_data_param.update({'Circ mav' : np.sum(era5_data['w500_hist']*abs(w500_bins_mid))/np.sum(era5_data['w500_hist'])})
#     era5_data_param.update({'Circ Mode' : w500_bins_mid[np.argmax(era5_data['w500_hist'])]})
#     jra55_data_param.update({'Circ Intensity' : (jra55_data['w500_hist']*w500_bins_mid)[w500_bins_mid > 0.].sum()/jra55_data['w500_hist'][w500_bins_mid > 0].sum()-(jra55_data['w500_hist']*w500_bins_mid)[w500_bins_mid < 0.].sum()/jra55_data['w500_hist'][w500_bins_mid < 0].sum()})
#     jra55_data_param.update({'Circ mav' : np.sum(jra55_data['w500_hist']*abs(w500_bins_mid))/np.sum(jra55_data['w500_hist'])})
#     jra55_data_param.update({'Circ Mode' : w500_bins_mid[np.argmax(jra55_data['w500_hist'])]})
#     merra2_data_param.update({'Circ Intensity' : (merra2_data['w500_hist']*w500_bins_mid)[w500_bins_mid > 0.].sum()/merra2_data['w500_hist'][w500_bins_mid > 0].sum()-(merra2_data['w500_hist']*w500_bins_mid)[w500_bins_mid < 0.].sum()/merra2_data['w500_hist'][w500_bins_mid < 0].sum()})
#     merra2_data_param.update({'Circ mav' : np.sum(merra2_data['w500_hist']*abs(w500_bins_mid))/np.sum(merra2_data['w500_hist'])})
#     merra2_data_param.update({'Circ Mode' : w500_bins_mid[np.argmax(merra2_data['w500_hist'])]})
#     for fit in ['Unconstrained', 'Afix', 'Constrained', 'D_0', 'D_mode', 'A']:
#         tot_data_param['SW'][fit]['bootstrap_param'] += merra2_data_param['SW'][fit]['bootstrap_param']
#         tot_data_param['SW'][fit]['bootstrap_param'] += jra55_data_param['SW'][fit]['bootstrap_param']
#         tot_data_param['SW'][fit]['bootstrap_param'] += era5_data_param['SW'][fit]['bootstrap_param']
#         tot_data_param['LW'][fit]['bootstrap_param'] += merra2_data_param['LW'][fit]['bootstrap_param']
#         tot_data_param['LW'][fit]['bootstrap_param'] += jra55_data_param['LW'][fit]['bootstrap_param']
#         tot_data_param['LW'][fit]['bootstrap_param'] += era5_data_param['LW'][fit]['bootstrap_param']
#     if rad_source == 'CERES_SYN': # Add calculated all-sky to bootstap estimates
#         for fit in ['Unconstrained', 'Afix', 'Constrained', 'D_0', 'D_mode', 'A']:
#             tot_data_param['SW'][fit]['bootstrap_param'] += merra2_data_param2['SW'][fit]['bootstrap_param']
#             tot_data_param['SW'][fit]['bootstrap_param'] += jra55_data_param2['SW'][fit]['bootstrap_param']
#             tot_data_param['SW'][fit]['bootstrap_param'] += era5_data_param2['SW'][fit]['bootstrap_param']
#             tot_data_param['SW'][fit]['bootstrap_param'] += tot_data_param2['SW'][fit]['bootstrap_param']
#             tot_data_param['LW'][fit]['bootstrap_param'] += merra2_data_param2['LW'][fit]['bootstrap_param']
#             tot_data_param['LW'][fit]['bootstrap_param'] += jra55_data_param2['LW'][fit]['bootstrap_param']
#             tot_data_param['LW'][fit]['bootstrap_param'] += era5_data_param2['LW'][fit]['bootstrap_param']
#             tot_data_param['LW'][fit]['bootstrap_param'] += tot_data_param2['LW'][fit]['bootstrap_param']
#     return tot_data_param, era5_data_param, jra55_data_param, merra2_data_param, tot_data


# def plot_cmip6_vs_reanalysis(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), yearlist=range(2001,2015), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30, experiment='AMIP', rad_source='CERES_SYN', show_plots=False):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     w500_bins_mid = 0.5*(w500_bins[:-1] + w500_bins[1:])
#     cre_bins_mid = 0.5*(cre_bins[:-1] + cre_bins[1:])
#     colorlist_cmip6=['r','g','b','c','m','y','orange']
#     w500_hist, w500_sw_cre_hist, w500_lw_cre_hist, sw_clr_sum, sw_cre_sum, sw_cre_sum_sq, sw_all_sum, lw_clr_sum, lw_cre_sum, lq_cre_sum_sq, lw_all_sum = get_cmip6_dist(spatial_av_scale=spatial_av_scale, w500_bins=w500_bins, lon_min=lon_min, lon_max=lon_max, experiment=experiment, yearlist=yearlist)
#     era5_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     obs_data = {}
#     obs_data_param, era5_data_param, jra55_data_param, merra2_data_param, obs_data_ann = combined_reanalysis_w500_cre_fit(era5_vs_ceres_two_deg_monthly['Ann'], merra2_vs_ceres_two_deg_monthly['Ann'], jra55_vs_ceres_two_deg_monthly['Ann'], w500_bins=w500_bins, cre_bins=cre_bins, spatial_av_scale=2.0, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, month='ANN', rad_source=rad_source)
#     obs_data.update({'Ann' : obs_data_ann})
#     amip_params = get_cmip6_param_data(spatial_av_scale=spatial_av_scale, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment=experiment, n_bootstrap=n_bootstrap) 
#     plt.close()
#     amip_params.update({'Obs' : {}})
#     amip_params['Obs'].update({'circ_intensity' : np.sum(obs_data['Ann']['w500_hist']*abs(w500_bins_mid))/np.sum(obs_data['Ann']['w500_hist'])})
#     amip_params['Obs'].update({'circ_mode' : w500_bins_mid[obs_data['Ann']['w500_hist'].argmax()]})
#     n_samples = int(((lat_max-lat_min)/spatial_av_scale)*((lon_max-lon_min)/spatial_av_scale)*(len(yearlist)*12*30*24/time_av_scale))
#     amip_params['Obs'] = bootstrap_sample_obs_intensity(amip_params['Obs'], w500_bins_mid, [obs_data, era5_vs_ceres_two_deg_monthly, merra2_vs_ceres_two_deg_monthly, jra55_vs_ceres_two_deg_monthly], n_samples, n_bootstrap=2)
#     amip_params['Obs'].update({'sw_cre_mean' : obs_data['Ann']['sw_cre_adj2_mean']})
#     amip_params['Obs'].update({'sw_cre_hist' : obs_data['Ann']['sw_cre_adj2_hist']})
#     amip_params['Obs'].update({'lw_cre_mean' : obs_data['Ann']['lw_cre_adj2_mean']})
#     amip_params['Obs'].update({'lw_cre_hist' : obs_data['Ann']['lw_cre_adj2_hist']})
# #   Calculate RMS error for mean for each datapoint.
#     for k in amip_params.keys():
#         w500_unbinned_ind_sw = (np.repeat(np.repeat(np.arange(w500_bins_mid.size),cre_bins_mid.size), amip_params[k]['sw_cre_hist'].astype(int).flatten()))
#         w500_unbinned_ind_lw = (np.repeat(np.repeat(np.arange(w500_bins_mid.size),cre_bins_mid.size), amip_params[k]['lw_cre_hist'].astype(int).flatten()))
#         sw_cre_unbinned = (np.repeat(np.repeat(cre_bins_mid[None,:],w500_bins_mid.size, axis=0).flatten(), amip_params[k]['sw_cre_hist'].astype(int).flatten()))
#         lw_cre_unbinned = (np.repeat(np.repeat(cre_bins_mid[None,:],w500_bins_mid.size, axis=0).flatten(), amip_params[k]['lw_cre_hist'].astype(int).flatten()))
#         sw_cre_mean_unbinned = amip_params[k]['sw_cre_mean'][w500_unbinned_ind_sw]
#         lw_cre_mean_unbinned = amip_params[k]['lw_cre_mean'][w500_unbinned_ind_lw]
#         amip_params[k].update({'sw_cre_mean_err' : np.sum((sw_cre_unbinned-sw_cre_mean_unbinned)**2)})
#         amip_params[k].update({'lw_cre_mean_err' : np.sum((lw_cre_unbinned-lw_cre_mean_unbinned)**2)})
#     print("obs_data.keys()=", obs_data.keys())
#     amip_params['Obs'].update({'SW' : obs_data_param['SW']})
#     amip_params['Obs'].update({'LW' : obs_data_param['LW']})
#     fig = plt.figure(2, figsize=(6.0,1.6))
#     ax = fig.add_subplot(121)
#     keylist = np.array([k for k in amip_params.keys()])
#     intensity = np.array([amip_params[k]['circ_intensity'] for k in keylist])
#     intensity_err = np.array([intensity - [np.nanmin(amip_params[k]['circ_intensity_bootstrap']) for k in keylist], [np.nanmax(amip_params[k]['circ_intensity_bootstrap'])for k in keylist] - intensity ])
#     keylist = keylist[intensity.argsort()]
#     intensity_err = (intensity_err.T[intensity.argsort()]).T
#     era5_ind = np.where(keylist == 'Obs')[0][0]
#     print('era5_ind=', era5_ind)
#     barlist = plt.bar(np.arange(len(amip_params.keys())), [amip_params[k]['circ_intensity'] for k in keylist], color='grey', yerr=intensity_err, capsize=3)
#     barlist[era5_ind].set_color('grey')
#     for i,k in enumerate(keylist):
#         barlist[i].set(hatch = cmip6_hatch_dict[k], color=cmip6_color_dict[k], fill=False)
#     barlist[era5_ind].set(color='grey', fill=True)
#     plt.ylabel('Circ Intensity\n(hPa day$^{-1}$)')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
#     plt.text(0.1, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     ax = fig.add_subplot(122)
#     mode = np.array([amip_params[k]['circ_mode'] for k in keylist])
#     mode_err = np.array([mode - [np.nanmin(amip_params[k]['circ_mode_bootstrap']) for k in keylist], [np.nanmax(amip_params[k]['circ_mode_bootstrap'])for k in keylist] - mode])
#     keylist = keylist[mode.argsort()]
#     era5_ind = np.where(keylist == 'Obs')[0][0]
#     print('era5_ind=', era5_ind)
#     barlist = plt.bar(np.arange(len(amip_params.keys())), [amip_params[k]['circ_mode'] for k in keylist], color='grey', yerr=mode_err, capsize=3)
#     barlist[era5_ind].set_color('grey')
#     for i,k in enumerate(keylist):
#         barlist[i].set(hatch = cmip6_hatch_dict[k], color=cmip6_color_dict[k], fill=False)
#     barlist[era5_ind].set(color='grey', fill=True)
#     plt.ylabel('Modal vertical velocity\n($\omega_{500}$, hPa day$^{-1}$)')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
#     plt.text(0.1, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     fig.tight_layout() # for poster
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+experiment+'_circ_vs_obs_'+rad_source+'_spat_av'+str(int(spatial_av_scale))+'_time_av'+str(int(time_av_scale))+'_lon'+str(lon_min)+'to'+str(lon_max)+'_year'+str(yearlist[0])+'to'+str(yearlist[-1])+'n_boot='+str(n_bootstrap)+plot_type, dpi=my_dpi)
#     if show_plots:
#         plt.show()
#     else:
#         plt.close('all')
#     fig = plt.figure(0, figsize=(6.1,4.8))
#     fit = 'A'
#     cmip6_era5_bar_plot_for_poster(fig, amip_params, fit, 'LW', keylist, cmip6_hatch_dict, cmip6_color_dict, n_bootstrap=n_bootstrap, rad_source=rad_source, experiment=experiment, show_plots=show_plots, yearlist=yearlist)
#     for fit in ['Unconstrained', 'Afix', 'Constrained', 'D_0', 'D_mode', 'A']:
#         fig = plt.figure(0, figsize=(6.4,9.6))
#         cmip6_era5_bar_plot(fig, amip_params, fit, 'SW', keylist, cmip6_hatch_dict, cmip6_color_dict, n_bootstrap=n_bootstrap, rad_source=rad_source, experiment=experiment, show_plots=show_plots, yearlist=yearlist)
#         fig = plt.figure(0, figsize=(6.4,9.6))
#         cmip6_era5_bar_plot(fig, amip_params, fit, 'LW', keylist, cmip6_hatch_dict, cmip6_color_dict, n_bootstrap=n_bootstrap, rad_source=rad_source, experiment=experiment, show_plots=show_plots, yearlist=yearlist)
#     return amip_params,obs_data_param, era5_data_param, jra55_data_param, merra2_data_param


# def bootstrap_sample_obs_intensity(obs_dict, w500_bins_mid, w500_data_list, n_samples, n_bootstrap=2, seed=1):
#     obs_dict.update({'circ_intensity_bootstrap'  : []})
#     obs_dict.update({'circ_mav_bootstrap'  : []})
#     obs_dict.update({'circ_mode_bootstrap'  : []})
#     for jj in range(n_bootstrap):
#         for w500_data in w500_data_list:
#             seed = seed + jj
#             rng = Generator(PCG64(seed))
#             samples = rng.choice(w500_bins_mid, n_samples, p=w500_data['Ann']['w500_hist']/w500_data['Ann']['w500_hist'].sum())            
#             obs_dict['circ_intensity_bootstrap'] += [np.mean(samples[samples >=0.])-np.mean(samples[samples < 0.])]
#             obs_dict['circ_mav_bootstrap'] += [np.mean(abs(samples))]
#             obs_dict['circ_mode_bootstrap'] += [stats_mode(samples)[0][0]]
#     return obs_dict


# def get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, experiment='AMIP', n_bootstrap=2, seed=1, time_av_scale=720, yearlist=range(2001,2015), fit_param=True):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     w500_bins_mid = 0.5*(w500_bins[:-1] + w500_bins[1:])
#     w500_hist, w500_sw_cre_hist, w500_lw_cre_hist, sw_clr_sum, sw_cre_sum, sw_cre_sum_sq, sw_all_sum, lw_clr_sum, lw_cre_sum, lq_cre_sum_sq, lw_all_sum = get_cmip6_dist(spatial_av_scale=spatial_av_scale, w500_bins=w500_bins, lon_min=lon_min, lon_max=lon_max, experiment=experiment, cre_bins=cre_bins, yearlist=yearlist)
#     amip_params = {}
#     n_samples = int(((lat_max-lat_min)/spatial_av_scale)*((lon_max-lon_min)/spatial_av_scale)*(len(yearlist)*12*30*24/time_av_scale))
#     for k in w500_hist.keys():
# #    for k in ['GFDL-AM4','GFDL-CM4','SAM0-UNICON']:
#         print('k=', k)
#         amip_params.update({k : {}})
#         amip_params[k].update({'circ_intensity' : (w500_hist[k]*w500_bins_mid)[w500_bins_mid > 0.].sum()/w500_hist[k][w500_bins_mid > 0].sum()-(w500_hist[k]*w500_bins_mid)[w500_bins_mid < 0.].sum()/w500_hist[k][w500_bins_mid < 0].sum()})
#         amip_params[k].update({'circ_mav' : np.sum(w500_hist[k]*abs(w500_bins_mid))/np.sum(w500_hist[k])})
#         amip_params[k].update({'w500_hist' : w500_hist[k]})
#         amip_params[k].update({'circ_intensity_bootstrap'  : []})
#         amip_params[k].update({'circ_mav_bootstrap'  : []})
#         amip_params[k].update({'circ_mode' : w500_bins_mid[w500_hist[k].argmax()]})
#         amip_params[k].update({'circ_mode_bootstrap'  : []})
#         for jj in range(n_bootstrap):
#             seed = seed + jj
#             rng = Generator(PCG64(seed))
#             samples = rng.choice(w500_bins_mid, n_samples, p=w500_hist[k]/w500_hist[k].sum())            
#             amip_params[k]['circ_intensity_bootstrap'] += [np.mean(samples[samples >= 0.])-np.mean(samples[samples < 0.])]
#             amip_params[k]['circ_mav_bootstrap'] += [np.mean(abs(samples))]
#             amip_params[k]['circ_mode_bootstrap'] += [stats_mode(samples)[0][0]]
#         amip_params[k].update({'sw_cre_mean' : sw_cre_sum[k] / w500_hist[k]})
#         amip_params[k].update({'lw_cre_mean' : lw_cre_sum[k] / w500_hist[k]})
#         amip_params[k].update({'sw_cre_hist' : w500_sw_cre_hist[k]})
#         amip_params[k].update({'lw_cre_hist' : w500_lw_cre_hist[k]})
#         if fit_param:
#             tot_data_param = fit_w500_cre_exp_flat2(amip_params[k], w500_bins, cre_bins, w500_source=k, rad_source=k+'_ANN_'+experiment, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, n_bootstrap=n_bootstrap, yearlist=yearlist, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#             for kk in tot_data_param.keys():
#                 amip_params[k].update({kk : tot_data_param[kk]})
#     return amip_params


# def plot_rce_vs_reanalysis(w500_bins=np.arange(-700,700.01,2), yearlist=range(2001,2021), rce_list=['/gws/nopw/j04/circulates_vol2/PHill/UM_data/RCEMIP/RCE_large300_fixrhcrit_L98/', '/gws/nopw/j04/circulates_vol2/PHill/UM_data/RCEMIP/RCE_large_hadley_fixrhcrit_L98/', '/gws/nopw/j04/circulates_vol2/PHill/UM_data/RCEMIP/RCE_large_hadley_steep/'], label_list=['Fixed SST', 'SST gradient', 'Steeper SST gradient']):
#     w500_bins_mid = 0.5*(w500_bins[:-1] + w500_bins[1:])
#     print('w500_bins_mid', w500_bins_mid)
#     era5_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_SYN', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=24, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, yearlist=yearlist)
#     print("era5_vs_ceres_two_deg_monthly['Ann']['w500_hist'].size=", era5_vs_ceres_two_deg_monthly['Ann']['w500_hist'].size)
#     print("era5_vs_ceres_two_deg_monthly['Ann']['sw_cre_mean'].size=", era5_vs_ceres_two_deg_monthly['Ann']['sw_cre_mean'].size)
#     fig = plt.figure(0)
#     plt.plot(w500_bins_mid, era5_vs_ceres_two_deg_monthly['Ann']['sw_cre_mean'], 'k', label='Era5')
#     fig = plt.figure(1)
#     plt.plot(w500_bins_mid, era5_vs_ceres_two_deg_monthly['Ann']['lw_cre_mean'], 'k', label='Era5')
#     fig = plt.figure(2)
#     plt.plot(w500_bins_mid, era5_vs_ceres_two_deg_monthly['Ann']['w500_hist']/era5_vs_ceres_two_deg_monthly['Ann']['w500_hist'].sum(), 'k', label='Era5'+' {:.2f}'.format(np.sum(era5_vs_ceres_two_deg_monthly['Ann']['w500_hist']*abs(w500_bins_mid))/np.sum(era5_vs_ceres_two_deg_monthly['Ann']['w500_hist'])))
#     for model_dir, label  in zip(rce_list, label_list):
#         sw_cre_hist_two_deg_monthly, lw_cre_hist_two_deg_monthly, w500_hist_two_deg_monthly = get_rce_cre_data(model_dir, spatial_av_scale=72, start_day=50, end_day=200, n_hours=24)
#         fig = plt.figure(0)
#         print('w500_bins_mid', w500_bins_mid)
#         print('sw_cre_hist_two_deg_monthly.size=', sw_cre_hist_two_deg_monthly.size)
# #        return w500_hist_two_deg_monthly
#         print('w500_hist_two_deg_monthly[0].size=', w500_hist_two_deg_monthly[0].size)
#         plt.plot(w500_bins_mid, sw_cre_hist_two_deg_monthly, label=label+' {:.2f}'.format((np.nansum(sw_cre_hist_two_deg_monthly*w500_hist_two_deg_monthly[0]))/np.nansum(w500_hist_two_deg_monthly[0])))
#         print(model_dir, ' mean SW =', (np.nansum(sw_cre_hist_two_deg_monthly*w500_hist_two_deg_monthly[0]))/np.nansum(w500_hist_two_deg_monthly[0]))
#         fig = plt.figure(1)
#         plt.plot(w500_bins_mid, lw_cre_hist_two_deg_monthly, label=label+' {:.2f}'.format((np.nansum(lw_cre_hist_two_deg_monthly*w500_hist_two_deg_monthly[0]))/np.nansum(w500_hist_two_deg_monthly[0])))
#         print(model_dir, ' mean LW =', (np.nansum(lw_cre_hist_two_deg_monthly*w500_hist_two_deg_monthly[0]))/np.nansum(w500_hist_two_deg_monthly[0]))
#         fig = plt.figure(2)
#         plt.plot(w500_bins_mid, w500_hist_two_deg_monthly[0]/w500_hist_two_deg_monthly[0].sum(), label=label+' {:.2f}'.format(np.sum(w500_hist_two_deg_monthly[0]*abs(w500_bins_mid))/np.sum(w500_hist_two_deg_monthly[0])))
#     fig = plt.figure(0)
#     plt.legend(loc=0)
#     plt.xlabel('Circulation Regime ($\omega_{500}$, hPa day$^{-1}$)')
#     plt.ylabel('TOA SW CRE (W m$^{-2}$)')
# #    plt.gca().set_ylim(bottom=0)
#     plt.xlim([-300.,300.])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/rce_vs_ERA5_sw_cre'+plot_type, dpi=my_dpi)
#     fig = plt.figure(1)
#     plt.legend(loc=0)
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.ylabel('TOA LW CRE (W m$^{-2}$)')
# #    plt.gca().set_ylim(bottom=0)
#     plt.xlim([-300.,300.])
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/rce_vs_ERA5_lw_cre'+plot_type, dpi=my_dpi)
#     fig = plt.figure(2)
#     plt.legend(loc=0)
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.ylabel('Probability Density')
#     plt.gca().set_ylim(bottom=0)
#     plt.xlim([-300.,300.])
#     fig.tight_layout()
#     plt.grid(color='lightgrey')
#     plt.savefig('/home/users/phill/images/CIRCULATES/rce_vs_ERA5_w500_dist'+plot_type, dpi=my_dpi)
#     plt.show()



# def cmip6_dynamic_feedback(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), yearlist=range(2001,2015), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30, rad_source='CERES_EBAF', fit='A'):
#     '''
#     Analyse how feedback and dynamic feedback in CMIP6 relates to ability to
#     reproduce circulation and cloud circulation relationships
#     '''
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
# #   1) Compare parameters for 3 different simulation types
#     amip_params,obs_data_param, era5_data_param, jra55_data_param, merra2_data_param = plot_cmip6_vs_reanalysis(w500_bins=w500_bins, cre_bins=cre_bins, yearlist=yearlist, n_bootstrap=n_bootstrap, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, seed=seed, spatial_av_scale=spatial_av_scale, time_av_scale=time_av_scale, experiment='AMIP', rad_source=rad_source)
#     PiControl_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, experiment='PiControl', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=yearlist)
#     abrupt4CO2_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, experiment='abrupt4CO2', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=yearlist)
#     return PiControl_params, abrupt4CO2_params, amip_params,obs_data_param, era5_data_param, jra55_data_param, merra2_data_param
#     complete_model_list = []
#     for model in amip_params.keys():
#         if ((model in PiControl_params.keys()) & (model in abrupt4CO2_params.keys())):
#             complete_model_list += [model]
#     for region in ['SW', 'LW']:
#         ax = fig.add_subplot(511)
#         maxval_cre = np.array([[amip_params[k][region][fit]['param'][0], PiControl_params[k][region][fit]['param'][0], abrupt4CO2_params[k][region][fit]['param'][0]] for k in complete_model_list])
# #        maxval_cre_err = np.array([maxval_cre - np.array([np.nanmin([pp[0] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]), np.array([np.nanmax([pp[0] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]) - maxval_cre])
#         maxval_cre_ord = maxval_cre.argsort()
#         complete_model_list = complete_model_list[maxval_cre_ord]
#         maxval_cre = maxval_cre[maxval_cre_ord]
#         maxval_cre_err = (maxval_cre_err.T[maxval_cre_ord]).T
# #    barlist = plt.bar(np.arange(len(amip_params.keys())), maxval_cre, color='grey')
# #    barlist = plt.bar(np.arange(len(amip_params.keys())), [amip_params[k][region][fit]['param'][0] for k in complete_model_list], color='grey', yerr=maxval_cre_err)
#     barlist = plt.bar(np.arange(len(amip_params.keys())), maxval_cre, color='grey', yerr=maxval_cre_err, capsize=3)
#     plt.show()
#     for i,k in enumerate(complete_model_list):
#         barlist[i].set(hatch = hatch_dict[k], color=color_dict[k], fill=False)
#     plt.ylabel(region+' CRE "A"\n(W m$^{-2}$')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
#     ax = fig.add_subplot(512)
#     maxval_cre = np.array([amip_params[k][region][fit]['param'][1] for k in complete_model_list])
#     maxval_cre_err = np.array([maxval_cre - np.array([np.nanmin([pp[1] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]), np.array([np.nanmax([pp[1] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]) - maxval_cre])
#     maxval_cre_ord = maxval_cre.argsort()
#     complete_model_list = complete_model_list[maxval_cre_ord]
#     maxval_cre = maxval_cre[maxval_cre_ord]
#     maxval_cre_err = (maxval_cre_err.T[maxval_cre_ord]).T
#     era5_ind = np.where(complete_model_list == 'Obs')[0][0]
#     barlist = plt.bar(np.arange(len(amip_params.keys())), maxval_cre, color='grey', yerr=maxval_cre_err, capsize=3)
#     for i,k in enumerate(complete_model_list):
#         barlist[i].set(hatch = hatch_dict[k], color=color_dict[k], fill=False)
#     barlist[era5_ind].set(color='grey', fill=True)
#     plt.ylabel(region+' CRE "B"\n(W m$^{-2}$')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
#     ax = fig.add_subplot(513)
#     maxval_cre = np.array([amip_params[k][region][fit]['param'][2] for k in complete_model_list])
#     maxval_cre_err = np.array([maxval_cre - np.array([np.nanmin([pp[2] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]), np.array([np.nanmax([pp[2] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]) - maxval_cre])
#     maxval_cre_ord = maxval_cre.argsort()
#     complete_model_list = complete_model_list[maxval_cre_ord]
#     maxval_cre = maxval_cre[maxval_cre_ord]
#     maxval_cre_err = (maxval_cre_err.T[maxval_cre_ord]).T
#     era5_ind = np.where(complete_model_list == 'Obs')[0][0]
#     barlist = plt.bar(np.arange(len(amip_params.keys())), maxval_cre, color='grey', yerr=maxval_cre_err, capsize=3)
#     for i,k in enumerate(complete_model_list):
#         barlist[i].set(hatch = hatch_dict[k], color=color_dict[k], fill=False)
#     barlist[era5_ind].set(color='grey', fill=True)
#     plt.ylabel(region+' CRE "C"\n(day hPa$^{-1}$)')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
# #   Add legend here as middle subplot
#     fig.subplots_adjust(right=0.65)
#     patches = [Patch(facecolor='white', edgecolor=color_dict[k], label=k, hatch=hatch_dict[k]) for i,k in enumerate([k for k in sorted(amip_params.keys()) if k != 'Obs'])]
#     patches += [Patch(facecolor='grey', label='Obs')]
# # add the legend
#     leg = plt.legend(handles=patches, bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0, frameon=False, labelspacing=2)
#     for patch in leg.get_patches():
#         patch.set_height(22)
# #   Finished adding legend
#     ax = fig.add_subplot(514)
#     maxval_cre = np.array([amip_params[k][region][fit]['param'][3] for k in complete_model_list])
#     maxval_cre_err = np.array([maxval_cre - np.array([np.nanmin([pp[3] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]), np.array([np.nanmax([pp[3] for pp in amip_params[k][region][fit]['bootstrap_param']]) for k in complete_model_list]) - maxval_cre])
#     maxval_cre_ord = maxval_cre.argsort()
#     complete_model_list = complete_model_list[maxval_cre_ord]
#     maxval_cre = maxval_cre[maxval_cre_ord]
#     maxval_cre_err = (maxval_cre_err.T[maxval_cre_ord]).T
#     era5_ind = np.where(complete_model_list == 'Obs')[0][0]
#     barlist = plt.bar(np.arange(len(amip_params.keys())), maxval_cre, color='grey', yerr=maxval_cre_err, capsize=3)
#     for i,k in enumerate(complete_model_list):
#         barlist[i].set(hatch = hatch_dict[k], color=color_dict[k], fill=False)
#     barlist[era5_ind].set(color='grey', fill=True)
#     plt.ylabel(region+' CRE "D"\n(hPa day$^{-1}$)')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
#     ax = fig.add_subplot(515)
#     err_val = 100.*(np.array([amip_params[k][region][fit]['tot_err']/amip_params[k][region.lower()+'_cre_mean_err'] for k in complete_model_list])-1)
# #    err_val_err = np.array([np.percentile([pp/amip_params[k][region.lower()+'_cre_mean_err'] for pp in amip_params[k][region][fit]['bootstrap_tot_err']], (2.5, 97.5)) for k in complete_model_list]).T - maxval_cre
#     print('region=', region)
#     print('fit=', fit)
#     print("amip_params['Obs'][region][fit]['tot_err']=", amip_params['Obs'][region][fit]['tot_err'])
#     print("amip_params['Obs'][region.lower()+'_cre_mean_err']=", amip_params['Obs'][region.lower()+'_cre_mean_err'])
#     err_val_ord = err_val.argsort()
#     complete_model_list = complete_model_list[err_val_ord]
#     err_val = err_val[err_val_ord]
# #    err_val_err = (err_val_err.T[err_val_ord]).T
#     era5_ind = np.where(complete_model_list == 'Obs')[0][0]
# #    barlist = plt.bar(np.arange(len(amip_params.keys())), err_val, color='grey', yerr=err_val_err, capsize=3)
#     barlist = plt.bar(np.arange(len(amip_params.keys())), err_val, color='grey')
#     print('era5_ind=', era5_ind)
#     print('err_val=', err_val)
#     for i,k in enumerate(complete_model_list):
#         barlist[i].set(hatch = hatch_dict[k], color=color_dict[k], fill=False)
#     barlist[era5_ind].set(color='grey', fill=True)
#     plt.ylabel('Relative change in\n'+region+' CRE fit RMS error\n(%)')
#     plt.grid(axis='y')
#     plt.tick_params(top=False, bottom=False, left=True, right=False,
#                 labelleft=True, labelbottom=False)
# #    plt.show()
# # create the rectangles for the legend
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+region+'_'+experiment+'_vs_obs_'+rad_source+'_params_'+fit+'_spat_av'+str(int(spatial_av_scale))+'_time_av'+str(int(time_av_scale))+'_lon'+str(lon_min)+'to'+str(lon_max)+'_year'+str(yearlist[0])+'to'+str(yearlist[-1])+plot_type, dpi=my_dpi)
#     if show_plots:
#         plt.show()
#     else:
#         plt.close('all')


# def calc_feedbacks(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), yearlist=range(2001,2015), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30, rad_source='CERES_EBAF', fit='A'):
#     '''
#     Calculates feedbacks and components of feedback

#     Method: first 150 years each of abrupt4CO2 and piControl.
#     Feedback is calculated using Gregory method, using annual abrupt4xCO2
#     anomalies of regional mean TOA rad versus (where anomaly is wrt 150 year
#     regional mean TOA rad from picontrol) versus global mean surface
#     temperarure anomaly (again wrt 150 year mean from pi control)
#     '''
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
#     complete_model_list = []
#     quad_co2_forcing, all_sky_feedback, net_cre_dynamic, net_cre_thermodynamic, net_cre_co_variation,sw_cre_dynamic, sw_cre_thermodynamic, sw_cre_co_variation, lw_cre_dynamic, lw_cre_thermodynamic, lw_cre_co_variation, net_cre_dynamic_param, net_cre_thermodynamic_param, net_cre_co_variation_param,sw_cre_dynamic_param, sw_cre_thermodynamic_param, sw_cre_co_variation_param, lw_cre_dynamic_param, lw_cre_thermodynamic_param, lw_cre_co_variation_param, net_cre_dynamic_obs, net_cre_thermodynamic_obs, net_cre_co_variation_obs,sw_cre_dynamic_obs, sw_cre_thermodynamic_obs, sw_cre_co_variation_obs, lw_cre_dynamic_obs, lw_cre_thermodynamic_obs, lw_cre_co_variation_obs, net_cre_dynamic_feedback, net_cre_thermodynamic_feedback, net_cre_co_variation_feedback,sw_cre_dynamic_feedback, sw_cre_thermodynamic_feedback, sw_cre_co_variation_feedback, lw_cre_dynamic_feedback, lw_cre_thermodynamic_feedback, lw_cre_co_variation_feedback, net_cre_dynamic_param_feedback, net_cre_thermodynamic_param_feedback, net_cre_co_variation_param_feedback,sw_cre_dynamic_param_feedback, sw_cre_thermodynamic_param_feedback, sw_cre_co_variation_param_feedback, lw_cre_dynamic_param_feedback, lw_cre_thermodynamic_param_feedback, lw_cre_co_variation_param_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_obs_feedback,sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_obs_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_obs_feedback = ({} for __ in range(56))
# #   Get observed data
#     era5_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     obs_data = {}
#     obs_data_param, era5_data_param, jra55_data_param, merra2_data_param, obs_data_ann = combined_reanalysis_w500_cre_fit(era5_vs_ceres_two_deg_monthly['Ann'], merra2_vs_ceres_two_deg_monthly['Ann'], jra55_vs_ceres_two_deg_monthly['Ann'], w500_bins=w500_bins, cre_bins=cre_bins, spatial_av_scale=2.0, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, month='ANN', rad_source=rad_source)
#     obs_data.update({'Ann' : obs_data_ann})
# #   ADJ2 values are consistent with model definition of CRE, so use these instead.
#     obs_data['Ann']['sw_cre_mean'] = obs_data['Ann']['sw_cre_adj2_mean']
#     obs_data['Ann']['sw_cre_hist'] = obs_data['Ann']['sw_cre_adj2_hist']
#     obs_data['Ann']['lw_cre_mean'] = obs_data['Ann']['lw_cre_adj2_mean']
#     obs_data['Ann']['lw_cre_hist'] = obs_data['Ann']['lw_cre_adj2_hist']
# #   Get fits, which we use to compare whether they change with time period and model version and whether the fit is good enough to use instead of data
#     n_samples = int(((lat_max-lat_min)/spatial_av_scale)*((lon_max-lon_min)/spatial_av_scale)*(len(yearlist)*12*30*24/time_av_scale))
#     obs_data_param = bootstrap_sample_obs_intensity(obs_data_param, w500_bins_mid, [obs_data, era5_vs_ceres_two_deg_monthly, merra2_vs_ceres_two_deg_monthly, jra55_vs_ceres_two_deg_monthly], n_samples, n_bootstrap=n_bootstrap, seed=seed)
#     AMIP_params_ceres_era = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=np.arange(-400,400.01,0.2), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=yearlist)
#     AMIP_params_long = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=np.arange(-400,400.01,0.2), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(1979,2015))
#     PiControl_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=np.arange(-400,400.01,0.2), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='PiControl', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(0,150))
#     abrupt4CO2_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=np.arange(-400,400.01,0.2), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='abrupt4CO2', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(0,150))
#     for model in picontrol_dict.keys():
#         if ((model in abrupt4co2_dict.keys()) & (model in amip_p4k_dict.keys())):
#             complete_model_list += [model]
#     complete_model_list.sort()
# #    return complete_model_list, AMIP_params_ceres_era, AMIP_params_long, PiControl_params, abrupt4CO2_params, obs_data_param, obs_data
# #   First compare data across scenarios and averaging period.
#     plot_scenario_comparison(complete_model_list, [AMIP_params_ceres_era, AMIP_params_long, PiControl_params, abrupt4CO2_params], obs_data_param, var='circ_intensity', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_scenario_comparison(complete_model_list, [AMIP_params_ceres_era, AMIP_params_long, PiControl_params, abrupt4CO2_params], obs_data_param, var='circ_mode', ylabel='Modal vertical velocity (hPa day$^{-1}$)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     for region in ['SW', 'LW']:
#         for param in ['A', 'B', 'C', 'D']:
#             plot_scenario_comparison(complete_model_list, [AMIP_params_ceres_era, AMIP_params_long, PiControl_params, abrupt4CO2_params], obs_data_param, var=param, region=region, ylabel=region+' CRE vs w500 fit, '+param, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
# #   Now do plot for each model.
#     for model in complete_model_list:
# #       Plot vs observations
#         fig = plt.figure(0)
#         plt.plot(w500_bins_mid,obs_data['Ann']['w500_hist'], 'k')
#         plt.plot(w500_bins_mid,AMIP_params_ceres_era[model]['w500_hist'])
#         plt.plot(w500_bins_mid,AMIP_params_long[model]['w500_hist'])
#         plt.plot(w500_bins_mid,PiControl_params[model]['w500_hist'])
#         plt.plot(w500_bins_mid,abrupt4CO2_params[model]['w500_hist'])
#         plt.ylabel('Frequency')
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.savefig('/home/users/phill/images/CIRCULATES/w500_dist_'+model+'vs_obs'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_'+plot_type)
#         plt.clf()
# #   Now calculate feedbacks and sensitivities
# #   First get 150 year means from piControl (global mean SST, regional mean TOA rad as function of w500 and regional mean w500 distribution)
#     picontrol_global_mean_ts, picontrol_regional_mean_sw_all, picontrol_regional_mean_sw_clr, picontrol_regional_mean_lw_all, picontrol_regional_mean_lw_clr, picontrol_w500_hist, picontrol_w500_sw_cre_hist, picontrol_w500_lw_cre_hist, picontrol_sw_clr_sum, picontrol_sw_cre_sum, picontrol_sw_cre_sum_sq, picontrol_sw_all_sum, picontrol_lw_clr_sum, picontrol_lw_cre_sum, picontrol_lw_cre_sum_sq, picontrol_lw_all_sum = get_picontrol_data(w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, model_list=complete_model_list)
# #   Now get these for each year in abrupt4xCO2
#     abrupt4co2_global_mean_ts,abrupt4co2_regional_mean_sw_all,abrupt4co2_regional_mean_sw_clr,abrupt4co2_regional_mean_lw_all,abrupt4co2_regional_mean_lw_clr,abrupt4co2_regional_mean_sw_cre,abrupt4co2_regional_mean_lw_cre,abrupt4co2_regional_mean_w500_dist,abrupt4co2_regional_mean_olr_vs_w500_dist,abrupt4co2_regional_mean_lw_cre_vs_w500_dist,abrupt4co2_regional_mean_osr_vs_w500_dist,abrupt4co2_regional_mean_sw_cre_vs_w500_dist = get_abrupt4co2_data(w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, model_list=complete_model_list)
# #   Calculate radiative response following BYrne & Schneider 2018.
# #   This requires CO2 forcing, which we get using Gregory method 
#     for model in complete_model_list:
#         print('model=', model)
#         print('picontrol_global_mean_ts[model].shape=', picontrol_global_mean_ts[model].shape)
#         print('picontrol_regional_mean_sw_all[model].shape=', picontrol_regional_mean_sw_all[model].shape)
#         print('abrupt4co2_global_mean_ts[model].shape=', abrupt4co2_global_mean_ts[model].shape)
#         print('abrupt4co2_regional_mean_sw_all[model].shape=', abrupt4co2_regional_mean_sw_all[model].shape)
#         global_mean_ts_anomaly = abrupt4co2_global_mean_ts[model] - picontrol_global_mean_ts[model]
#         regional_mean_net_rad_anomaly = (picontrol_regional_mean_sw_all[model] - abrupt4co2_regional_mean_sw_all[model]) + (picontrol_regional_mean_lw_all[model] - abrupt4co2_regional_mean_lw_all[model]) # positve downwards so take negative of upwards terms (downwards terms don;t change)
#         print('global_mean_ts_anomaly=', global_mean_ts_anomaly)
#         print('regional_mean_net_rad_anomaly', regional_mean_net_rad_anomaly)
#         print('global_mean_ts_anomaly.shape=', global_mean_ts_anomaly.shape)
#         print('regional_mean_net_rad_anomaly.shape', regional_mean_net_rad_anomaly.shape)
#         fit = np.polyfit(global_mean_ts_anomaly, regional_mean_net_rad_anomaly, 1)
# #       bootstrap_fit = # Can used bootstrapping to get uncertainty on fit (cf Andrews 20xx)
#         quad_co2_forcing.update({model : fit[1]})
#         all_sky_feedback.update({model : fit[0]})
#         for rad in [net_cre_dynamic, net_cre_thermodynamic, net_cre_co_variation,sw_cre_dynamic, sw_cre_thermodynamic, sw_cre_co_variation, lw_cre_dynamic, lw_cre_thermodynamic, lw_cre_co_variation, net_cre_dynamic_param, net_cre_thermodynamic_param, net_cre_co_variation_param, sw_cre_dynamic_param, sw_cre_thermodynamic_param, sw_cre_co_variation_param, lw_cre_dynamic_param, lw_cre_thermodynamic_param, lw_cre_co_variation_param, net_cre_dynamic_obs, net_cre_thermodynamic_obs, net_cre_co_variation_obs, sw_cre_dynamic_obs, sw_cre_thermodynamic_obs, sw_cre_co_variation_obs, lw_cre_dynamic_obs, lw_cre_thermodynamic_obs, lw_cre_co_variation_obs]:
#             rad.update({model : []})
#         delta_rad = regional_mean_net_rad_anomaly.mean()
#         for yy in range(150):
#             print('model=', model)
#             print('((picontrol_sw_cre_sum[model]+picontrol_lw_cre_sum[model])/picontrol_w500_hist[model]).shape=', ((picontrol_sw_cre_sum[model]+picontrol_lw_cre_sum[model])/picontrol_w500_hist[model]).shape)
#             print('((abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]+abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:])/abrupt4co2_regional_mean_w500_dist[model][yy,:]).shape=', ((abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]+abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:])/abrupt4co2_regional_mean_w500_dist[model][yy,:]).shape)
#             print('(picontrol_w500_hist[model]/picontrol_w500_hist[model].sum()).shape=', (picontrol_w500_hist[model]/picontrol_w500_hist[model].sum()).shape)
#             print('(abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum()).shape=',(abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum()).shape) 
#             A,B,C= decompose_rad((picontrol_sw_cre_sum[model]+picontrol_lw_cre_sum[model])/picontrol_w500_hist[model], (abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]+abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:])/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum()) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             net_cre_dynamic[model] += [A]
#             net_cre_thermodynamic[model] += [B]
#             net_cre_co_variation[model] += [C]
#             A,B,C = decompose_rad(picontrol_sw_cre_sum[model]/picontrol_w500_hist[model], abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum()) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             sw_cre_dynamic[model] += [A]
#             sw_cre_thermodynamic[model] += [B]
#             sw_cre_co_variation[model] += [C]
#             A, B, C = decompose_rad(picontrol_lw_cre_sum[model]/picontrol_w500_hist[model], abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum()) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             lw_cre_dynamic[model] += [A]
#             lw_cre_thermodynamic[model] += [B]
#             lw_cre_co_variation[model] += [C]
# #        fig = plt.figure(0)
# #        ax = fig.add_subplot(311)
# #        plt.bar()
#             A, B, C= decompose_rad((picontrol_sw_cre_sum[model]+picontrol_lw_cre_sum[model])/picontrol_w500_hist[model], (abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]+abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:])/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum(), fixed_rad_hist=neg_exp_func_full2(w500_bins_mid, PiControl_params[model]['LW']['A']['param'][0], PiControl_params[model]['LW']['A']['param'][1], PiControl_params[model]['LW']['A']['param'][2], PiControl_params[model]['LW']['A']['param'][3])+neg_exp_func_full2(w500_bins_mid, PiControl_params[model]['SW']['A']['param'][0], PiControl_params[model]['SW']['A']['param'][1], PiControl_params[model]['SW']['A']['param'][2], PiControl_params[model]['SW']['A']['param'][3])) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             net_cre_dynamic_param[model] += [A]
#             net_cre_thermodynamic_param[model] += [B]
#             net_cre_co_variation_param[model] += [C]
#             A,B,C = decompose_rad(picontrol_sw_cre_sum[model]/picontrol_w500_hist[model], abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum(), fixed_rad_hist=neg_exp_func_full2(w500_bins_mid, PiControl_params[model]['SW']['A']['param'][0], PiControl_params[model]['SW']['A']['param'][1], PiControl_params[model]['SW']['A']['param'][2], PiControl_params[model]['SW']['A']['param'][3])) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             sw_cre_dynamic_param[model]+= [A]
#             sw_cre_thermodynamic_param[model] += [B]
#             sw_cre_co_variation_param[model] += [C]
#             A, B, C = decompose_rad(picontrol_lw_cre_sum[model]/picontrol_w500_hist[model], abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum(), fixed_rad_hist=neg_exp_func_full2(w500_bins_mid, PiControl_params[model]['LW']['A']['param'][0], PiControl_params[model]['LW']['A']['param'][1], PiControl_params[model]['LW']['A']['param'][2], PiControl_params[model]['LW']['A']['param'][3])) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             lw_cre_dynamic_param[model] += [A]
#             lw_cre_thermodynamic_param[model] += [B]
#             lw_cre_co_variation_param[model] += [C]
#             A, B, C = decompose_rad((picontrol_sw_cre_sum[model]+picontrol_lw_cre_sum[model])/picontrol_w500_hist[model], (abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]+abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:])/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum(), fixed_w500_hist=obs_data_ann['w500_hist']/obs_data_ann['w500_hist'].sum(), fixed_rad_hist=(obs_data_ann['sw_cre_sum']+obs_data_ann['lw_cre_sum'])/obs_data_ann['w500_hist']) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             print('A=', A)
#             net_cre_dynamic_obs[model] += [A]
#             print("net_cre_dynamic_obs[model]=", net_cre_dynamic_obs[model])
#             net_cre_thermodynamic_obs[model] += [B]
#             net_cre_co_variation_obs[model] += [C]
#             A, B, C = decompose_rad(picontrol_sw_cre_sum[model]/picontrol_w500_hist[model], abrupt4co2_regional_mean_sw_cre_vs_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum(), fixed_w500_hist=obs_data_ann['w500_hist']/obs_data_ann['w500_hist'].sum(), fixed_rad_hist=obs_data_ann['sw_cre_sum']/obs_data_ann['w500_hist']) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             print('A=', A)
#             sw_cre_dynamic_obs[model] += [A]
#             print("sw_cre_dynamic_obs[model]=", sw_cre_dynamic_obs[model])
#             sw_cre_thermodynamic_obs[model] += [B]
#             sw_cre_co_variation_obs[model] += [C]
#             A, B, C = decompose_rad(picontrol_lw_cre_sum[model]/picontrol_w500_hist[model], abrupt4co2_regional_mean_lw_cre_vs_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:], picontrol_w500_hist[model]/picontrol_w500_hist[model].sum(), abrupt4co2_regional_mean_w500_dist[model][yy,:]/abrupt4co2_regional_mean_w500_dist[model][yy,:].sum(), fixed_w500_hist=obs_data_ann['w500_hist']/obs_data_ann['w500_hist'].sum(), fixed_rad_hist=obs_data_ann['lw_cre_sum']/obs_data_ann['w500_hist']) # Byrne and Schneider seem to suggest doing this on a year by year basis?
#             lw_cre_dynamic_obs[model] += [A]
#             lw_cre_thermodynamic_obs[model] += [B]
#             lw_cre_co_variation_obs[model] += [C]
#         lw_cre_dynamic_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_dynamic[model], 1)[0]})
#         lw_cre_thermodynamic_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_thermodynamic[model], 1)[0]})
#         lw_cre_co_variation_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_co_variation[model], 1)[0]})
#         lw_cre_dynamic_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_dynamic_param[model], 1)[0]})
#         lw_cre_thermodynamic_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_thermodynamic_param[model], 1)[0]})
#         lw_cre_co_variation_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_co_variation_param[model], 1)[0]})
#         lw_cre_dynamic_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_dynamic_obs[model], 1)[0]})
#         lw_cre_thermodynamic_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_thermodynamic_obs[model], 1)[0]})
#         lw_cre_co_variation_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, lw_cre_co_variation_obs[model], 1)[0]})
#         sw_cre_dynamic_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_dynamic[model], 1)[0]})
#         sw_cre_thermodynamic_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_thermodynamic[model], 1)[0]})
#         sw_cre_co_variation_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_co_variation[model], 1)[0]})
#         sw_cre_dynamic_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_dynamic_param[model], 1)[0]})
#         sw_cre_thermodynamic_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_thermodynamic_param[model], 1)[0]})
#         sw_cre_co_variation_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_co_variation_param[model], 1)[0]})
#         sw_cre_dynamic_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_dynamic_obs[model], 1)[0]})
#         sw_cre_thermodynamic_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_thermodynamic_obs[model], 1)[0]})
#         sw_cre_co_variation_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, sw_cre_co_variation_obs[model], 1)[0]})
#         net_cre_dynamic_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_dynamic[model], 1)[0]})
#         net_cre_thermodynamic_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_thermodynamic[model], 1)[0]})
#         net_cre_co_variation_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_co_variation[model], 1)[0]})
#         net_cre_dynamic_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_dynamic_param[model], 1)[0]})
#         net_cre_thermodynamic_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_thermodynamic_param[model], 1)[0]})
#         net_cre_co_variation_param_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_co_variation_param[model], 1)[0]})
#         net_cre_dynamic_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_dynamic_obs[model], 1)[0]})
#         net_cre_thermodynamic_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_thermodynamic_obs[model], 1)[0]})
#         net_cre_co_variation_obs_feedback.update({model : np.polyfit(global_mean_ts_anomaly, net_cre_co_variation_obs[model], 1)[0]})
# #    Now compare feedbacks from model directly to feedbacks from fit for each model
#     mean_sw_cre_dynamic = {k : np.mean(sw_cre_dynamic[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_dynamic_param = {k : np.mean(sw_cre_dynamic_param[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_dynamic_obs = {k : np.mean(sw_cre_dynamic_obs[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_thermodynamic = {k : np.mean(sw_cre_thermodynamic[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_thermodynamic_param = {k : np.mean(sw_cre_thermodynamic_param[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_thermodynamic_obs = {k : np.mean(sw_cre_thermodynamic_obs[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_co_variation = {k : np.mean(sw_cre_co_variation[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_co_variation_param = {k : np.mean(sw_cre_co_variation_param[k]) for k in sw_cre_dynamic.keys()}
#     mean_sw_cre_co_variation_obs = {k : np.mean(sw_cre_co_variation_obs[k]) for k in sw_cre_dynamic.keys()}
#     mean_lw_cre_dynamic = {k : np.mean(lw_cre_dynamic[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_dynamic_param = {k : np.mean(lw_cre_dynamic_param[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_dynamic_obs = {k : np.mean(lw_cre_dynamic_obs[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_thermodynamic = {k : np.mean(lw_cre_thermodynamic[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_thermodynamic_param = {k : np.mean(lw_cre_thermodynamic_param[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_thermodynamic_obs = {k : np.mean(lw_cre_thermodynamic_obs[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_co_variation = {k : np.mean(lw_cre_co_variation[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_co_variation_param = {k : np.mean(lw_cre_co_variation_param[k]) for k in lw_cre_dynamic.keys()}
#     mean_lw_cre_co_variation_obs = {k : np.mean(lw_cre_co_variation_obs[k]) for k in lw_cre_dynamic.keys()}
#     mean_net_cre_dynamic = {k : np.mean(net_cre_dynamic[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_dynamic_param = {k : np.mean(net_cre_dynamic_param[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_dynamic_obs = {k : np.mean(net_cre_dynamic_obs[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_thermodynamic = {k : np.mean(net_cre_thermodynamic[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_thermodynamic_param = {k : np.mean(net_cre_thermodynamic_param[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_thermodynamic_obs = {k : np.mean(net_cre_thermodynamic_obs[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_co_variation = {k : np.mean(net_cre_co_variation[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_co_variation_param = {k : np.mean(net_cre_co_variation_param[k]) for k in net_cre_dynamic.keys()}
#     mean_net_cre_co_variation_obs = {k : np.mean(net_cre_co_variation_obs[k]) for k in net_cre_dynamic.keys()}
#     plot_decomposition_comparison(complete_model_list, mean_sw_cre_dynamic, mean_sw_cre_dynamic_param, mean_sw_cre_thermodynamic, mean_sw_cre_thermodynamic_param, mean_sw_cre_co_variation, mean_sw_cre_co_variation_param, ylabel='Delta SW cloud radiative effect (W m$^{-2}$)', savename='data_vs_param_decomposition_evalSW_cre_abrupt4CO2', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, mean_lw_cre_dynamic, mean_lw_cre_dynamic_param, mean_lw_cre_thermodynamic, mean_lw_cre_thermodynamic_param, mean_lw_cre_co_variation, mean_lw_cre_co_variation_param, ylabel='Delta LW cloud radiative effect (W m$^{-2}$)', savename='data_vs_param_decomposition_evalLW_cre_abrupt4CO2', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, mean_net_cre_dynamic, mean_net_cre_dynamic_param, mean_net_cre_thermodynamic, mean_net_cre_thermodynamic_param, mean_net_cre_co_variation, mean_net_cre_co_variation_param, ylabel='Delta Net cloud radiative effect (W m$^{-2}$)', savename='data_vs_param_decomposition_evalNet_cre_abrupt4CO2', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, mean_sw_cre_dynamic, mean_sw_cre_dynamic_obs, mean_sw_cre_thermodynamic, mean_sw_cre_thermodynamic_obs, mean_sw_cre_co_variation, mean_sw_cre_co_variation_obs, ylabel='Delta SW cloud radiative effect (W m$^{-2}$)', savename='obs_decomposition_evalSW_cre_abrupt4CO2', leg=['dynamic', 'dynamic obs', 'thermodynamic', 'thermodynamic obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison_v2(complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_feedback, title='SW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalSW_cre_feedback_abrupt4CO2', leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, mean_lw_cre_dynamic, mean_lw_cre_dynamic_obs, mean_lw_cre_thermodynamic, mean_lw_cre_thermodynamic_obs, mean_lw_cre_co_variation, mean_lw_cre_co_variation_obs, ylabel='Delta LW cloud radiative effect (W m$^{-2}$)', savename='obs_decomposition_evalLW_cre_abrupt4CO2', leg=['dynamic', 'dynamic obs', 'thermodynamic', 'thermodynamic obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison_v2(complete_model_list, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_feedback, title='LW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalLW_cre_feedback_abrupt4CO2', leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, mean_net_cre_dynamic, mean_net_cre_dynamic_obs, mean_net_cre_thermodynamic, mean_net_cre_thermodynamic_obs, mean_net_cre_co_variation, mean_net_cre_co_variation_obs, ylabel='Delta Net cloud radiative effect (W m$^{-2}$)', savename='obs_decomposition_evalNet_cre_abrupt4CO2', leg=['dynamic', 'dynamic obs', 'thermodynamic', 'thermodynamic obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison_v2(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_feedback, title='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalNet_cre_feedback_abrupt4CO2', leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_feedback, ylabel='SW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalSW_cre_feedback_abrupt4CO2', leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_feedback, ylabel='LW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalLW_cre_feedbacl_abrupt4CO2', leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_decomposition_comparison(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_feedback, ylabel='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalNet_cre_feedback_abrupt4CO2', leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_model_feedbacks_vs_w500_cmip6(complete_model_list, w500_bins_mid, abrupt4co2_regional_mean_w500_dist, picontrol_w500_hist, abrupt4co2_global_mean_ts, picontrol_global_mean_ts, obs_data_ann, picontrol_sw_cre_sum, picontrol_lw_cre_sum, show_plots=True, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, method='CMIP', w500_bins=w500_bins, cre_bins=cre_bins)
#     return  picontrol_global_mean_ts, picontrol_regional_mean_sw_all, picontrol_regional_mean_sw_clr, picontrol_regional_mean_lw_all, picontrol_regional_mean_lw_clr, picontrol_w500_hist, picontrol_w500_sw_cre_hist, picontrol_w500_lw_cre_hist, picontrol_sw_clr_sum, picontrol_sw_cre_sum, picontrol_sw_cre_sum_sq, picontrol_sw_all_sum, picontrol_lw_clr_sum, picontrol_lw_cre_sum, picontrol_lw_cre_sum_sq, picontrol_lw_all_sum, abrupt4co2_global_mean_ts,abrupt4co2_regional_mean_sw_all,abrupt4co2_regional_mean_sw_clr,abrupt4co2_regional_mean_lw_all,abrupt4co2_regional_mean_lw_clr,abrupt4co2_regional_mean_sw_cre,abrupt4co2_regional_mean_lw_cre,abrupt4co2_regional_mean_w500_dist,abrupt4co2_regional_mean_olr_vs_w500_dist,abrupt4co2_regional_mean_lw_cre_vs_w500_dist,abrupt4co2_regional_mean_osr_vs_w500_dist,abrupt4co2_regional_mean_sw_cre_vs_w500_dist, PiControl_params, abrupt4CO2_params, quad_co2_forcing, all_sky_feedback, net_cre_dynamic, net_cre_thermodynamic, net_cre_co_variation,sw_cre_dynamic, sw_cre_thermodynamic, sw_cre_co_variation, lw_cre_dynamic, lw_cre_thermodynamic, lw_cre_co_variation, net_cre_dynamic_param, net_cre_thermodynamic_param, net_cre_co_variation_param,sw_cre_dynamic_param, sw_cre_thermodynamic_param, sw_cre_co_variation_param, lw_cre_dynamic_param, lw_cre_thermodynamic_param, lw_cre_co_variation_param, net_cre_dynamic_obs, net_cre_thermodynamic_obs, net_cre_co_variation_obs,sw_cre_dynamic_obs, sw_cre_thermodynamic_obs, sw_cre_co_variation_obs, lw_cre_dynamic_obs, lw_cre_thermodynamic_obs, lw_cre_co_variation_obs, obs_data_param, obs_data_ann, complete_model_list


def obs_interannual_var(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), yearlist=range(2001,2015), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30, rad_source='CERES_EBAF', w500_source='ERA5'):
    '''
    plots cre_vs_w500 by year for analysis of interannual variability
    '''
    w500_bins_mid = 0.5*(w500_bins[:-1]+w500_bins[1:])
    obs_data = {}
    for year in yearlist:
       obs_data[str(year)] = match_omega500_rad_reanalyses_obs(w500_source=w500_source, rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=[year])
    fig = plt.figure(0)
    jj = 0
    ii = 0
    mean_sw_cre_adj2_mean = np.nanmean(np.array([obs_data[str(year)]['Ann']['sw_cre_adj2_mean'] for year in range(2001,2015)]), axis=0)
    for year in yearlist:
        if jj%4 == 0:
            ax = fig.add_subplot(221+ii)
            ii += 1
            plt.plot(w500_bins_mid, mean_sw_cre_adj2_mean, color='k', linewidth=2.0, label='2001-2014 mean')
            plt.text(0.1, 0.9, '('+chr(96+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        plt.plot(w500_bins_mid, obs_data[str(year)]['Ann']['sw_cre_adj2_mean'], color=colorlist[jj%4], label=str(year))
        jj += 1
        if jj%4 == 0:
            plt.legend(loc=0)
            ax.set_xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
            ax.set_ylabel('Mean SW CRE (W m$^{-2}$)')
            plt.xlim([0,50])
            plt.ylim([-45,-25])
    plt.legend(loc=0)
    ax.set_xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
    ax.set_ylabel('Mean SW CRE (W m$^{-2}$)')
    plt.xlim([0,50])
    plt.ylim([-45,-25])
    fig.tight_layout()
    plt.savefig('/home/users/phill/images/CIRCULATES/'+w500_source+'zoomed_sw_cre_vs_w500_by_year'+plot_type)
    plt.show()
    return obs_data
    


# def eval_cloud_circulation(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), yearlist=range(2001,2015), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30, rad_source='CERES_EBAF'):
#     '''
#     plots w500 distribution and cre vs w500 for observations and models

#     Produces plot intended for paper
#     '''
# #   Get observed data
#     era5_data = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     era5_data = era5_data['Ann']
#     jra55_data = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_data = jra55_data['Ann']
#     merra2_data = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_data = merra2_data['Ann']
#     obs_data = {}
#     for kk in ['sw_cre_hist', 'sw_cre_sum', 'lw_cre_hist', 'lw_cre_sum', 'w500_hist', 'w500_hist_lw', 'sw_cre_adj_hist', 'lw_cre_adj_hist', 'sw_cre_adj_sum', 'lw_cre_adj_sum', 'sw_cre_adj2_hist', 'lw_cre_adj2_hist', 'sw_cre_adj2_sum', 'lw_cre_adj2_sum']: # Check w500_hist_lw and adj2 variables  will work for CERES_EBAF
#         obs_data[kk] = era5_data[kk] + merra2_data[kk] + jra55_data[kk]
#     for kk in ['sw_cre_mean', 'lw_cre_mean', 'sw_cre_adj_mean', 'lw_cre_adj_mean', 'sw_cre_adj2_mean', 'lw_cre_adj2_mean']:# Check adj2 variables  will work for CERES_EBAF
#         obs_data[kk]= np.nanmean((era5_data[kk][:,None], merra2_data[kk][:,None], jra55_data[kk][:,None]), axis=0)[:,0]
#     AMIP_params_ceres_era = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=yearlist, fit_param=False)
#     AMIP_params_long = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(1979,2015), fit_param=False)
#     PiControl_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='PiControl', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(0,150), fit_param=False)
#     w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
#     cre_bins_mid = 0.5*(cre_bins[1:]+cre_bins[:-1])
#     AMIP_params_ceres_4K = {k : AMIP_params_ceres_era[k] for k in amip_p4k_dict.keys()}
#     AMIP_params_long_4K = {k : AMIP_params_long[k] for k in amip_p4k_dict.keys()}
#     PiControl_params = {k : PiControl_params[k] for k in amip_p4k_dict.keys()}
#     AMIP_params_ceres_4K['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_ceres_4K[model]['w500_hist'] for model in AMIP_params_ceres_4K.keys()]).mean(axis=0),
#                                                 'sw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_ceres_4K[model]['sw_cre_mean'] for model in AMIP_params_ceres_4K.keys()]), axis=0),
#                                                 'lw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_ceres_4K[model]['lw_cre_mean'] for model in AMIP_params_ceres_4K.keys()]), axis=0)
#                                          }
#     AMIP_params_long_4K['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long_4K[model]['w500_hist'] for model in AMIP_params_long_4K.keys()]).mean(axis=0),
#                                                'sw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_long_4K[model]['sw_cre_mean'] for model in AMIP_params_long_4K.keys()]), axis=0),
#                                                'lw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_long_4K[model]['lw_cre_mean'] for model in AMIP_params_long_4K.keys()]), axis=0)
#                                          }
#     PiControl_params['multi_model_mean'] = {'w500_hist' : np.array([PiControl_params[model]['w500_hist'] for model in PiControl_params.keys()]).mean(axis=0),
#                                                'sw_cre_adj2_mean' : np.nanmean(np.array([PiControl_params[model]['sw_cre_mean'] for model in PiControl_params.keys()]), axis=0),
#                                                'lw_cre_adj2_mean' : np.nanmean(np.array([PiControl_params[model]['lw_cre_mean'] for model in PiControl_params.keys()]), axis=0)
#                                          }
#     AMIP_params_long_4K['multi_model_mean']['sw_cre_mean'] = AMIP_params_long_4K['multi_model_mean']['sw_cre_adj2_mean']
#     AMIP_params_long_4K['multi_model_mean']['lw_cre_mean'] = AMIP_params_long_4K['multi_model_mean']['lw_cre_adj2_mean']
# #   Plot multi-mean vs obs
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(5.4,3.9))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K['multi_model_mean'], AMIP_params_long_4K['multi_model_mean'], labels=['Obs', 'AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='w500_hist', fig=fig, subplot_index=311, panel='(a)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs')
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K['multi_model_mean'], AMIP_params_long_4K['multi_model_mean'], labels=['Obs', 'AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='lw_cre_adj2_mean', fig=fig, subplot_index=312, panel='(b)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, show_legend=True, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs')
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K['multi_model_mean'], AMIP_params_long_4K['multi_model_mean'], labels=['Obs', 'AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='sw_cre_adj2_mean', fig=fig, subplot_index=313, panel='(c)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs')
#     #Now plot picontrol instead of AMIP for CERES ERA.
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(5.4,3.9))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, PiControl_params['multi_model_mean'], AMIP_params_long_4K['multi_model_mean'], labels=['Obs', 'PiControl', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='w500_hist', fig=fig, subplot_index=311, panel='(a)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs_plus_picontrol')
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, PiControl_params['multi_model_mean'], AMIP_params_long_4K['multi_model_mean'], labels=['Obs', 'PiControl', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='lw_cre_adj2_mean', fig=fig, subplot_index=312, panel='(b)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, show_legend=True, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs_plus_picontrol')
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, PiControl_params['multi_model_mean'], AMIP_params_long_4K['multi_model_mean'], labels=['Obs', 'PiControl', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='sw_cre_adj2_mean', fig=fig, subplot_index=313, panel='(c)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs_plus_picontrol')
# #   Plot both PDF and differences, 4 panels 7 models per panel
#     model_list = list(AMIP_params_ceres_4K.keys())
#     model_list.remove('multi_model_mean')
#     model_list.sort(key=lambda s: s.lower())
#     model_list += ['multi_model_mean']
# #   SW CRE vs w500 zoomed to 0-50 hPa day-1
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(7,6))
#     for ii in range(2,4): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0)- obs_data['sw_cre_adj2_mean'], np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0)- obs_data['sw_cre_adj2_mean'], color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[(ii-2)*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['sw_cre_mean'] - obs_data['sw_cre_adj2_mean'], color=colorlist[jj %2 ], linestyle=linestylelist[jj], label=model, linewidth=2)
#         plt.xlim([0,50])
#         plt.ylim([-30,10])
#         plt.text(0.1, 0.9, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         if ii == 2:
#             plt.ylabel('CMIP6 - observed Mean SW CRE (W m$^{-2}$)')
#         else:
#             ax.tick_params(labelleft=False)
#     for ii in range(2): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         plt.text(0.1, 0.9, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         for jj in range(7):
#             model = model_list[ii*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['sw_cre_mean'], color=colorlist[jj % 2 ], linestyle=linestylelist[jj ], label=model, linewidth=2)
#         plt.plot(w500_bins_mid, obs_data['sw_cre_adj2_mean'], color=colorlist[3], label='Obs')
#         plt.xlim([0,50])
#         plt.ylim([-70,-20])
#         plt.legend(loc=(0.425,-0.15), handlelength=2.5).set_zorder(102)
#         ax.tick_params(labelbottom=False)
#         if ii == 0:
#             plt.ylabel('Mean SW CRE (W m$^{-2}$)')
#         else:
#             ax.tick_params(labelleft=False)
#     fig.subplots_adjust(left=0.105, right=0.95, bottom=0.1, top=0.95, wspace=0.16, hspace=0.11)
#     plt.savefig('/home/users/phill/images/CIRCULATES/zoomed_sw_cre_vs_w500_models_vs_obs_diff'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   SW CRE vs w500
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(7,6))
#     for ii in range(2,4): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0)- obs_data['sw_cre_adj2_mean'], np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0)- obs_data['sw_cre_adj2_mean'], color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[(ii-2)*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['sw_cre_mean'] - obs_data['sw_cre_adj2_mean'], color=colorlist[jj %2 ], linestyle=linestylelist[jj], label=model, linewidth=2)
#         plt.xlim([-150,100])
#         plt.ylim([-40,20])
# #        plt.legend(loc=0, handlelength=2.5)
#         plt.text(0.06, 0.94, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         if ii == 2:
#             plt.ylabel('CMIP6 - observed Mean SW CRE (W m$^{-2}$)')
#         else:
#             ax.tick_params(labelleft=False)
#     for ii in range(2): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[ii*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['sw_cre_mean'], color=colorlist[jj % 2 ], linestyle=linestylelist[jj ], label=model, linewidth=2)
#         plt.plot(w500_bins_mid, obs_data['sw_cre_adj2_mean'], color=colorlist[3], label='Obs')
#         plt.xlim([-150,100])
#         plt.ylim([-150,0])
#         plt.text(0.06, 0.94, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.legend(loc=(0.4,-0.25), handlelength=2.5).set_zorder(102)
#         ax.tick_params(labelbottom=False)
#         if ii == 0:
#             plt.ylabel('Mean SW CRE (W m$^{-2}$)')
#         else:
#             ax.tick_params(labelleft=False)
#     fig.subplots_adjust(left=0.105, right=0.95, bottom=0.1, top=0.95, wspace=0.16, hspace=0.11)
#     plt.savefig('/home/users/phill/images/CIRCULATES/sw_cre_vs_w500_models_vs_obs_diff'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   LW CRE vs w500
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(7,6))
#     for ii in range(2,4): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0)- obs_data['lw_cre_adj2_mean'], np.max((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0)- obs_data['lw_cre_adj2_mean'], color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[(ii-2)*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['lw_cre_mean'] - obs_data['lw_cre_adj2_mean'], color=colorlist[jj %2 ], linestyle=linestylelist[jj], label=model, linewidth=2)
#         plt.xlim([-150,100])
#         plt.ylim([-25,25])
#         plt.text(0.94, 0.94, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
# #        plt.legend(loc=0, handlelength=2.5)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         if ii == 2:
#             plt.ylabel('CMIP6 - observed Mean LW CRE (W m$^{-2}$)')
#         else:
#             ax.tick_params(labelleft=False)
#     for ii in range(2): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0), np.max((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0), color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[ii*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['lw_cre_mean'], color=colorlist[jj % 2 ], linestyle=linestylelist[jj ], label=model, linewidth=2)
#         plt.plot(w500_bins_mid, obs_data['lw_cre_adj2_mean'], color=colorlist[3], label='Obs')
#         plt.xlim([-150,100])
#         plt.ylim([0,100])
#         plt.text(0.94, 0.94, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         if ii == 0:
#             plt.legend(loc=(0.025,-0.275), handlelength=2.5).set_zorder(102)
#         else:
#             plt.legend(loc=(0.025,-0.3), handlelength=2.5).set_zorder(102)
#         ax.tick_params(labelbottom=False)
#         if ii == 0:
#             plt.ylabel('Mean LW CRE (W m$^{-2}$)')
#         else:
#             ax.tick_params(labelleft=False)
#     fig.subplots_adjust(left=0.105, right=0.95, bottom=0.1, top=0.95, wspace=0.16, hspace=0.11)
#     plt.savefig('/home/users/phill/images/CIRCULATES/lw_cre_vs_w500_models_vs_obs_diff'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   w500 distribution
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(7,6))
#     for ii in range(2): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0), np.max((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0), color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[ii*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['w500_hist']/AMIP_params_long_4K[model]['w500_hist'].sum(), color=colorlist[jj % 2 ], linestyle=linestylelist[jj ], label=model, linewidth=2)
#         plt.plot(w500_bins_mid, obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[3], label='Obs')
#         plt.xlim([-150,100])
#         plt.text(0.94, 0.94, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.ylim([0.0,0.05])
#         plt.legend(loc=0, handlelength=2.5)
# #        plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         ax.tick_params(labelbottom=False)
#         if ii == 0:
#             plt.ylabel('Frequency')
#         else:
#             ax.tick_params(labelleft=False)
#     for ii in range(2,4): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(221+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0)- obs_data['w500_hist']/obs_data['w500_hist'].sum(), np.max((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0)- obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         for jj in range(7):
#             model = model_list[(ii-2)*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['w500_hist']/AMIP_params_long_4K[model]['w500_hist'].sum() - obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[jj %2 ], linestyle=linestylelist[jj], label=model, linewidth=2)
#         plt.text(0.94, 0.94, '('+chr(97+ii)+')', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.xlim([-150,100])
#         plt.ylim([-0.02,0.01])
# #        plt.legend(loc=0, handlelength=3.0)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         if ii == 2:
#             plt.ylabel('CMIP6 - observed frequency')
#         else:
#             ax.tick_params(labelleft=False)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/w500_dist_models_vs_obs_diff'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   Plot one reanalysis and one model with error bars showing sampling uncertainty on the cre dependence on w500.
#     era5_sd = np.sqrt(np.sum(era5_data['sw_cre_adj2_hist']*(cre_bins_mid**2), axis=1)/np.sum(era5_data['sw_cre_adj2_hist'], axis=1) - (np.sum(era5_data['sw_cre_adj2_hist']*(cre_bins_mid), axis=1)/np.sum(era5_data['sw_cre_adj2_hist'], axis=1))**2)
#     ipsl_sd = np.sqrt(np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist']*(cre_bins_mid**2), axis=1)/np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'], axis=1) - (np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist']*(cre_bins_mid), axis=1)/np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'], axis=1))**2)
#     plt.plot(w500_bins_mid, np.sum(era5_data['sw_cre_adj2_hist']*cre_bins_mid, axis=1)/np.sum(era5_data['sw_cre_adj2_hist'],axis=1), color='blue')
#     plt.plot(w500_bins_mid, np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist']*cre_bins_mid, axis=1)/np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'],axis=1), color='red')
#     plt.fill_between(w500_bins_mid, np.sum(era5_data['sw_cre_adj2_hist']*cre_bins_mid, axis=1)/np.sum(era5_data['sw_cre_adj2_hist'],axis=1)+era5_sd/np.sqrt(5400*np.sum(era5_data['sw_cre_adj2_hist'], axis=1)), np.sum(era5_data['sw_cre_adj2_hist']*cre_bins_mid, axis=1)/np.sum(era5_data['sw_cre_adj2_hist'],axis=1)-era5_sd/np.sqrt(5400*np.sum(era5_data['sw_cre_adj2_hist'], axis=1)), color='blue', alpha=0.4)
#     plt.fill_between(w500_bins_mid, np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist']*cre_bins_mid, axis=1)/np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'],axis=1)-ipsl_sd/np.sqrt(5400*np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'], axis=1)), np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist']*cre_bins_mid, axis=1)/np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'],axis=1)+ipsl_sd/np.sqrt(5400*np.sum(AMIP_params_ceres_era['IPSL-CM6A-LR']['sw_cre_hist'], axis=1)), color='red', alpha=0.4)
#     plt.xlim([-150,100])
#     plt.ylim([-120,-20])
#     plt.legend(['ERA5', 'IPSL-CM6A-LR'])
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.ylabel('Mean SW CRE (W m$^{-2}$)')
#     plt.savefig('/home/users/phill/images/CIRCULATES/sw_cre_vs_w500_plus_sampling_error_ERA5_IPSL.png')
#     plt.show()
# #    return era5_data, jra55_data, merra2_data, obs_data, AMIP_params_ceres_era, AMIP_params_long, PiControl_params

# #   Plot individual models as differences, 
#     model_list = list(AMIP_params_ceres_4K.keys())
#     model_list.remove('multi_model_mean')
#     model_list.sort(key=lambda s: s.lower())
#     model_list += ['multi_model_mean']
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     for ii in range(2): # 2 panels, 7 models per panel
#         ax = fig.add_subplot(211+ii)
#         plt.fill_between(w500_bins_mid,np.min((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0)- obs_data['w500_hist']/obs_data['w500_hist'].sum(), np.max((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0)- obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[2], label='')
#         linestylelist=[':', '-', '--', '-.', '-',':', '-.', '--']
#         markerlist=['o', 's', 'p', 'D', 'o', 's', 'p', 'D']
#         for jj in range(7):
#             model = model_list[ii*7+jj]
#             plt.plot(w500_bins_mid, AMIP_params_long_4K[model]['w500_hist']/AMIP_params_long_4K[model]['w500_hist'].sum() - obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[jj %2 ], linestyle=linestylelist[jj], label=model, linewidth=2)
#         plt.xlim([-150,100])
#         plt.ylim([-0.02,0.01])
#         plt.legend(loc=0, handlelength=3.0)
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.ylabel('CMIP6 - observed frequency')
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/w500_dist_models_vs_obs_diff'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   Plot individual models vs obs start with w500 PDF
#     model_list = list(AMIP_params_ceres_4K.keys())
#     model_list.remove('multi_model_mean')
#     model_list.sort(key=lambda s: s.lower())
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     for ii in range(13):
#         model = model_list[ii]
#         plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K[model], AMIP_params_long_4K[model], labels=['Obs','AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='w500_hist', fig=fig, subplot_index=(5,3,ii+1), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_model_vs_obs', title='('+chr(97+ii)+') '+model)
#     fig.tight_layout()
#     plt.legend(bbox_to_anchor=(2.0, 0.5), loc='center')
#     plt.savefig('/home/users/phill/images/CIRCULATES/w500_dist_model_vs_obs'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   SW CRE by model
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     for ii in range(13):
#         model = model_list[ii]
#         AMIP_params_ceres_4K[model]['sw_cre_adj2_mean']=AMIP_params_ceres_4K[model]['sw_cre_mean']
#         AMIP_params_long_4K[model]['sw_cre_adj2_mean']=AMIP_params_long_4K[model]['sw_cre_mean']
#         plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K[model], AMIP_params_long_4K[model], labels=['Obs','AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='sw_cre_adj2_mean', fig=fig, subplot_index=(5,3,ii+1), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_vs_swcre_model_vs_obs', title='('+chr(97+ii)+') '+model)
#     fig.tight_layout()
#     plt.legend(bbox_to_anchor=(2.0, 0.5), loc='center')
#     plt.savefig('/home/users/phill/images/CIRCULATES/w500_vs_swcre_model_vs_obs'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
# #   LW CRE by model
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     for ii in range(13):
#         model = model_list[ii]
#         AMIP_params_ceres_4K[model]['lw_cre_adj2_mean']=AMIP_params_ceres_4K[model]['lw_cre_mean']
#         AMIP_params_long_4K[model]['lw_cre_adj2_mean']=AMIP_params_long_4K[model]['lw_cre_mean']
#         plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K[model], AMIP_params_long_4K[model], labels=['Obs','AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data=era5_data, jra55_data=jra55_data, merra2_data=merra2_data, var='lw_cre_adj2_mean', fig=fig, subplot_index=(5,3,ii+1), lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_vs_lwcre_model_vs_obs', title='('+chr(97+ii)+') '+model)
#     fig.tight_layout()
#     plt.legend(bbox_to_anchor=(2.0, 0.5), loc='center')
#     plt.savefig('/home/users/phill/images/CIRCULATES/w500_vs_lwcre_model_vs_obs'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
#     return
# #   Plot multi-mean from different reanalyses
#     if plot_type == '.png':
#         fig = plt.figure(0, figsize=(7,3))
#     elif plot_type == '.eps':
#         fig = plt.figure(0, figsize=(5,8))
#     plot_circ_cloud_relationships(w500_bins, cre_bins, era5_data, merra2_data, jra55_data, labels=['ERA5', 'MERRA2', 'JRA55', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], var='w500_hist', fig=fig, subplot_index=311, panel='(a)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_obs')
#     plot_circ_cloud_relationships(w500_bins, cre_bins, era5_data, merra2_data, jra55_data, labels=['ERA5', 'MERRA2', 'JRA55', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], var='lw_cre_adj2_mean', fig=fig, subplot_index=312, panel='(b)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, show_legend=True, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_obs')
#     plot_circ_cloud_relationships(w500_bins, cre_bins, era5_data, merra2_data, jra55_data, labels=['ERA5', 'MERRA2', 'JRA55', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], var='sw_cre_adj2_mean', fig=fig, subplot_index=313, panel='(c)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_obs')
#     fig = plt.figure(0, figsize=(5,8))
#     ax = fig.add_subplot(221)
#     plt.fill_between(w500_bins_mid,np.min((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0), np.max((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0), color='grey', label='')
#     plt.plot(w500_bins_mid, obs_data['lw_cre_adj2_mean'], color='k', label='Obs 2001-2014')
#     plt.plot(w500_bins_mid, AMIP_params_ceres_4K['multi_model_mean']['lw_cre_adj2_mean'], color=colorlist[1], linestyle='--', label='CFMIP 2001-2014')
#     plt.plot(w500_bins_mid, AMIP_params_long_4K['multi_model_mean']['lw_cre_adj2_mean'], color=colorlist[2], linestyle=':', label='CFMIP 1979-2014')
#     plt.legend(loc=0, handlelength=1.5)
#     plt.ylabel('Mean LW CRE (W m$^{-2}$)')
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.xlim([-150,100])
#     plt.ylim([0,100])
#     plt.text(0.1, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     plt.grid(color='lightgrey')
#     ax = fig.add_subplot(222)
#     plt.fill_between(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), color='grey', label='')
#     plt.plot(w500_bins_mid, obs_data['sw_cre_adj2_mean'], color='k', label='Obs')
#     plt.plot(w500_bins_mid, AMIP_params_ceres_4K['multi_model_mean']['sw_cre_adj2_mean'], color=colorlist[1], linestyle='--', label='AMIP 2001-2014')
#     plt.plot(w500_bins_mid, AMIP_params_long_4K['multi_model_mean']['sw_cre_adj2_mean'], color=colorlist[2], linestyle=':', label='AMIP 1979-2014')
#     plt.ylabel('Mean SW CRE (W m$^{-2}$)')
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.xlim([-150,100])
#     plt.ylim([-125,0])
#     plt.grid(color='lightgrey')
#     plt.text(0.1, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     ax = fig.add_subplot(223)
#     plt.plot(w500_bins_mid,np.min((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0)-obs_data['lw_cre_adj2_mean'], color='k', label='')
#     plt.plot(w500_bins_mid, np.max((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0)-obs_data['lw_cre_adj2_mean'], color='black', label='Obs range')
#     plt.plot(w500_bins_mid, AMIP_params_ceres_4K['multi_model_mean']['lw_cre_adj2_mean']-obs_data['lw_cre_adj2_mean'], color=colorlist[1], linestyle='--', label='AMIP 2001-2014')
#     plt.plot(w500_bins_mid, AMIP_params_long_4K['multi_model_mean']['lw_cre_adj2_mean']-obs_data['lw_cre_adj2_mean'], color=colorlist[2], linestyle=':', label='AMIP 1979-2014')
#     plt.legend(loc=0, handlelength=1.5)
#     plt.ylabel('CMIP6 - observed mean LW CRE (W m$^{-2}$)')
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.xlim([-150,100])
#     plt.ylim([-15,15])
#     plt.grid(color='lightgrey')
#     plt.text(0.1, 0.9, '(c)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     ax = fig.add_subplot(224)
#     plt.plot(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0)-obs_data['sw_cre_adj2_mean'], color='k', label='')
#     plt.plot(w500_bins_mid, np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0)-obs_data['sw_cre_adj2_mean'], color='k', label='Obs range')
#     plt.plot(w500_bins_mid, AMIP_params_ceres_4K['multi_model_mean']['sw_cre_adj2_mean']-obs_data['sw_cre_adj2_mean'], color=colorlist[1], linestyle='--', label='AMIP 2001-2014')
#     plt.plot(w500_bins_mid, AMIP_params_long_4K['multi_model_mean']['sw_cre_adj2_mean']-obs_data['sw_cre_adj2_mean'], color=colorlist[2], linestyle=':', label='AMIP 1979-2014')
#     plt.ylabel('CMIP6 - observed mean SW CRE (W m$^{-2}$)')
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.xlim([-150,100])
#     plt.ylim([-15,15])
#     plt.text(0.1, 0.9, '(d)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     plt.grid(color='lightgrey')
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/cre_vs_w500_err'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
#     fig = plt.figure(0, figsize=(5,6))
#     ax = fig.add_subplot(211)
#     plt.fill_between(w500_bins_mid,np.min((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0), np.max((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0), color='grey', label='')
#     plt.plot(w500_bins_mid, obs_data['w500_hist']/obs_data['w500_hist'].sum(), color='k', label='Obs')
#     plt.plot(w500_bins_mid, np.array([AMIP_params_ceres_4K[k]['w500_hist']/AMIP_params_ceres_4K[k]['w500_hist'].sum() for k in AMIP_params_ceres_4K.keys()]).mean(axis=0), color=colorlist[1], linestyle='--', label='AMIP 2001-2014')
#     plt.plot(w500_bins_mid, np.array([AMIP_params_long_4K[k]['w500_hist']/AMIP_params_long_4K[k]['w500_hist'].sum() for k in AMIP_params_long_4K.keys()]).mean(axis=0), color=colorlist[2], linestyle=':', label='AMIP 1979-2014')
#     plt.ylabel('Frequency')
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.grid(color='lightgrey')
#     plt.xlim([-150,100])
#     plt.text(0.1, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     ax = fig.add_subplot(212)
#     plt.plot(w500_bins_mid,np.min((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0) - obs_data['w500_hist']/obs_data['w500_hist'].sum(), color='k', label='')
#     plt.plot(w500_bins_mid,np.max((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum())- obs_data['w500_hist']/obs_data['w500_hist'].sum(), axis=0), color='k', label='Obs range')
#     plt.plot(w500_bins_mid, np.array([AMIP_params_ceres_4K[k]['w500_hist']/AMIP_params_ceres_4K[k]['w500_hist'].sum() for k in AMIP_params_ceres_4K.keys()]).mean(axis=0) - obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[1], linestyle='--', label='CFMIP 00-14')
#     plt.plot(w500_bins_mid, np.array([AMIP_params_long_4K[k]['w500_hist']/AMIP_params_long_4K[k]['w500_hist'].sum() for k in AMIP_params_long_4K.keys()]).mean(axis=0) - obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=colorlist[2], linestyle=':', label='CFMIP 79-14')
#     plt.legend(loc=0, handlelength=1.5)
#     plt.ylabel('CMIP6 - observed frequency')
#     plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#     plt.grid(color='lightgrey')
#     plt.xlim([-150,100])
#     plt.text(0.1, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/w500_dist_error'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()
#     return era5_data, jra55_data, merra2_data, obs_data, AMIP_params_ceres_era, AMIP_params_long, PiControl_params


# def plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, AMIP_params_ceres_4K, AMIP_params_long_4K, title='', labels=['Obs', 'AMIP 2001-2014', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], era5_data={}, jra55_data={}, merra2_data={}, var='w500_hist', fig=None, subplot_index=111, panel='', lon_min=165, lon_max=235, lat_min=-30, lat_max=30, show_legend=False, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs'):
#     '''
#     Produces plot comparing w500 dist and cre as fn of w500.
#     '''
#     if fig == None:
#         if plot_type == '.png':
#             fig = plt.figure(0, figsize=(7,3))
#         elif plot_type == '.eps':
#             fig = plt.figure(0, figsize=(5,8))
#     w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
#     if type(subplot_index) == tuple:
#         ax = fig.add_subplot(subplot_index[0], subplot_index[1], subplot_index[2])
#     else:
#         ax = fig.add_subplot(subplot_index)
#     if var == 'w500_hist':
#         if 'w500_hist' in era5_data.keys(): 
#             plt.fill_between(w500_bins_mid,np.min((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0), np.max((era5_data['w500_hist']/era5_data['w500_hist'].sum(), jra55_data['w500_hist']/jra55_data['w500_hist'].sum(), merra2_data['w500_hist']/merra2_data['w500_hist'].sum()), axis=0), color=list_of_colors[3], label=labels[3])
#         plt.plot(w500_bins_mid, obs_data['w500_hist']/obs_data['w500_hist'].sum(), color=list_of_colors[0], label=labels[0])
#         plt.plot(w500_bins_mid, AMIP_params_ceres_4K['w500_hist']/AMIP_params_ceres_4K['w500_hist'].sum(), color=list_of_colors[1], linestyle='--', label=labels[1])
#         plt.plot(w500_bins_mid, AMIP_params_long_4K['w500_hist']/AMIP_params_long_4K['w500_hist'].sum(), color=list_of_colors[2], linestyle=':', label=labels[2])
#         plt.ylabel('Frequency')
#         if len(panel) > 0:
#             print('Edited OK, why is red spot not appearing??')
#             plt.scatter(0.1, 0.9, transform=plt.gca().transAxes, color='white') # Make invisible plot point here to stop legend obscuring text.
#             plt.text(0.1, 0.9, panel, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         if show_legend:
#             plt.legend(loc=0, handlelength=1.5)
#         if type(subplot_index) == tuple:
#            plt.xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#            plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.grid(color='lightgrey')
#         plt.xlim([-150,100])
#         if len(title) > 0:
#             plt.title(title)
#     if var == 'lw_cre_adj2_mean':
#         if 'w500_hist' in era5_data.keys(): 
#             plt.fill_between(w500_bins_mid,np.min((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0), np.max((era5_data['lw_cre_adj2_mean'], jra55_data['lw_cre_adj2_mean'], merra2_data['lw_cre_adj2_mean']), axis=0), color=colorlist[2], label=labels[3])
#         plt.plot(w500_bins_mid, obs_data['lw_cre_adj2_mean'], color=colorlist[3], label=labels[0])
#         plt.plot(w500_bins_mid, AMIP_params_ceres_4K['lw_cre_adj2_mean'], color=colorlist[0], linestyle='--', label=labels[1])
#         plt.plot(w500_bins_mid, AMIP_params_long_4K['lw_cre_adj2_mean'], color=colorlist[1], linestyle=':', label=labels[2])
#         if show_legend:
#             plt.legend(loc=0, handlelength=1.5)
#         plt.ylabel('Mean LW CRE (W m$^{-2}$)')
#         if type(subplot_index) == tuple:
#            plt.xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#            plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.ylim([0,100])
#         plt.grid(color='lightgrey')
#         if len(panel) > 0:
#             plt.text(0.1, 0.9, panel, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         if len(title) > 0:
#             plt.title(title)
#     if var == 'sw_cre_adj2_mean':
#         if 'w500_hist' in era5_data.keys(): 
#             plt.fill_between(w500_bins_mid,np.min((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), np.max((era5_data['sw_cre_adj2_mean'], jra55_data['sw_cre_adj2_mean'], merra2_data['sw_cre_adj2_mean']), axis=0), color=colorlist[2], label=labels[3])
#         plt.plot(w500_bins_mid, obs_data['sw_cre_adj2_mean'], color=colorlist[3], label=labels[0])
#         plt.plot(w500_bins_mid, AMIP_params_ceres_4K['sw_cre_adj2_mean'], color=colorlist[0], linestyle='--', label=labels[1])
#         plt.plot(w500_bins_mid, AMIP_params_long_4K['sw_cre_adj2_mean'], color=colorlist[1], linestyle=':', label=labels[2])
#         if len(panel) > 0:
#             plt.scatter(0.1, 0.9, transform=plt.gca().transAxes, color='white') # Make invisible plot point here to stop legend obscuring text.
#             plt.text(0.1, 0.9, panel, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         if show_legend:
#             plt.legend(loc=0, handlelength=1.5)
#         plt.ylabel('Mean SW CRE (W m$^{-2}$)')
#         if type(subplot_index) == tuple:
#            plt.xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#            plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.ylim([-125,0])
#         plt.grid(color='lightgrey')
#         if len(title) > 0:
#             plt.title(title)
#     if int(str(subplot_index).replace(',', '').replace('(', '').replace(')', '').replace(' ', '')[2]) == int(str(subplot_index).replace(',', '').replace('(', '').replace(')', '').replace(' ', '')[0])*int(str(subplot_index).replace(',', '').replace('(', '').replace(')', '').replace(' ', '')[1]):
#         fig.tight_layout()
#         plt.savefig(savename+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_'+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#         plt.show()
    
    
    
# def calc_feedbacks_amip(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), yearlist=range(2001,2015), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30, rad_source='CERES_EBAF', fit='A'):
#     '''
#     Calculates feedbacks and components of feedback

#     Method: first 150 years each of abrupt4CO2 and piControl.
#     Feedback is calculated using Gregory method, using annual abrupt4xCO2
#     anomalies of regional mean TOA rad versus (where anomaly is wrt 150 year
#     regional mean TOA rad from picontrol) versus global mean surface
#     temperarure anomaly (again wrt 150 year mean from pi control)
#     '''
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
#     complete_model_list = []
#     net_cre_all, sw_cre_all, lw_cre_all, net_cre_feedback_all, sw_cre_feedback_all, lw_cre_feedback_all, net_cre_dynamic, net_cre_thermodynamic, net_cre_co_variation,sw_cre_dynamic, sw_cre_thermodynamic, sw_cre_co_variation, lw_cre_dynamic, lw_cre_thermodynamic, lw_cre_co_variation, net_cre_dynamic_param, net_cre_thermodynamic_param, net_cre_co_variation_param,sw_cre_dynamic_param, sw_cre_thermodynamic_param, sw_cre_co_variation_param, lw_cre_dynamic_param, lw_cre_thermodynamic_param, lw_cre_co_variation_param, net_cre_dynamic_obs, net_cre_thermodynamic_obs, net_cre_co_variation_obs,sw_cre_dynamic_obs, sw_cre_thermodynamic_obs, sw_cre_co_variation_obs, lw_cre_dynamic_obs, lw_cre_thermodynamic_obs, lw_cre_co_variation_obs, net_cre_dynamic_feedback, net_cre_thermodynamic_feedback, net_cre_co_variation_feedback,sw_cre_dynamic_feedback, sw_cre_thermodynamic_feedback, sw_cre_co_variation_feedback, lw_cre_dynamic_feedback, lw_cre_thermodynamic_feedback, lw_cre_co_variation_feedback, net_cre_dynamic_obs_param_feedback, net_cre_thermodynamic_obs_param_feedback, net_cre_co_variation_obs_param_feedback,sw_cre_dynamic_obs_param_feedback, sw_cre_thermodynamic_obs_param_feedback, sw_cre_co_variation_obs_param_feedback, lw_cre_dynamic_obs_param_feedback, lw_cre_thermodynamic_obs_param_feedback, lw_cre_co_variation_obs_param_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_obs_feedback,sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_obs_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_obs_feedback, net_cre_dynamic_era5_feedback, net_cre_thermodynamic_era5_feedback, net_cre_co_variation_era5_feedback,sw_cre_dynamic_era5_feedback, sw_cre_thermodynamic_era5_feedback, sw_cre_co_variation_era5_feedback, lw_cre_dynamic_era5_feedback, lw_cre_thermodynamic_era5_feedback, lw_cre_co_variation_era5_feedback, net_cre_dynamic_merra2_feedback, net_cre_thermodynamic_merra2_feedback, net_cre_co_variation_merra2_feedback,sw_cre_dynamic_merra2_feedback, sw_cre_thermodynamic_merra2_feedback, sw_cre_co_variation_merra2_feedback, lw_cre_dynamic_merra2_feedback, lw_cre_thermodynamic_merra2_feedback, lw_cre_co_variation_merra2_feedback, net_cre_dynamic_jra55_feedback, net_cre_thermodynamic_jra55_feedback, net_cre_co_variation_jra55_feedback,sw_cre_dynamic_jra55_feedback, sw_cre_thermodynamic_jra55_feedback, sw_cre_co_variation_jra55_feedback, lw_cre_dynamic_jra55_feedback, lw_cre_thermodynamic_jra55_feedback, lw_cre_co_variation_jra55_feedback = ({} for __ in range(87))
# #   Get observed data
#     era5_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     jra55_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     merra2_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
#     obs_data = {}
#     obs_data_param, era5_data_param, jra55_data_param, merra2_data_param, obs_data_ann = combined_reanalysis_w500_cre_fit(era5_vs_ceres_two_deg_monthly['Ann'], merra2_vs_ceres_two_deg_monthly['Ann'], jra55_vs_ceres_two_deg_monthly['Ann'], w500_bins=w500_bins, cre_bins=cre_bins, spatial_av_scale=2.0, time_av_scale=24*30, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist, n_bootstrap=n_bootstrap, month='ANN', rad_source=rad_source)
#     obs_data.update({'Ann' : obs_data_ann})
# #   ADJ2 values are consistent with model definition of CRE, so use these instead.
#     obs_data['Ann']['sw_cre_mean'] = obs_data['Ann']['sw_cre_adj2_mean']
#     obs_data['Ann']['sw_cre_hist'] = obs_data['Ann']['sw_cre_adj2_hist']
#     obs_data['Ann']['lw_cre_mean'] = obs_data['Ann']['lw_cre_adj2_mean']
#     obs_data['Ann']['lw_cre_hist'] = obs_data['Ann']['lw_cre_adj2_hist']
# #   Get fits, which we use to compare whether they change with time period and model version and whether the fit is good enough to use instead of data
#     n_samples = int(((lat_max-lat_min)/spatial_av_scale)*((lon_max-lon_min)/spatial_av_scale)*(len(yearlist)*12*30*24/time_av_scale))
#     obs_data_param = bootstrap_sample_obs_intensity(obs_data_param, w500_bins_mid, [obs_data, era5_vs_ceres_two_deg_monthly, merra2_vs_ceres_two_deg_monthly, jra55_vs_ceres_two_deg_monthly], n_samples, n_bootstrap=n_bootstrap, seed=seed)
#     AMIP_params_ceres_era = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=yearlist)
#     AMIP_params_long = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(1979,2015))
#     AMIP4K_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP+4K', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(1979,2015))
#     for model in amip_p4k_dict.keys():
#         if (model in amip_dict.keys()):
#             complete_model_list += [model]
#     complete_model_list.sort()
# #    return complete_model_list, AMIP_params_ceres_era, AMIP_params_long, AMIP4K_params, obs_data_param, obs_data
# #   First compare data across scenarios and averaging period.
#     AMIP_params_long_temp = AMIP_params_long.copy()
#     AMIP_params_long_temp['Multi-model mean'] = {'circ_intensity_bootstrap' : 0}
#     AMIP_params_long_temp['Multi-model mean']['circ_intensity'] = np.mean([AMIP_params_long[m]['circ_intensity'] for m in complete_model_list])
#     AMIP4K_params_temp = AMIP4K_params.copy()
#     AMIP4K_params_temp['Multi-model mean'] = {'circ_intensity_bootstrap' : 0}
#     AMIP4K_params_temp['Multi-model mean']['circ_intensity'] = np.mean([AMIP4K_params[m]['circ_intensity'] for m in complete_model_list])
#     print("np.std([AMIP_params_long[m]['circ_intensity'] for m in complete_model_list])=",np.std([AMIP_params_long[m]['circ_intensity'] for m in complete_model_list]))
#     print("np.std([AMIP4K_params[m]['circ_intensity'] - AMIP_params_long[m]['circ_intensity'] for m in complete_model_list])=",np.std([AMIP4K_params[m]['circ_intensity'] - AMIP_params_long[m]['circ_intensity'] for m in complete_model_list]))
#     plot_scenario_comparison(['Multi-model mean',]+complete_model_list, [AMIP_params_long_temp, AMIP4K_params_temp], obs_data_param, var='circ_intensity', model_labels_list=['AMIP 1979-2014', 'AMIP4K'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, errorbar=False)
# #    return obs_data_param
#     plot_scenario_comparison(complete_model_list, [AMIP_params_ceres_era, AMIP_params_long, AMIP4K_params], obs_data_param, var='circ_intensity', model_labels_list=['AMIP 2001-2014', 'AMIP 1979-2014', 'AMIP+4K'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_scenario_comparison(complete_model_list, [AMIP_params_ceres_era, AMIP_params_long, AMIP4K_params], obs_data_param, var='circ_mode', ylabel='Modal vertical velocity (hPa day$^{-1}$)', model_labels_list=['AMIP 2001-2014', 'AMIP 1979-2014', 'AMIP+4K'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     for region in ['SW', 'LW']:
#         for param in ['A', 'B', 'C', 'D']:
#             plot_scenario_comparison(complete_model_list, [AMIP_params_ceres_era, AMIP_params_long, AMIP4K_params], obs_data_param, var=param, region=region, ylabel=region+' CRE vs w500 fit, '+param, model_labels_list=['AMIP 2001-2014', 'AMIP 1979-2014', 'AMIP+4K'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
# #   Now do plot for each model.
#     for model in complete_model_list:
# #       Plot vs observations
#         fig = plt.figure(0)
#         plt.plot(w500_bins_mid,obs_data['Ann']['w500_hist'], 'k')
#         plt.plot(w500_bins_mid,AMIP_params_ceres_era[model]['w500_hist'])
#         plt.plot(w500_bins_mid,AMIP_params_long[model]['w500_hist'])
#         plt.plot(w500_bins_mid,AMIP4K_params[model]['w500_hist'])
#         plt.ylabel('Frequency')
#         plt.xlabel('Circulation Regime ($\omega$500, hPa day$^{-1}$)')
#         plt.savefig('/home/users/phill/images/CIRCULATES/w500_dist_AMIP_'+model+'vs_obs'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_'+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#         plt.clf()
# #    return complete_model_list, AMIP_params_ceres_era, AMIP_params_long, AMIP4K_params, obs_data_param, obs_data
# #   Now calculate feedbacks and sensitivities
#     fixed_rad_hist_obs_param = {'lw_cre_mean': neg_exp_func_full2(w500_bins_mid, obs_data_param['LW']['A']['param'][0], obs_data_param['LW']['A']['param'][1], obs_data_param['LW']['A']['param'][2], obs_data_param['LW']['A']['param'][3]),
#                                 'sw_cre_mean' : neg_exp_func_full2(w500_bins_mid, obs_data_param['SW']['A']['param'][0], obs_data_param['SW']['A']['param'][1], obs_data_param['SW']['A']['param'][2], obs_data_param['SW']['A']['param'][3])
#                                 }
#     fixed_rad_hist_param = {}
#     for model in complete_model_list:
#         print('model=', model)
#         for rad in [net_cre_dynamic, net_cre_thermodynamic, net_cre_co_variation,sw_cre_dynamic, sw_cre_thermodynamic, sw_cre_co_variation, lw_cre_dynamic, lw_cre_thermodynamic, lw_cre_co_variation, net_cre_dynamic_param, net_cre_thermodynamic_param, net_cre_co_variation_param, sw_cre_dynamic_param, sw_cre_thermodynamic_param, sw_cre_co_variation_param, lw_cre_dynamic_param, lw_cre_thermodynamic_param, lw_cre_co_variation_param, net_cre_dynamic_obs, net_cre_thermodynamic_obs, net_cre_co_variation_obs, sw_cre_dynamic_obs, sw_cre_thermodynamic_obs, sw_cre_co_variation_obs, lw_cre_dynamic_obs, lw_cre_thermodynamic_obs, lw_cre_co_variation_obs]:
#             rad.update({model : []})
#         fixed_rad_hist_param[model] = {'lw_cre_mean': neg_exp_func_full2(w500_bins_mid, AMIP_params_long[model]['LW']['A']['param'][0], AMIP_params_long[model]['LW']['A']['param'][1], AMIP_params_long[model]['LW']['A']['param'][2], AMIP_params_long[model]['LW']['A']['param'][3]),
#                                 'sw_cre_mean' : neg_exp_func_full2(w500_bins_mid, AMIP_params_long[model]['SW']['A']['param'][0], AMIP_params_long[model]['SW']['A']['param'][1], AMIP_params_long[model]['SW']['A']['param'][2], AMIP_params_long[model]['SW']['A']['param'][3])
#                                }
#         net_cre_dynamic_feedback[model], net_cre_thermodynamic_feedback[model], net_cre_co_variation_feedback[model], sw_cre_dynamic_feedback[model], sw_cre_thermodynamic_feedback[model], sw_cre_co_variation_feedback[model], lw_cre_dynamic_feedback[model], lw_cre_thermodynamic_feedback[model], lw_cre_co_variation_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model])
#         net_cre_dynamic_obs_param_feedback[model], net_cre_thermodynamic_obs_param_feedback[model], net_cre_co_variation_obs_param_feedback[model], sw_cre_dynamic_obs_param_feedback[model], sw_cre_thermodynamic_obs_param_feedback[model], sw_cre_co_variation_obs_param_feedback[model], lw_cre_dynamic_obs_param_feedback[model], lw_cre_thermodynamic_obs_param_feedback[model], lw_cre_co_variation_obs_param_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=fixed_rad_hist_obs_param, fixed_w500_hist=obs_data['Ann']['w500_hist']/obs_data['Ann']['w500_hist'].sum())
# #        net_cre_dynamic_param_feedback[model], net_cre_thermodynamic_param_feedback[model], net_cre_co_variation_param_feedback[model], sw_cre_dynamic_param_feedback[model], sw_cre_thermodynamic_param_feedback[model], sw_cre_co_variation_param_feedback[model], lw_cre_dynamic_param_feedback[model], lw_cre_thermodynamic_param_feedback[model], lw_cre_co_variation_param_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=fixed_rad_hist_obs_param, fixed_w500_hist=obs_data['Ann']['w500_hist']/obs_data['Ann']['w500_hist'].sum())
#         net_cre_dynamic_obs_feedback[model], net_cre_thermodynamic_obs_feedback[model], net_cre_co_variation_obs_feedback[model], sw_cre_dynamic_obs_feedback[model], sw_cre_thermodynamic_obs_feedback[model], sw_cre_co_variation_obs_feedback[model], lw_cre_dynamic_obs_feedback[model], lw_cre_thermodynamic_obs_feedback[model], lw_cre_co_variation_obs_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=obs_data['Ann'], fixed_w500_hist=obs_data['Ann']['w500_hist']/obs_data['Ann']['w500_hist'].sum())
#         net_cre_dynamic_era5_feedback[model], net_cre_thermodynamic_era5_feedback[model], net_cre_co_variation_era5_feedback[model], sw_cre_dynamic_era5_feedback[model], sw_cre_thermodynamic_era5_feedback[model], sw_cre_co_variation_era5_feedback[model], lw_cre_dynamic_era5_feedback[model], lw_cre_thermodynamic_era5_feedback[model], lw_cre_co_variation_era5_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=era5_vs_ceres_two_deg_monthly['Ann'], fixed_w500_hist=era5_vs_ceres_two_deg_monthly['Ann']['w500_hist']/era5_vs_ceres_two_deg_monthly['Ann']['w500_hist'].sum())
#         net_cre_dynamic_merra2_feedback[model], net_cre_thermodynamic_merra2_feedback[model], net_cre_co_variation_merra2_feedback[model], sw_cre_dynamic_merra2_feedback[model], sw_cre_thermodynamic_merra2_feedback[model], sw_cre_co_variation_merra2_feedback[model], lw_cre_dynamic_merra2_feedback[model], lw_cre_thermodynamic_merra2_feedback[model], lw_cre_co_variation_merra2_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=merra2_vs_ceres_two_deg_monthly['Ann'], fixed_w500_hist=merra2_vs_ceres_two_deg_monthly['Ann']['w500_hist']/merra2_vs_ceres_two_deg_monthly['Ann']['w500_hist'].sum())
#         net_cre_dynamic_jra55_feedback[model], net_cre_thermodynamic_jra55_feedback[model], net_cre_co_variation_jra55_feedback[model], sw_cre_dynamic_jra55_feedback[model], sw_cre_thermodynamic_jra55_feedback[model], sw_cre_co_variation_jra55_feedback[model], lw_cre_dynamic_jra55_feedback[model], lw_cre_thermodynamic_jra55_feedback[model], lw_cre_co_variation_jra55_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=jra55_vs_ceres_two_deg_monthly['Ann'], fixed_w500_hist=jra55_vs_ceres_two_deg_monthly['Ann']['w500_hist']/jra55_vs_ceres_two_deg_monthly['Ann']['w500_hist'].sum())
#     sw_cre_dynamic_obs_feedback_err, sw_cre_thermodynamic_obs_feedback_err, sw_cre_sum_obs_feedback_err, lw_cre_dynamic_obs_feedback_err, lw_cre_thermodynamic_obs_feedback_err, lw_cre_sum_obs_feedback_err, net_cre_dynamic_obs_feedback_err, net_cre_thermodynamic_obs_feedback_err, net_cre_sum_obs_feedback_err= ({} for __ in range(9))
#     for k in complete_model_list:
#         sw_cre_dynamic_obs_feedback_err[k] = [sw_cre_dynamic_obs_feedback[k]-np.min([sw_cre_dynamic_jra55_feedback[k], sw_cre_dynamic_era5_feedback[k], sw_cre_dynamic_merra2_feedback[k], sw_cre_dynamic_obs_feedback[k]]), np.max([sw_cre_dynamic_jra55_feedback[k], sw_cre_dynamic_era5_feedback[k], sw_cre_dynamic_merra2_feedback[k], sw_cre_dynamic_obs_feedback[k]])-sw_cre_dynamic_obs_feedback[k]]
#         sw_cre_thermodynamic_obs_feedback_err[k] = [sw_cre_thermodynamic_obs_feedback[k]-np.min([sw_cre_thermodynamic_jra55_feedback[k], sw_cre_thermodynamic_era5_feedback[k], sw_cre_thermodynamic_merra2_feedback[k], sw_cre_thermodynamic_obs_feedback[k]]), np.max([sw_cre_thermodynamic_jra55_feedback[k], sw_cre_thermodynamic_era5_feedback[k], sw_cre_thermodynamic_merra2_feedback[k], sw_cre_thermodynamic_obs_feedback[k]])-sw_cre_thermodynamic_obs_feedback[k]]
#         sw_cre_sum_obs_feedback_err[k] = [sw_cre_dynamic_obs_feedback[k]+sw_cre_thermodynamic_obs_feedback[k]-np.min([sw_cre_dynamic_jra55_feedback[k]+sw_cre_thermodynamic_jra55_feedback[k], sw_cre_dynamic_era5_feedback[k]+sw_cre_thermodynamic_era5_feedback[k], sw_cre_dynamic_merra2_feedback[k]+sw_cre_thermodynamic_merra2_feedback[k], sw_cre_dynamic_obs_feedback[k]+sw_cre_thermodynamic_obs_feedback[k]]), np.max([sw_cre_dynamic_jra55_feedback[k]+sw_cre_thermodynamic_jra55_feedback[k], sw_cre_dynamic_era5_feedback[k]+sw_cre_thermodynamic_era5_feedback[k], sw_cre_dynamic_merra2_feedback[k]+sw_cre_thermodynamic_merra2_feedback[k], sw_cre_dynamic_obs_feedback[k]+sw_cre_thermodynamic_obs_feedback[k]])-(sw_cre_dynamic_obs_feedback[k]+sw_cre_thermodynamic_obs_feedback[k])]
#         lw_cre_dynamic_obs_feedback_err[k] = [lw_cre_dynamic_obs_feedback[k]-np.min([lw_cre_dynamic_jra55_feedback[k], lw_cre_dynamic_era5_feedback[k], lw_cre_dynamic_merra2_feedback[k], lw_cre_dynamic_obs_feedback[k]]), np.max([lw_cre_dynamic_jra55_feedback[k], lw_cre_dynamic_era5_feedback[k], lw_cre_dynamic_merra2_feedback[k], lw_cre_dynamic_obs_feedback[k]])-lw_cre_dynamic_obs_feedback[k]]
#         lw_cre_thermodynamic_obs_feedback_err[k] = [lw_cre_thermodynamic_obs_feedback[k]-np.min([lw_cre_thermodynamic_jra55_feedback[k], lw_cre_thermodynamic_era5_feedback[k], lw_cre_thermodynamic_merra2_feedback[k], lw_cre_thermodynamic_obs_feedback[k]]), np.max([lw_cre_thermodynamic_jra55_feedback[k], lw_cre_thermodynamic_era5_feedback[k], lw_cre_thermodynamic_merra2_feedback[k], lw_cre_thermodynamic_obs_feedback[k]])-lw_cre_thermodynamic_obs_feedback[k]]
#         lw_cre_sum_obs_feedback_err[k] = [lw_cre_dynamic_obs_feedback[k]+lw_cre_thermodynamic_obs_feedback[k]-np.min([lw_cre_dynamic_jra55_feedback[k]+lw_cre_thermodynamic_jra55_feedback[k], lw_cre_dynamic_era5_feedback[k]+lw_cre_thermodynamic_era5_feedback[k], lw_cre_dynamic_merra2_feedback[k]+lw_cre_thermodynamic_merra2_feedback[k], lw_cre_dynamic_obs_feedback[k]+lw_cre_thermodynamic_obs_feedback[k]]), np.max([lw_cre_dynamic_jra55_feedback[k]+lw_cre_thermodynamic_jra55_feedback[k], lw_cre_dynamic_era5_feedback[k]+lw_cre_thermodynamic_era5_feedback[k], lw_cre_dynamic_merra2_feedback[k]+lw_cre_thermodynamic_merra2_feedback[k], lw_cre_dynamic_obs_feedback[k]+lw_cre_thermodynamic_obs_feedback[k]])-(lw_cre_dynamic_obs_feedback[k]+lw_cre_thermodynamic_obs_feedback[k])]
#         net_cre_dynamic_obs_feedback_err[k] = [net_cre_dynamic_obs_feedback[k]-np.min([net_cre_dynamic_jra55_feedback[k], net_cre_dynamic_era5_feedback[k], net_cre_dynamic_merra2_feedback[k], net_cre_dynamic_obs_feedback[k]]), np.max([net_cre_dynamic_jra55_feedback[k], net_cre_dynamic_era5_feedback[k], net_cre_dynamic_merra2_feedback[k], net_cre_dynamic_obs_feedback[k]])-net_cre_dynamic_obs_feedback[k]]
#         net_cre_thermodynamic_obs_feedback_err[k] = [net_cre_thermodynamic_obs_feedback[k]-np.min([net_cre_thermodynamic_jra55_feedback[k], net_cre_thermodynamic_era5_feedback[k], net_cre_thermodynamic_merra2_feedback[k], net_cre_thermodynamic_obs_feedback[k]]), np.max([net_cre_thermodynamic_jra55_feedback[k], net_cre_thermodynamic_era5_feedback[k], net_cre_thermodynamic_merra2_feedback[k], net_cre_thermodynamic_obs_feedback[k]])-net_cre_thermodynamic_obs_feedback[k]]
#         net_cre_sum_obs_feedback_err[k] = [net_cre_dynamic_obs_feedback[k]+net_cre_thermodynamic_obs_feedback[k]-np.min([net_cre_dynamic_jra55_feedback[k]+net_cre_thermodynamic_jra55_feedback[k], net_cre_dynamic_era5_feedback[k]+net_cre_thermodynamic_era5_feedback[k], net_cre_dynamic_merra2_feedback[k]+net_cre_thermodynamic_merra2_feedback[k], net_cre_dynamic_obs_feedback[k]+net_cre_thermodynamic_obs_feedback[k]]), np.max([net_cre_dynamic_jra55_feedback[k]+net_cre_thermodynamic_jra55_feedback[k], net_cre_dynamic_era5_feedback[k]+net_cre_thermodynamic_era5_feedback[k], net_cre_dynamic_merra2_feedback[k]+net_cre_thermodynamic_merra2_feedback[k], net_cre_dynamic_obs_feedback[k]+net_cre_thermodynamic_obs_feedback[k]])-(net_cre_dynamic_obs_feedback[k]+net_cre_thermodynamic_obs_feedback[k])]
# #   Get global mean feedback for each model in order to calculate ECS perturbation.
#     net_feedback, olr_amip, osr_amip, olr_4k, osr_4k = calc_global_feedback()
#     ecs_old, ecs_new, ecs_new_lower, ecs_new_upper = {}, {}, {}, {}
#     for model in complete_model_list:
#         ecs_old[model] = 4.0/net_feedback[model]
#         ecs_new[model] = 4.0/(net_feedback[model]+0.5*((net_cre_dynamic_obs_feedback[model]+net_cre_thermodynamic_obs_feedback[model])-(net_cre_dynamic_feedback[model]+net_cre_thermodynamic_feedback[model])))
#         ecs_new_lower[model] = 4.0/(net_feedback[model]+0.5*((net_cre_dynamic_obs_feedback[model]+net_cre_thermodynamic_obs_feedback[model]-net_cre_sum_obs_feedback_err[model][0])-(net_cre_dynamic_feedback[model]+net_cre_thermodynamic_feedback[model])))
#         ecs_new_upper[model] = 4.0/(net_feedback[model]+0.5*((net_cre_dynamic_obs_feedback[model]+net_cre_thermodynamic_obs_feedback[model]+net_cre_sum_obs_feedback_err[model][0])-(net_cre_dynamic_feedback[model]+net_cre_thermodynamic_feedback[model])))
# #    Now compare feedbacks from model directly to feedbacks from fit for each model
# #    return complete_model_list, w500_bins_mid, obs_data['Ann'], AMIP_params_long, AMIP4K_params, net_cre_dynamic_feedback, net_cre_thermodynamic_feedback, net_cre_co_variation_feedback, w500_bins, cre_bins, lon_min, lon_max, lat_min, lat_max
#     plot_linearised_obs_feedback(complete_model_list, w500_bins_mid, obs_data['Ann'], AMIP_params_long, AMIP4K_params, net_cre_dynamic_feedback, net_cre_thermodynamic_feedback, net_cre_co_variation_feedback, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=-30, lat_max=30)
#     plot_decomposition_comparison(complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_feedback, ylabel='SW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalSW_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, sw_cre_dynamic_param_err=sw_cre_dynamic_obs_feedback_err, sw_cre_thermodynamic_param_err=sw_cre_thermodynamic_obs_feedback_err, sw_cre_sum_param_err=sw_cre_sum_obs_feedback_err)
#     plot_decomposition_comparison_v2(complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_feedback, title='SW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalSW_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison(complete_model_list, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_feedback, ylabel='LW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalLW_cre_feedback_AMIP'+'w500bin_width', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, sw_cre_dynamic_param_err=lw_cre_dynamic_obs_feedback_err, sw_cre_thermodynamic_param_err=lw_cre_thermodynamic_obs_feedback_err, sw_cre_sum_param_err=lw_cre_sum_obs_feedback_err)
#     plot_decomposition_comparison_v2(complete_model_list, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_feedback, title='LW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalLW_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_feedback, ylabel='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalNet_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, sw_cre_dynamic_param_err=net_cre_dynamic_obs_feedback_err, sw_cre_thermodynamic_param_err=net_cre_thermodynamic_obs_feedback_err, sw_cre_sum_param_err=net_cre_sum_obs_feedback_err)
#     plot_decomposition_comparison(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_feedback, ylabel='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalNet_cre_feedback_AMIP_no_err', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dyn.', 'dyn. obs', 'therm.', 'therm. obs', 'co-variation', 'sum', 'sum obs'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison_v2(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_feedback, title='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_decomposition_evalNet_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison(complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_param_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_param_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_param_feedback, ylabel='SW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_param_decomposition_evalSW_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'dynamic obs_param', 'thermo', 'thermo obs_param', 'co-variation', 'sum', 'sum obs_param'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison_v2(complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_param_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_param_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_param_feedback, title='SW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_param_decomposition_evalSW_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, ylabel='Param Obs feedback (W m$^{-2}$)')
#     plot_decomposition_comparison(complete_model_list, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_param_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_param_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_param_feedback, ylabel='LW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_param_decomposition_evalLW_cre_feedbacl_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'dynamic obs_param', 'thermodynamic', 'thermodynamic obs_param', 'co-variation', 'sum', 'sum obs_param'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison_v2(complete_model_list, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_param_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_param_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_param_feedback, title='LW cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_param_decomposition_evalLW_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, ylabel='Param Obs feedback (W m$^{-2}$)')
#     plot_decomposition_comparison(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_param_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_param_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_param_feedback, ylabel='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_param_decomposition_evalNet_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'dynamic obs_param', 'thermodynamic', 'thermodynamic obs_param', 'co-variation', 'sum', 'sum obs_param'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max)
#     plot_decomposition_comparison_v2(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_obs_param_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_param_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_param_feedback, title='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='obs_param_decomposition_evalNet_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dynamic', 'thermo', 'sum'], lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, ylabel='Param Obs feedback (W m$^{-2}$)')
# #    plot_feedback_relationship_correlations(complete_model_list, mean_sw_cre_dynamic, mean_sw_cre_dynamic_obs, mean_sw_cre_thermodynamic, mean_sw_cre_thermodynamic_obs, mean_sw_cre_co_variation, mean_sw_cre_co_variation_obs)
#     plot_delta_feedback_vs_delta_parameter(AMIP_params_long, obs_data_param, lw_cre_dynamic_obs_feedback, lw_cre_dynamic_feedback, complete_model_list, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_delta_feedback_vs_delta_parameter(AMIP_params_long, obs_data_param, sw_cre_dynamic_obs_feedback, sw_cre_dynamic_feedback, complete_model_list, region_param='SW', region='SW', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_delta_feedback_vs_delta_parameter(AMIP_params_long, obs_data_param, net_cre_dynamic_obs_feedback, net_cre_dynamic_feedback, complete_model_list, region_param='SW', region='Net', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_delta_feedback_vs_delta_parameter(AMIP_params_long, obs_data_param, net_cre_dynamic_obs_feedback, net_cre_dynamic_feedback, complete_model_list, region_param='LW', region='Net', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_model_feedbacks_vs_w500(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_model_feedbacks_vs_w500_v2(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_model_feedbacks_vs_w500_v3(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     plot_model_feedbacks_vs_w500_v4(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, w500_bins=w500_bins, cre_bins=cre_bins)
#     return complete_model_list, sw_cre_dynamic_feedback, sw_cre_dynamic_obs_feedback, sw_cre_thermodynamic_feedback, sw_cre_thermodynamic_obs_feedback, sw_cre_co_variation_feedback, sw_cre_co_variation_obs_feedback, lw_cre_dynamic_feedback, lw_cre_dynamic_obs_feedback, lw_cre_thermodynamic_feedback, lw_cre_thermodynamic_obs_feedback, lw_cre_co_variation_feedback, lw_cre_co_variation_obs_feedback, net_cre_dynamic_feedback, net_cre_dynamic_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_obs_feedback, obs_data, obs_data_param, AMIP_params_long, AMIP4K_params, fixed_rad_hist_param, fixed_rad_hist_obs_param, net_cre_dynamic_era5_feedback, net_cre_thermodynamic_era5_feedback, net_cre_co_variation_era5_feedback,sw_cre_dynamic_era5_feedback, sw_cre_thermodynamic_era5_feedback, sw_cre_co_variation_era5_feedback, lw_cre_dynamic_era5_feedback, lw_cre_thermodynamic_era5_feedback, lw_cre_co_variation_era5_feedback, net_cre_dynamic_merra2_feedback, net_cre_thermodynamic_merra2_feedback, net_cre_co_variation_merra2_feedback,sw_cre_dynamic_merra2_feedback, sw_cre_thermodynamic_merra2_feedback, sw_cre_co_variation_merra2_feedback, lw_cre_dynamic_merra2_feedback, lw_cre_thermodynamic_merra2_feedback, lw_cre_co_variation_merra2_feedback, net_cre_dynamic_jra55_feedback, net_cre_thermodynamic_jra55_feedback, net_cre_co_variation_jra55_feedback,sw_cre_dynamic_jra55_feedback, sw_cre_thermodynamic_jra55_feedback, sw_cre_co_variation_jra55_feedback, lw_cre_dynamic_jra55_feedback, lw_cre_thermodynamic_jra55_feedback, lw_cre_co_variation_jra55_feedback, ecs_old, ecs_new, ecs_new_upper, ecs_new_lower


# def plot_linearised_obs_feedback(complete_model_list, w500_bins_mid, obs_data, AMIP_params_long, AMIP4K_params, net_cre_dynamic_feedback, net_cre_thermodynamic_feedback, net_cre_co_variation_feedback, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30):
#     '''
#     Plot observationally constrained dynamic feedback if it is linearsied

#     Demonstrates that it is the nonlinearity between 0 and 30 hPa day-1 that
#     causes the increase in the dynamic feedback with observational constraints
#     '''
#     start_linear=np.where(w500_bins_mid <= 0.)[0][-1] # 0 hPa day-1
#     end_linear=np.where(w500_bins_mid >= 30.)[0][0] # 30 hPa day-1
#     n_pts = obs_data['sw_cre_adj2_mean'].size
#     linearised_obs_data = {'sw_cre_adj2_mean' :np.concatenate((obs_data['sw_cre_adj2_mean'][:start_linear],np.interp(np.arange(start_linear,end_linear), np.concatenate((np.arange(start_linear),np.arange(end_linear,n_pts))), np.concatenate((obs_data['sw_cre_adj2_mean'][:start_linear], obs_data['sw_cre_adj2_mean'][end_linear:]))),obs_data['sw_cre_adj2_mean'][end_linear:n_pts]))}
#     linearised_obs_data['sw_cre_mean'] = linearised_obs_data['sw_cre_adj2_mean']
#     linearised_obs_data['lw_cre_mean'] = obs_data['lw_cre_adj2_mean']
#     AMIP_params_long['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                             'sw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                             'sw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                             'lw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in complete_model_list]), axis=0),
#                                             'lw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                            }
#     AMIP4K_params['multi_model_mean'] = {'w500_hist' : np.array([AMIP4K_params[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                          'sw_cre_adj2_mean' : np.nanmean(np.array([AMIP4K_params[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                          'sw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                          'lw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['lw_cre_mean'] for model in complete_model_list]), axis=0),
#                                          'lw_cre_adj2_mean' : np.nanmean(np.array([AMIP4K_params[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                            }
#     net_cre_dynamic_linearised_obs_feedback, net_cre_thermodynamic_linearised_obs_feedback, net_cre_co_variation_linearised_obs_feedback, sw_cre_dynamic_linearised_obs_feedback, sw_cre_thermodynamic_linearised_obs_feedback, sw_cre_co_variation_linearised_obs_feedback, lw_cre_dynamic_linearised_obs_feedback, lw_cre_thermodynamic_linearised_obs_feedback, lw_cre_co_variation_linearised_obs_feedback = ({} for __ in range(9))
#     for model in complete_model_list:
#         net_cre_dynamic_linearised_obs_feedback[model], net_cre_thermodynamic_linearised_obs_feedback[model], net_cre_co_variation_linearised_obs_feedback[model], sw_cre_dynamic_linearised_obs_feedback[model], sw_cre_thermodynamic_linearised_obs_feedback[model], sw_cre_co_variation_linearised_obs_feedback[model], lw_cre_dynamic_linearised_obs_feedback[model], lw_cre_thermodynamic_linearised_obs_feedback[model], lw_cre_co_variation_linearised_obs_feedback[model] = decompose_rad_cess(AMIP_params_long[model], AMIP4K_params[model], fixed_rad_hist=linearised_obs_data, fixed_w500_hist=obs_data['w500_hist']/obs_data['w500_hist'].sum())   
#     plt.clf()
#     fig = plt.figure(9, figsize=(6,6))
#     plot_circ_cloud_relationships(w500_bins, cre_bins, obs_data, linearised_obs_data, AMIP_params_long['multi_model_mean'], labels=['Obs', 'Linearised Obs', 'AMIP 1979-2014', ''], list_of_colors=[colorlist[3], colorlist[0], colorlist[1], colorlist[2]], var='sw_cre_adj2_mean', fig=fig, subplot_index=221, panel='(a)', lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, show_legend=True, savename='/home/users/phill/images/CIRCULATES/w500_dist_and_cre_vs_obs')
#     ax = fig.add_subplot(222)
#     plt.scatter(w500_bins_mid, (((AMIP4K_params['multi_model_mean']['w500_hist']-AMIP_params_long['multi_model_mean']['w500_hist'])/4.)*(linearised_obs_data['sw_cre_mean']-AMIP_params_long['multi_model_mean']['sw_cre_mean']))/AMIP_params_long['multi_model_mean']['w500_hist'].sum(), label='SW {:.2f}'.format(np.nansum(((AMIP4K_params['multi_model_mean']['w500_hist']-AMIP_params_long['multi_model_mean']['w500_hist'])/4.)*(linearised_obs_data['sw_cre_mean']-AMIP_params_long['multi_model_mean']['sw_cre_mean'])/AMIP_params_long['multi_model_mean']['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#     plt.scatter(w500_bins_mid, (((AMIP4K_params['multi_model_mean']['w500_hist']-AMIP_params_long['multi_model_mean']['w500_hist'])/4.)*(linearised_obs_data['lw_cre_mean']-AMIP_params_long['multi_model_mean']['lw_cre_mean']))/AMIP_params_long['multi_model_mean']['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params['multi_model_mean']['w500_hist']-AMIP_params_long['multi_model_mean']['w500_hist'])/4.)*(linearised_obs_data['lw_cre_mean']-AMIP_params_long['multi_model_mean']['lw_cre_mean'])/AMIP_params_long['multi_model_mean']['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#     plt.text(0.08, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     plt.legend(loc=0)
#     plt.ylabel('Difference in dynamic\ncloud feedback (W m$^{-2}$ K$^{-1}$)')
#     plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#     plt.xlim([-150,100])
#     plt.ylim([-0.005,0.015]) # To match non-linearised axis
#     plt.grid(color='lightgrey')
#     plot_decomposition_comparison(complete_model_list, net_cre_dynamic_feedback, net_cre_dynamic_linearised_obs_feedback, net_cre_thermodynamic_feedback, net_cre_thermodynamic_linearised_obs_feedback, net_cre_co_variation_feedback, net_cre_co_variation_linearised_obs_feedback, ylabel='Net cloud feedback (W m$^{-2}$ K$^{-1}$)', savename='linearised_obs_decomposition_evalNet_cre_feedback_AMIP', w500_bins=w500_bins, cre_bins=cre_bins, leg=['dyn.', 'dyn. lin.', 'therm.', 'therm. lin.', 'co-variation', 'sum', 'sum lin.'], co_variation2=False, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, fig=fig, subplot_index=212, text='(c)')

    
# def make_table(w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), n_bootstrap=2, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, seed=1, spatial_av_scale=2.0, time_av_scale=24*30):
#     '''
#     Print model names and properties in format of latex table
 
#     Should be suitable for copying straight into latex file.
#     '''
#     model_list = [k for k in amip_dict.keys() if k in amip_p4k_dict.keys()]
#     model_list.sort(key=lambda s: s.lower())
#     AMIP_params = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=n_bootstrap, seed=seed, time_av_scale=time_av_scale, yearlist=range(1979,2015))
#     w500_bins_mid = 0.5*(w500_bins[:-1] + w500_bins[1:])
#     era5_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source='CERES_EBAF', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=range(2001,2015))
#     jra55_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source='CERES_EBAF', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=range(2001,2015))
#     merra2_vs_ceres_two_deg_monthly = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source='CERES_EBAF', w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=range(2001,2015))
#     whist = merra2_vs_ceres_two_deg_monthly['Ann']['w500_hist'] + era5_vs_ceres_two_deg_monthly['Ann']['w500_hist'] + jra55_vs_ceres_two_deg_monthly['Ann']['w500_hist']
#     circ_intensity_obs = (whist*w500_bins_mid)[w500_bins_mid > 0.].sum()/whist[w500_bins_mid > 0].sum()-(whist*w500_bins_mid)[w500_bins_mid < 0.].sum()/whist[w500_bins_mid < 0].sum()
#     sw_cre_obs = np.nansum(merra2_vs_ceres_two_deg_monthly['Ann']['sw_cre_adj2_mean']*merra2_vs_ceres_two_deg_monthly['Ann']['w500_hist']+era5_vs_ceres_two_deg_monthly['Ann']['sw_cre_adj2_mean']*era5_vs_ceres_two_deg_monthly['Ann']['w500_hist']+jra55_vs_ceres_two_deg_monthly['Ann']['sw_cre_adj2_mean']*jra55_vs_ceres_two_deg_monthly['Ann']['w500_hist'])/whist.sum()
#     lw_cre_obs = np.nansum(merra2_vs_ceres_two_deg_monthly['Ann']['lw_cre_adj2_mean']*merra2_vs_ceres_two_deg_monthly['Ann']['w500_hist']+era5_vs_ceres_two_deg_monthly['Ann']['lw_cre_adj2_mean']*era5_vs_ceres_two_deg_monthly['Ann']['w500_hist']+jra55_vs_ceres_two_deg_monthly['Ann']['lw_cre_adj2_mean']*jra55_vs_ceres_two_deg_monthly['Ann']['w500_hist'])/whist.sum()
#     circ_intensity, sw_cre, lw_cre = [], [], []
#     for model in model_list:
#         whist = AMIP_params[model]['w500_hist']
#         circ_intensity += [(whist*w500_bins_mid)[w500_bins_mid > 0.].sum()/whist[w500_bins_mid > 0].sum()-(whist*w500_bins_mid)[w500_bins_mid < 0.].sum()/whist[w500_bins_mid < 0].sum()] # Note this is slightly different to definition used elsewhere, but matches literature.
#         sw_cre += [np.nansum(AMIP_params[model]['sw_cre_mean']*whist)/whist.sum()]
#         lw_cre += [np.nansum(AMIP_params[model]['lw_cre_mean']*whist)/whist.sum()]
#         filename_amip = amip_dict[model]
#         id = filename_amip.index('/amip/')
#         member_amip = filename_amip[id+6:id+14]
#         filename_amip4K = amip_p4k_dict[model]
#         id = filename_amip4K.index('/amip-p4K/')
#         member_amip4K = filename_amip4K[id+10:id+18]
# #        print('{:<16}'.format(model)+'& '+'{:<10}'.format(member_amip)+'& '+'{:<10}'.format(member_amip4K))
#         print('{:<16}'.format(model)+'& '+'{:<10}'.format(member_amip)+'& '+'{:.1f}'.format(cmip6_resolution[model][0])+'\\textdegree $\\times${:.1f}'.format(cmip6_resolution[model][1])+'\\textdegree & {:<2}'.format(cmip6_resolution[model][2])+' & {:.1f}'.format(circ_intensity[-1])+' & {:.1f}'.format(lw_cre[-1])+'& {:.1f}'.format(sw_cre[-1])+' \\\ ')
#     print('Multi-model mean & {:.1f}'.format(np.mean(circ_intensity))+' & {:.1f}'.format(np.mean(lw_cre))+'& {:.1f}'.format(np.mean(sw_cre))+' \\\ ')
#     print('Observations (Reanalyses and CERES-EBAF) & {:.1f}'.format(circ_intensity_obs)+' & {:.1f}'.format(lw_cre_obs)+'& {:.1f}'.format(sw_cre_obs)+' \\\ ')
   


# def plot_model_feedbacks_vs_w500(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=True, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, method='AMIP', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
#     '''
#     Plot thermodynamic and dynamic feedbacks vs w500 for each model.
#     '''

#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
# #   Add multi-model means to complete_model_list
#     AMIP4K_params['multi_model_mean'] = {'w500_hist' : np.array([AMIP4K_params[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                          'sw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                          'lw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                          }
#     AMIP_params_long['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                             'sw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                             'lw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                          }
#     fixed_rad_hist_param['multi_model_mean'] = {'sw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                 'lw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                          }
#     complete_model_list += ['multi_model_mean']
#     for kk,model in enumerate(complete_model_list):
#         fig = plt.figure(0, figsize=(10.0,5.4)) # Plot distributions of w500, SW and LW CRE vs w500 and delta for model, obs, obs param and model param
#         ax = fig.add_subplot(231)
#         plt.scatter(w500_bins_mid, obs_data['Ann']['w500_hist']/obs_data['Ann']['w500_hist'].sum(), s=5, facecolors='none', edgecolors=colorlist[0], label='Obs {:.2f}'.format((obs_data['Ann']['w500_hist']*abs(w500_bins_mid)).sum()/obs_data['Ann']['w500_hist'].sum()))
#         plt.scatter(w500_bins_mid, AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum(), s=5, facecolors='none', edgecolors=colorlist[1], label='AMIP+4K {:.2f}'.format((AMIP4K_params[model]['w500_hist']*abs(w500_bins_mid)).sum()/AMIP4K_params[model]['w500_hist'].sum()))
#         plt.scatter(w500_bins_mid, AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum(), s=5, facecolors='none', edgecolors=colorlist[2], label='AMIP {:.2f}'.format((AMIP_params_long[model]['w500_hist']*abs(w500_bins_mid)).sum()/AMIP_params_long[model]['w500_hist'].sum()))
#         plt.legend(loc=0)
#         plt.title(model +'('+chr(ord('a')+kk)+')')
#         plt.ylabel('Frequency')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-300,150])
#         plt.grid(color='lightgrey')
#         ax = fig.add_subplot(234)
#         plt.scatter(w500_bins_mid, (obs_data['Ann']['w500_hist']/obs_data['Ann']['w500_hist'].sum()) - (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors=colorlist[0], label='Obs-AMIP')
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors=colorlist[1], label='AMIP4K-AMIP')
#         plt.legend(loc=0)
#         plt.title(model +'('+chr(ord('a')+kk)+')')
#         plt.ylabel('Change in frequency')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-300,150])
#         plt.grid(color='lightgrey')
#         for ii, (region, cre_mean) in enumerate(zip(['SW', 'LW'], ['sw_cre_mean', 'lw_cre_mean'])):
#             ax = fig.add_subplot(230+ii+2)
#             plt.scatter(w500_bins_mid, obs_data['Ann'][cre_mean], s=5, facecolors='none', edgecolors=colorlist[0], label='Obs {:.2f}'.format(np.nansum(obs_data['Ann'][cre_mean])/obs_data['Ann']['w500_hist'].sum()))
#             plt.scatter(w500_bins_mid, AMIP4K_params[model][cre_mean], s=5, facecolors='none', edgecolors=colorlist[1], label='AMIP+4K {:.2f}'.format(np.nansum(AMIP4K_params[model][cre_mean])/AMIP4K_params[model]['w500_hist'].sum()))
#             plt.scatter(w500_bins_mid, AMIP_params_long[model][cre_mean], s=5, facecolors='none', edgecolors=colorlist[2], label='AMIP {:.2f}'.format(np.nansum(AMIP_params_long[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum()))
#             plt.legend(loc=0)
#             plt.title(model +'('+chr(ord('a')+kk)+')')
#             plt.ylabel('Mean '+region+' CRE (W m$^{-2}$)')
#             plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#             plt.xlim([-300,150])
#             plt.grid(color='lightgrey')
#             ax = fig.add_subplot(230+ii+5)
#             plt.scatter(w500_bins_mid, obs_data['Ann'][cre_mean]-AMIP_params_long[model][cre_mean], s=5, facecolors='none', edgecolors=colorlist[0], label='Obs-AMIP')
#             plt.scatter(w500_bins_mid, AMIP4K_params[model][cre_mean]-AMIP_params_long[model][cre_mean], s=5, facecolors='none', edgecolors=colorlist[1], label='AMIP4K-AMIP')
#             plt.legend(loc=0)
#             plt.title(model +'('+chr(ord('a')+kk)+')')
#             plt.ylabel('Change in '+region+' CRE (W m$^{-2}$)')
#             plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#             plt.xlim([-300,150])
#             plt.grid(color='lightgrey')
#         fig.tight_layout()
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_'+model+'_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+plot_type)
#         fig = plt.figure(1, figsize=(10.0,5.4)) # PLot dynamic effect as fn of w500 and deltas for SW, LW and net for model, obs constrained model, param model, param obs constrained model
#         for ii, (region, cre_mean) in enumerate(zip(['SW', 'LW'], ['sw_cre_mean', 'lw_cre_mean'])):
#             ax = fig.add_subplot(220+ii+1)
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Model {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())), s=5, facecolors='none', edgecolors=colorlist[0])
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann'][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Obs {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann'][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())), s=5, facecolors='none', edgecolors=colorlist[1])
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(fixed_rad_hist_param[model][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Par Model {:.2f}'.format(np.nansum( ((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(fixed_rad_hist_param[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())), s=5, facecolors='none', edgecolors=colorlist[2])
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(fixed_rad_hist_obs_param[cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Par Obs {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(fixed_rad_hist_obs_param[cre_mean])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[3])
#             plt.legend(loc=0)
#             plt.title(model +'('+chr(ord('a')+kk)+')')
#             plt.ylabel(region+' Dynamic feedback (W m$^{-2}$ K$^{-1}$)')
#             plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#             plt.xlim([-300,150])
#             plt.grid(color='lightgrey')
#             ax = fig.add_subplot(220+ii+3)
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann'][cre_mean]-AMIP_params_long[model][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Obs-Model {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann'][cre_mean]-AMIP_params_long[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann'][cre_mean]-fixed_rad_hist_param[model][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Obs-Par Model {:.2f}'.format(np.nansum((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])*(obs_data['Ann'][cre_mean]-fixed_rad_hist_param[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(fixed_rad_hist_obs_param[cre_mean]-AMIP_params_long[model][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Par Obs-Model {:.2f}'.format(np.nansum((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])*(fixed_rad_hist_obs_param[cre_mean]-AMIP_params_long[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[2])
#             plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(fixed_rad_hist_obs_param[cre_mean]-fixed_rad_hist_param[model][cre_mean]))/AMIP_params_long[model]['w500_hist'].sum(), label='Par Obs-Par Model {:.2f}'.format(np.nansum((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])*(fixed_rad_hist_obs_param[cre_mean]-fixed_rad_hist_param[model][cre_mean])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[3])
#             plt.legend(loc=0)
#             plt.title(model +'('+chr(ord('a')+kk)+')')
#             plt.ylabel(region+' Dynamic feedback difference (W m$^{-2}$ K$^{-1}$)')
#             plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#             plt.xlim([-150,100])
#             plt.grid(color='lightgrey')
#         fig.tight_layout()
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+model+'_dynamic_feedback_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+plot_type)
#         if show_plots:
#            plt.show()
#         else:
#             plt.close('all')

        
# def plot_model_feedbacks_vs_w500_cmip6(complete_model_list, w500_bins_mid, abrupt4co2_regional_mean_w500_dist, picontrol_w500_hist, abrupt4co2_global_mean_ts, picontrol_global_mean_ts, obs_data_ann, picontrol_sw_cre_sum, picontrol_lw_cre_sum, show_plots=True, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, method='AMIP', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
#     '''
#     Plot thermodynamic and dynamic feedbacks vs w500 for each model.
#     '''
#     if not 'multi_model_mean' in abrupt4co2_regional_mean_w500_dist.keys():
#         abrupt4co2_regional_mean_w500_dist['multi_model_mean'] = np.array([abrupt4co2_regional_mean_w500_dist[model] for model in complete_model_list]).mean(axis=0)
#         picontrol_w500_hist['multi_model_mean'] = np.array([picontrol_w500_hist[model] for model in complete_model_list]).mean(axis=0)
#         picontrol_sw_cre_sum['multi_model_mean'] = np.array([picontrol_sw_cre_sum[model] for model in complete_model_list]).mean(axis=0)
#         picontrol_lw_cre_sum['multi_model_mean'] = np.array([picontrol_lw_cre_sum[model] for model in complete_model_list]).mean(axis=0)
#         abrupt4co2_global_mean_ts['multi_model_mean']= np.array([abrupt4co2_global_mean_ts[model] for model in complete_model_list]).mean(axis=0)
#         picontrol_global_mean_ts['multi_model_mean']= np.array([picontrol_global_mean_ts[model] for model in complete_model_list]).mean(axis=0)
#         complete_model_list += ['multi_model_mean']
#     for kk,model in enumerate(complete_model_list):
#         global_mean_ts_anomaly = abrupt4co2_global_mean_ts[model] - picontrol_global_mean_ts[model]
#         fig = plt.figure(0, figsize=(5.0,3.5)) # Plot dynamic feedback as fn of w500 and 
#         ax = fig.add_subplot(211)
#         delta_w500 = ((abrupt4co2_regional_mean_w500_dist[model].T/abrupt4co2_regional_mean_w500_dist[model].sum(axis=1)).T-(picontrol_w500_hist[model]/picontrol_w500_hist[model].sum()))
#         w500_feedback = np.polyfit(global_mean_ts_anomaly, delta_w500,1)[0,:]
#         plt.scatter(w500_bins_mid, w500_feedback*(obs_data_ann['sw_cre_adj2_mean']-picontrol_sw_cre_sum[model]/picontrol_w500_hist[model]), s=5, facecolors='none', edgecolors=colorlist[0], label='SW {:.2f}'.format(np.nansum(w500_feedback*(obs_data_ann['sw_cre_adj2_mean']-picontrol_sw_cre_sum[model]/picontrol_w500_hist[model]))))
#         plt.scatter(w500_bins_mid, w500_feedback*(obs_data_ann['lw_cre_adj2_mean']-picontrol_lw_cre_sum[model]/picontrol_w500_hist[model]), s=5, facecolors='none', edgecolors=colorlist[1], label='LW {:.2f}'.format(np.nansum(w500_feedback*(obs_data_ann['lw_cre_adj2_mean']-picontrol_lw_cre_sum[model]/picontrol_w500_hist[model]))))
#         plt.legend(loc=0)
#         plt.ylabel('Difference in dynamic\ncloud feedback (W m$^{-2}$ K$^{-1}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.grid(color='lightgrey')
#         ax1 = fig.add_subplot(212)
#         plt.scatter(w500_bins_mid, w500_feedback, s=5, facecolors='none', edgecolors=colorlist[2], label='Freq.')
#         ax1.set_xlim([-150,100])
#         delta_w500 = w500_bins[1]-w500_bins[0]
#         ax1.set_ylim([-0.004*delta_w500,0.006*delta_w500])
#         ax1.set_yticks(np.arange(-0.004*delta_w500,0.006*delta_w500+0.00000000001, 0.002*delta_w500), color=colorlist[2])
#         ax1.set_ylabel('Frequency; abrupt4xCO2-piControl', color=colorlist[2])
#         ax1.set_xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax1.spines['left'].set_color(colorlist[2])
#         ax1.yaxis.label.set_color(colorlist[2])
#         ax1.tick_params(axis='y', colors=colorlist[2])
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, (obs_data_ann['sw_cre_adj2_mean']-picontrol_sw_cre_sum[model]/picontrol_w500_hist[model]), s=5, facecolors='none', edgecolors=colorlist[0], label='SW')
#         plt.scatter(w500_bins_mid, (obs_data_ann['lw_cre_adj2_mean']-picontrol_lw_cre_sum[model]/picontrol_w500_hist[model]), s=5, facecolors='none', edgecolors=colorlist[1], label='LW')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         ax2.legend(lines + lines2, labels + labels2, loc=3, ncol=3)
#         ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)', color='#F28D32')
# #        ax2.set_xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax2.set_xlim([-150,100])
#         ax2.set_ylim([-10,15])
#         ax2.grid(which='both', axis='both', color='lightgrey')
#         ax2.spines['right'].set_color('#F28D32')
#         ax2.spines['left'].set_color(colorlist[2])
#         ax2.yaxis.label.set_color('#F28D32')
#         ax2.tick_params(axis='y', colors='#F28D32')
#         plt.text(0.08, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.text(0.08, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
#         fig.subplots_adjust(left=0.191, right=0.869, bottom=0.12, top=0.95, wspace=0.2, hspace=0.43)
# #        fig.tight_layout() # not working nicely
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_'+model+'_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer'+plot_type)
#         if model == 'multi_model_mean':
#             plt.show()
# #        plt.show()
#         if show_plots:
#            plt.show()
#         else:
#             plt.close('all')
# #   Put all models on single plot
#     fig = plt.figure(0, figsize=(5,8))
#     for kk in range(13):
#         ax = fig.add_subplot(5,3,1+kk)
#         model = complete_model_list[kk]
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#         plt.legend(loc=0)
#         if kk % 3 ==  0:
#             plt.ylabel('Change in dynamic cloud\n feedback (W m$^{-2}$ K$^{-1}$)')
#         else:
#             ax.tick_params(labelleft=False)
#         if kk > 9:
#             plt.xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#             ax.tick_params(labelbottom=False)
#         plt.xlim([-150,100])
#         plt.ylim([-0.025,0.06])
#         plt.grid(color='lightgrey')
#         plt.title('('+chr(97+kk)+') '+model)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_all_models_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer1'+plot_type)
#     fig = plt.figure(2, figsize=(5,8))
#     for kk in range(13):        
#         model = complete_model_list[kk]
#         ax1 = fig.add_subplot(5,3,1+kk)
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors=colorlist[2], label='Freq.')
#         ax1.set_xlim([-150,100])
#         delta_w500 = w500_bins[1]-w500_bins[0]
#         ax1.set_ylim([-0.01,0.015])
#         ax1.set_yticks(np.arange(-0.01,0.015001,0.005))
#         if kk % 3 ==  0:
#             ax1.set_ylabel('Frequency; AMIP4K-AMIP')
#         else:
#             ax1.tick_params(labelleft=False)
#         if kk > 9:
#             ax1.set_xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#             ax1.tick_params(labelbottom=False)
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[0], label='SW')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[1], label='LW')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         if kk % 3 ==  2:
#             ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)')
#         elif kk == 12:
#             ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)')
#         else:
#             ax2.tick_params(labelright=False)
#         ax2.set_ylim([-20,30])
#         ax2.grid(which='both', axis='both', color='lightgrey')
#         plt.title('('+chr(97+kk)+') '+model, fontsize=8)
# #        fig.subplots_adjust(left=0.191, right=0.869, bottom=0.12, top=0.95, wspace=0.2, hspace=0.43)
#     plt.legend(lines + lines2, labels + labels2, bbox_to_anchor=(2.0, 0.5), loc='center')
#     fig.subplots_adjust(left=0.157, right=0.869, bottom=0.061, top=0.961, wspace=0.190, hspace=0.48)
# #    fig.tight_layout() # not working nicely
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_all_models_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer2'+plot_type)
#     plt.show()
#     if show_plots:
#         plt.show()
#     else:
#         plt.close('all')

        
# def plot_model_feedbacks_vs_w500_v2(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=True, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, method='AMIP', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
#     '''
#     Plot thermodynamic and dynamic feedbacks vs w500 for each model.
#     '''

#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
# #   Add multi-model means to complete_model_list
#     if not 'multi_model_mean' in AMIP4K_params.keys():
#         AMIP4K_params['multi_model_mean'] = {'w500_hist' : np.array([AMIP4K_params[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                              'sw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                              'lw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                              }
#         AMIP_params_long['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                                 'sw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                 'lw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                              }
#         fixed_rad_hist_param['multi_model_mean'] = {'sw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                     'lw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                                     }
#         complete_model_list += ['multi_model_mean']
#     for kk,model in enumerate(complete_model_list):
#         fig = plt.figure(0, figsize=(5.0,3.5)) # Plot dynamic feedback as fn of w500 and 
#         ax = fig.add_subplot(211)
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#         plt.legend(loc=0)
#         plt.ylabel('Difference in dynamic\ncloud feedback (W m$^{-2}$ K$^{-1}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.grid(color='lightgrey')
#         ax1 = fig.add_subplot(212)
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors=colorlist[2], label='Freq.')
#         ax1.set_xlim([-150,100])
#         delta_w500 = w500_bins[1]-w500_bins[0]
#         ax1.set_ylim([-0.004*delta_w500,0.006*delta_w500])
#         ax1.set_yticks(np.arange(-0.004*delta_w500,0.006*delta_w500+0.00000000001, 0.002*delta_w500), color=colorlist[2])
#         ax1.set_ylabel('Frequency; AMIP4K-AMIP', color=colorlist[2])
#         ax1.set_xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax1.spines['left'].set_color(colorlist[2])
#         ax1.yaxis.label.set_color(colorlist[2])
#         ax1.tick_params(axis='y', colors=colorlist[2])
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[0], label='SW')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[1], label='LW')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         ax2.legend(lines + lines2, labels + labels2, loc=3, ncol=3)
#         ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)', color='#F28D32')
# #        ax2.set_xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax2.set_xlim([-150,100])
#         ax2.set_ylim([-10,15])
#         ax2.grid(which='both', axis='both', color='lightgrey')
#         ax2.spines['right'].set_color('#F28D32')
#         ax2.spines['left'].set_color(colorlist[2])
#         ax2.yaxis.label.set_color('#F28D32')
#         ax2.tick_params(axis='y', colors='#F28D32')
#         plt.text(0.08, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.text(0.08, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
#         fig.subplots_adjust(left=0.191, right=0.869, bottom=0.12, top=0.95, wspace=0.2, hspace=0.43)
# #        fig.tight_layout() # not working nicely
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_'+model+'_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer'+plot_type)
#         if model == 'multi_model_mean':
#             plt.show()
# #        plt.show()
#         if show_plots:
#            plt.show()
#         else:
#             plt.close('all')
#         fig = plt.figure(0, figsize=(8.0,2.85)) # Plot dynamic feedback as fn of w500 and 
#         ax = fig.add_subplot(121)
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#         plt.legend(loc=3)
#         plt.ylabel('Difference in dynamic\ncloud feedback (W m$^{-2}$ K$^{-1}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.grid(color='lightgrey')
#         ax1 = fig.add_subplot(122)
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors=colorlist[2], label='Freq.')
#         ax1.set_xlim([-150,100])
#         delta_w500 = w500_bins[1]-w500_bins[0]
#         ax1.set_ylim([-0.004*delta_w500,0.006*delta_w500])
#         ax1.set_yticks(np.arange(-0.004*delta_w500,0.006*delta_w500+0.00000000001, 0.002*delta_w500), color=colorlist[2])
#         ax1.set_ylabel('Frequency; AMIP4K-AMIP', color=colorlist[2])
#         ax1.set_xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax1.spines['left'].set_color(colorlist[2])
#         ax1.yaxis.label.set_color(colorlist[2])
#         ax1.tick_params(axis='y', colors=colorlist[2])
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[0], label='SW')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[1], label='LW')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         ax2.legend(lines + lines2, labels + labels2, loc=3, ncol=1)
#         ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)', color='#F28D32')
# #        ax2.set_xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax2.set_xlim([-150,100])
#         ax2.set_ylim([-10,15])
#         ax2.grid(which='both', axis='both', color='lightgrey')
#         ax2.spines['right'].set_color('#F28D32')
#         ax2.spines['left'].set_color(colorlist[2])
#         ax2.yaxis.label.set_color('#F28D32')
#         ax2.tick_params(axis='y', colors='#F28D32')
#         plt.text(0.08, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.text(0.08, 0.9, '(b)', horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
#         fig.subplots_adjust(left=0.12, right=0.92, bottom=0.15, top=0.95, wspace=0.35, hspace=0.43)
# #        fig.tight_layout() # not working nicely
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_'+model+'_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer_landscape'+plot_type)
#         if model == 'multi_model_mean':
#             plt.show()
# #        plt.show()
#         if show_plots:
#            plt.show()
#         else:
#             plt.close('all')
# #   Put all models on single plot
#     fig = plt.figure(0, figsize=(5,8))
#     for kk in range(13):
#         ax = fig.add_subplot(5,3,1+kk)
#         model = complete_model_list[kk]
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#         plt.legend(loc=0)
#         if kk % 3 ==  0:
#             plt.ylabel('Change in dynamic cloud\n feedback (W m$^{-2}$ K$^{-1}$)')
#         else:
#             ax.tick_params(labelleft=False)
#         if kk > 9:
#             plt.xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#             ax.tick_params(labelbottom=False)
#         plt.xlim([-150,100])
#         plt.ylim([-0.025,0.06])
#         plt.grid(color='lightgrey')
#         plt.title('('+chr(97+kk)+') '+model)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_all_models_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer1'+plot_type)
#     fig = plt.figure(2, figsize=(5,8))
#     for kk in range(13):        
#         model = complete_model_list[kk]
#         ax1 = fig.add_subplot(5,3,1+kk)
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors=colorlist[2], label='Freq.')
#         ax1.set_xlim([-150,100])
#         delta_w500 = w500_bins[1]-w500_bins[0]
#         ax1.set_ylim([-0.01,0.015])
#         ax1.set_yticks(np.arange(-0.01,0.015001,0.005))
#         if kk % 3 ==  0:
#             ax1.set_ylabel('Frequency; AMIP4K-AMIP')
#         else:
#             ax1.tick_params(labelleft=False)
#         if kk > 9:
#             ax1.set_xlabel('$\omega$500 (hPa day$^{-1}$)')
#         else:
#             ax1.tick_params(labelbottom=False)
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, obs_data['Ann']['sw_cre_mean']-AMIP_params_long[model]['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[0], label='SW')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['lw_cre_mean']-AMIP_params_long[model]['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[1], label='LW')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
# #        ax2.legend(lines + lines2, labels + labels2, loc=3, ncol=3)
#         if kk % 3 ==  2:
#             ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)')
#         elif kk == 12:
#             ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)')
#         else:
#             ax2.tick_params(labelright=False)
#  #        ax2.set_xlim([-150,100])
#         ax2.set_ylim([-20,30])
#         ax2.grid(which='both', axis='both', color='lightgrey')
#         plt.title('('+chr(97+kk)+') '+model, fontsize=8)
# #        fig.subplots_adjust(left=0.191, right=0.869, bottom=0.12, top=0.95, wspace=0.2, hspace=0.43)
#     plt.legend(lines + lines2, labels + labels2, bbox_to_anchor=(2.0, 0.5), loc='center')
#     fig.subplots_adjust(left=0.157, right=0.869, bottom=0.061, top=0.961, wspace=0.190, hspace=0.48)
# #    fig.tight_layout() # not working nicely
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_all_models_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer2'+plot_type)
#     plt.show()
#     if show_plots:
#         plt.show()
#     else:
#         plt.close('all')

        
# def plot_model_feedbacks_vs_w500_v3(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=True, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, method='AMIP', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
#     '''
#     Plot thermodynamic and dynamic feedbacks vs w500 for each model.
#     '''

#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
# #   Add multi-model means to complete_model_list
#     if not 'multi_model_mean' in AMIP4K_params.keys():
#         AMIP4K_params['multi_model_mean'] = {'w500_hist' : np.array([AMIP4K_params[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                              'sw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                              'lw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                              }
#         AMIP_params_long['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                                 'sw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                 'lw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                              }
#         fixed_rad_hist_param['multi_model_mean'] = {'sw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                     'lw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                                     }
#         complete_model_list += ['multi_model_mean']
#     for kk,model in enumerate(complete_model_list):
#         fig = plt.figure(0, figsize=(5.0,3.5)) # Plot dynamic feedback as fn of w500 and 
#         ax = fig.add_subplot(211)
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model]['sw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model]['sw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model]['lw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model]['lw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#         plt.scatter(w500_bins_mid, ((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*obs_data['Ann']['sw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum(), label='Obs SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*obs_data['Ann']['sw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[2])
#         plt.scatter(w500_bins_mid, ((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*obs_data['Ann']['lw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum(), label='Obs LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*obs_data['Ann']['lw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[3])
#         plt.legend(loc=0)
#         plt.ylabel('Dynamic\ncloud feedback (W m$^{-2}$ K$^{-1}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.grid(color='lightgrey')
#         ax1 = fig.add_subplot(212)
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors='k', label='Freq.')
#         ax1.set_xlim([-150,100])
# #        ax1.set_ylim([-0.002,0.003])
#         ax1.set_ylabel('Frequency; AMIP4K-AMIP')
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, AMIP_params_long[model]['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[0], label='SW CRE')
#         plt.scatter(w500_bins_mid, AMIP_params_long[model]['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[1], label='LW CRE')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[2], label='Obs SW CRE')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[3], label='Obs LW CRE')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         ax2.legend(lines + lines2, labels + labels2, loc=0)
#         ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax2.set_xlim([-150,100])
# #        ax2.set_ylim([-10,15])
#         ax2.grid(which='both', axis='both')
#         fig.tight_layout()
#         plt.text(0.1, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_'+model+'_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer_v3'+plot_type)
#         if show_plots:
#            plt.show()
#         else:
#             plt.close('all')

        
# def plot_model_feedbacks_vs_w500_v4(complete_model_list, w500_bins_mid, AMIP4K_params, AMIP_params_long, obs_data, fixed_rad_hist_obs_param, fixed_rad_hist_param, show_plots=True, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, method='AMIP', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
#     '''
#     Plot thermodynamic and dynamic feedbacks vs w500 for each model.
#     '''

#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
# #   Add multi-model means to complete_model_list
#     if not 'multi_model_mean' in AMIP4K_params.keys():
#         AMIP4K_params['multi_model_mean'] = {'w500_hist' : np.array([AMIP4K_params[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                              'sw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                              'lw_cre_mean' : np.nanmean(np.array([AMIP4K_params[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                              }
#         AMIP_params_long['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long[model]['w500_hist'] for model in complete_model_list]).mean(axis=0),
#                                                 'sw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                 'lw_cre_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                              }
#         fixed_rad_hist_param['multi_model_mean'] = {'sw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['sw_cre_mean'] for model in complete_model_list]), axis=0),
#                                                     'lw_cre_mean' : np.nanmean(np.array([fixed_rad_hist_param[model]['lw_cre_mean'] for model in complete_model_list]), axis=0)
#                                                     }
#         complete_model_list += ['multi_model_mean']
#     for kk,model in enumerate(complete_model_list):
#         fig = plt.figure(0, figsize=(5.0,3.5)) # Plot dynamic feedback as fn of w500 and 
#         ax = fig.add_subplot(211)
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(-AMIP_params_long[model]['sw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='-SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(-AMIP_params_long[model]['sw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[0])
#         plt.scatter(w500_bins_mid, (((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model]['lw_cre_mean']))/AMIP_params_long[model]['w500_hist'].sum(), label='LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*(AMIP_params_long[model]['lw_cre_mean'])/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[1])
#         plt.scatter(w500_bins_mid, ((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*-obs_data['Ann']['sw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum(), label='-Obs SW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*-obs_data['Ann']['sw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[2])
#         plt.scatter(w500_bins_mid, ((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*obs_data['Ann']['lw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum(), label='Obs LW {:.2f}'.format(np.nansum(((AMIP4K_params[model]['w500_hist']-AMIP_params_long[model]['w500_hist'])/4.)*obs_data['Ann']['lw_cre_mean']/AMIP_params_long[model]['w500_hist'].sum())),s=5, facecolors='none', edgecolors=colorlist[3])
#         plt.legend(loc=0)
#         plt.ylabel('Dynamic\ncloud feedback (W m$^{-2}$ K$^{-1}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         plt.xlim([-150,100])
#         plt.grid(color='lightgrey')
#         ax1 = fig.add_subplot(212)
#         plt.scatter(w500_bins_mid, (AMIP4K_params[model]['w500_hist']/AMIP4K_params[model]['w500_hist'].sum())- (AMIP_params_long[model]['w500_hist']/AMIP_params_long[model]['w500_hist'].sum()), s=5, facecolors='none', edgecolors='k', label='Freq.')
#         ax1.set_xlim([-150,100])
# #        ax1.set_ylim([-0.002,0.003])
#         ax1.set_ylabel('Frequency; AMIP4K-AMIP')
#         ax1.grid(zorder=-20)
#         ax2 = ax1.twinx()
#         plt.scatter(w500_bins_mid, -AMIP_params_long[model]['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[0], label='-SW CRE')
#         plt.scatter(w500_bins_mid, AMIP_params_long[model]['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[1], label='LW CRE')
#         plt.scatter(w500_bins_mid, -obs_data['Ann']['sw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[2], label='-Obs SW CRE')
#         plt.scatter(w500_bins_mid, obs_data['Ann']['lw_cre_mean'], s=5, facecolors='none', edgecolors=colorlist[3], label='Obs LW CRE')
#         lines, labels = ax1.get_legend_handles_labels()
#         lines2, labels2 = ax2.get_legend_handles_labels()
#         ax2.legend(lines + lines2, labels + labels2, loc=0)
#         ax2.set_ylabel('CRE; Obs-AMIP (W m$^{-2}$)')
#         plt.xlabel('Circulation regime (hPa day$^{-1}$)')
#         ax2.set_xlim([-150,100])
# #        ax2.set_ylim([-10,15])
#         ax2.grid(which='both', axis='both')
#         fig.tight_layout()
#         plt.text(0.1, 0.9, '(a)', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#         plt.savefig('/home/users/phill/images/CIRCULATES/'+method+'_'+model+'_dist_cre_vs_w500_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_explainer_v4'+plot_type)
#         if show_plots:
#            plt.show()
#         else:
#             plt.close('all')

                

# def decompose_rad_cess(params_ctrl, params_warming, fixed_rad_hist={'sw_cre_mean' : [-9999], 'lw_cre_mean' : [-9999]}, fixed_w500_hist=[-9999], delta_t=4.0):
#     if fixed_rad_hist['sw_cre_mean'][0] != -9999:
#         A,B,C= decompose_rad((params_ctrl['sw_cre_mean']+params_ctrl['lw_cre_mean']), (params_warming['sw_cre_mean']+params_warming['lw_cre_mean']), params_ctrl['w500_hist']/params_ctrl['w500_hist'].sum(), params_warming['w500_hist']/params_warming['w500_hist'].sum(), fixed_w500_hist=fixed_w500_hist, fixed_rad_hist=(fixed_rad_hist['sw_cre_mean']+fixed_rad_hist['lw_cre_mean'])) #
#     else:
#         A,B,C= decompose_rad((params_ctrl['sw_cre_mean']+params_ctrl['lw_cre_mean']), (params_warming['sw_cre_mean']+params_warming['lw_cre_mean']), params_ctrl['w500_hist']/params_ctrl['w500_hist'].sum(), params_warming['w500_hist']/params_warming['w500_hist'].sum(), fixed_w500_hist=fixed_w500_hist) #
#     net_cre_dynamic = A/delta_t
#     net_cre_thermodynamic = B/delta_t
#     net_cre_co_variation = C/delta_t
#     A,B,C = decompose_rad(params_ctrl['sw_cre_mean'], params_warming['sw_cre_mean'], params_ctrl['w500_hist']/params_ctrl['w500_hist'].sum(), params_warming['w500_hist']/params_warming['w500_hist'].sum(), fixed_w500_hist=fixed_w500_hist, fixed_rad_hist=fixed_rad_hist['sw_cre_mean']) 
#     sw_cre_dynamic = A/delta_t
#     sw_cre_thermodynamic = B/delta_t
#     sw_cre_co_variation = C/delta_t
#     A,B,C = decompose_rad(params_ctrl['lw_cre_mean'], params_warming['lw_cre_mean'], params_ctrl['w500_hist']/params_ctrl['w500_hist'].sum(), params_warming['w500_hist']/params_warming['w500_hist'].sum(), fixed_w500_hist=fixed_w500_hist, fixed_rad_hist=fixed_rad_hist['lw_cre_mean'])
#     lw_cre_dynamic = A/delta_t
#     lw_cre_thermodynamic = B/delta_t
#     lw_cre_co_variation = C/delta_t
#     return net_cre_dynamic, net_cre_thermodynamic, net_cre_co_variation, sw_cre_dynamic, sw_cre_thermodynamic, sw_cre_co_variation, lw_cre_dynamic, lw_cre_thermodynamic, lw_cre_co_variation


# def plot_decomposition_comparison(complete_model_list, sw_cre_dynamic, sw_cre_dynamic_param, sw_cre_thermodynamic, sw_cre_thermodynamic_param, sw_cre_co_variation, sw_cre_co_variation_param, ylabel='SW cloud feedback (W m$^{-2}$)', savename='', leg=['dynamic', 'dynamic param', 'thermodynamic', 'thermodynamic param', 'co-variation', 'co-variation param', 'sum', 'sum param'], co_variation2=True, lon_min=165, lon_max=235, lat_min=-30, lat_max=30, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), sw_cre_dynamic_err={}, sw_cre_dynamic_param_err={}, sw_cre_thermodynamic_err={}, sw_cre_thermodynamic_param_err={}, sw_cre_co_variation_err={}, sw_cre_co_variation_param_err={}, sw_cre_sum_err={}, sw_cre_sum_param_err={}, fig=None, subplot_index=111, text=None):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     if fig == None:
#         fig = plt.figure(0, figsize=(5.0, 4.0))
#     ax = fig.add_subplot(subplot_index)
#     plt.plot(np.arange(len(complete_model_list)+1)+0.36, [np.mean([sw_cre_dynamic[m] for m in complete_model_list]),]+[sw_cre_dynamic[m] for m in complete_model_list], color=colorlist[0], marker='D', markersize=4, linestyle='', label=leg[0])
#     if len(sw_cre_dynamic_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.36, [np.mean([sw_cre_dynamic[m] for m in complete_model_list]),]+[sw_cre_dynamic[m] for m in complete_model_list], color=colorlist[0], marker='D', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_dynamic_err[m][0] for m in complete_model_list]),]+[sw_cre_dynamic_err[m][0] for m in complete_model_list], [np.mean([sw_cre_dynamic_err[m][1] for m in complete_model_list]),]+[sw_cre_dynamic_err[m][1] for m in complete_model_list]])
#     plt.plot(np.arange(len(complete_model_list)+1)+0.4, [np.mean([sw_cre_dynamic_param[m] for m in complete_model_list]),]+[sw_cre_dynamic_param[m] for m in complete_model_list], color=colorlist[0], marker='x', markersize=4, linestyle='', label=leg[1])
#     if len(sw_cre_dynamic_param_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.4, [np.mean([sw_cre_dynamic_param[m] for m in complete_model_list]),]+[sw_cre_dynamic_param[m] for m in complete_model_list], color=colorlist[0], marker='x', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_dynamic_param_err[m][0] for m in complete_model_list]),]+[sw_cre_dynamic_param_err[m][0] for m in complete_model_list], [np.mean([sw_cre_dynamic_param_err[m][1] for m in complete_model_list]),]+[sw_cre_dynamic_param_err[m][1] for m in complete_model_list]])
#     plt.plot(np.arange(len(complete_model_list)+1)+0.44, [np.mean([sw_cre_thermodynamic[m] for m in complete_model_list]),]+[sw_cre_thermodynamic[m] for m in complete_model_list], color=colorlist[1], marker='D', markersize=4, linestyle='', label=leg[2])
#     if len(sw_cre_thermodynamic_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.44, [np.mean([sw_cre_thermodynamic[m] for m in complete_model_list]),]+[sw_cre_thermodynamic[m] for m in complete_model_list], color=colorlist[1], marker='D', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_thermodynamic_err[m][0] for m in complete_model_list]),]+[sw_cre_thermodynamic_err[m][0] for m in complete_model_list], [np.mean([sw_cre_thermodynamic_err[m][1] for m in complete_model_list]),]+[sw_cre_thermodynamic_err[m][1] for m in complete_model_list]])
#     plt.plot(np.arange(len(complete_model_list)+1)+0.48, [np.mean([sw_cre_thermodynamic_param[m] for m in complete_model_list]),]+[sw_cre_thermodynamic_param[m] for m in complete_model_list], color=colorlist[1], marker='x', markersize=4, linestyle='', label=leg[3])
#     if len(sw_cre_thermodynamic_param_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.48, [np.mean([sw_cre_thermodynamic_param[m] for m in complete_model_list]),]+[sw_cre_thermodynamic_param[m] for m in complete_model_list], color=colorlist[1], marker='x', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_thermodynamic_param_err[m][0] for m in complete_model_list]),]+[sw_cre_thermodynamic_param_err[m][0] for m in complete_model_list], [np.mean([sw_cre_thermodynamic_param_err[m][1] for m in complete_model_list]),]+[sw_cre_thermodynamic_param_err[m][1] for m in complete_model_list]])
#     plt.plot(np.arange(len(complete_model_list)+1)+0.52, [np.mean([sw_cre_co_variation[m] for m in complete_model_list]),]+ [sw_cre_co_variation[m] for m in complete_model_list], color=colorlist[2], marker='D', markersize=4, linestyle='', label=leg[4])
#     if len(sw_cre_co_variation_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.52, [np.mean([sw_cre_co_variation[m] for m in complete_model_list]),]+[sw_cre_co_variation[m] for m in complete_model_list], color=colorlist[2], marker='D', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_co_variation_err[m][0] for m in complete_model_list]),]+[sw_cre_co_variation_err[m][0] for m in complete_model_list], [np.mean([sw_cre_co_variation_err[m][1] for m in complete_model_list]),]+[sw_cre_co_variation_err[m][1] for m in complete_model_list]])
#     if co_variation2:
#         plt.plot(np.arange(len(complete_model_list)+1)+0.56, [np.mean([sw_cre_co_variation_param[m] for m in complete_model_list]),]+ [sw_cre_co_variation_param[m] for m in complete_model_list], color=colorlist[2], marker='x', markersize=4, linestyle='', label=leg[5])
#     else:
#        plt.plot(np.arange(len(complete_model_list)+1)+0.56, np.zeros(len(complete_model_list)+1)/0., color='none', marker='x', markersize=4, linestyle='', label='should not show up')
#     plt.plot(np.arange(len(complete_model_list)+1)+0.6, [np.mean([sw_cre_thermodynamic[m]+sw_cre_dynamic[m]+sw_cre_co_variation[m] for m in complete_model_list]),]+ [sw_cre_thermodynamic[m]+sw_cre_dynamic[m]+sw_cre_co_variation[m] for m in complete_model_list], color='k', marker='D', markersize=4, linestyle='', label=leg[-2])
#     if len(sw_cre_sum_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.56, [np.mean([sw_cre_thermodynamic[m]+sw_cre_dynamic[m]+sw_cre_co_variation[m] for m in complete_model_list]),]+ [sw_cre_thermodynamic[m]+sw_cre_dynamic[m]+sw_cre_co_variation[m] for m in complete_model_list], color='k', marker='D', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_sum_err[m][0] for m in complete_model_list]),]+[sw_cre_sum_err[m][0] for m in complete_model_list], [np.mean([sw_cre_sum_err[m][1] for m in complete_model_list]),]+[sw_cre_sum_err[m][1] for m in complete_model_list]])
#     plt.plot(np.arange(len(complete_model_list)+1)+0.64, [np.mean([sw_cre_thermodynamic_param[m]+sw_cre_dynamic_param[m]+sw_cre_co_variation_param[m] for m in complete_model_list]),]+ [sw_cre_thermodynamic_param[m]+sw_cre_dynamic_param[m]+sw_cre_co_variation_param[m] for m in complete_model_list], color='k', marker='x', markersize=4, linestyle='', label=leg[-1])
#     if len(sw_cre_sum_param_err) > 0:
#         plt.errorbar(np.arange(len(complete_model_list)+1)+0.64, [np.mean([sw_cre_thermodynamic_param[m]+sw_cre_dynamic_param[m]+sw_cre_co_variation_param[m] for m in complete_model_list]),]+ [sw_cre_thermodynamic_param[m]+sw_cre_dynamic_param[m]+sw_cre_co_variation_param[m] for m in complete_model_list], color='k', marker='x', markersize=4, linestyle='', yerr=[[np.mean([sw_cre_sum_param_err[m][0] for m in complete_model_list]),]+[sw_cre_sum_param_err[m][0] for m in complete_model_list], [np.mean([sw_cre_sum_param_err[m][1] for m in complete_model_list]),]+[sw_cre_sum_param_err[m][1] for m in complete_model_list]])
#     if co_variation2:
#         plt.legend(loc='center', ncol=4, bbox_to_anchor=[0.5,1.1])
#     else:
#         plt.legend(loc='center', ncol=4, bbox_to_anchor=[0.5,1.1], labelcolor=['k','k', 'k', 'k', 'k', 'none','k', 'k'])
#     plt.ylabel(ylabel)
# #    plt.xlim([0,len(complete_model_list)+5])
#     plt.grid(color='lightgrey')
#     plt.xticks(np.arange(len(complete_model_list)+1)+0.5, ['Multi-model mean',]+complete_model_list, rotation=90)
#     if text != None:
#         plt.text(0.08, 0.9, text, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+savename+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_'+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()    

    
# def plot_decomposition_comparison_v2(complete_model_list, sw_cre_dynamic, sw_cre_dynamic_param, sw_cre_thermodynamic, sw_cre_thermodynamic_param, sw_cre_co_variation, sw_cre_co_variation_param, title='SW cloud feedback (W m$^{-2}$)', savename='', leg=['dynamic', 'thermodynamic', 'sum'], lon_min=165, lon_max=235, lat_min=-30, lat_max=30, xlabel='Model feedback (W m$^{-2}$)', ylabel='Obs feedback (W m$^{-2}$)', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), fig=None, subplot_index=111):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     print('sw_cre_dynamic=', sw_cre_dynamic)
#     if fig == None:
#         fig = plt.figure(0, figsize=(5.0, 3.0))
#     ax = fig.add_subplot(subplot_index)
#     plt.scatter(np.array([sw_cre_dynamic[model] for model in complete_model_list]).mean(), np.array([sw_cre_dynamic_param[model] for model in complete_model_list]).mean(), color=colorlist[0], marker="o", edgecolor='k',s=25, zorder=20)
#     plt.scatter(np.array([sw_cre_thermodynamic[model] for model in complete_model_list]).mean(), np.array([sw_cre_thermodynamic_param[model] for model in complete_model_list]).mean(), color=colorlist[1], marker="o", edgecolor='k',s=25, zorder=20)
#     plt.scatter(np.array([sw_cre_thermodynamic[model] for model in complete_model_list]).mean()+np.array([sw_cre_dynamic[model] for model in complete_model_list]).mean()+np.array([sw_cre_co_variation[model] for model in complete_model_list]).mean(), np.array([sw_cre_thermodynamic_param[model] for model in complete_model_list]).mean()+np.array([sw_cre_dynamic_param[model] for model in complete_model_list]).mean()+np.array([sw_cre_co_variation_param[model] for model in complete_model_list]).mean(), color=colorlist[2], marker="o", edgecolor='k',s=25, zorder=20)
#     plt.title(title)
#     plt.legend(leg, loc=0)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.grid(zorder=-30)
#     for jj,model in enumerate(complete_model_list):
#         plt.scatter(sw_cre_dynamic[model], sw_cre_dynamic_param[model], color=colorlist[0], marker="$"+chr(ord('a')+jj)+"$", zorder=10)
#         plt.scatter(sw_cre_thermodynamic[model], sw_cre_thermodynamic_param[model], color=colorlist[1], marker="$"+chr(ord('a')+jj)+"$", zorder=10)
#         plt.scatter(sw_cre_thermodynamic[model]+sw_cre_dynamic[model]+sw_cre_co_variation[model], sw_cre_thermodynamic_param[model]+sw_cre_dynamic_param[model]+sw_cre_co_variation_param[model], color=colorlist[2], marker="$"+chr(ord('a')+jj)+"$", zorder=10)
#     xlims = ax.get_xlim()
#     ylims = ax.get_ylim()
#     lims = [np.min((xlims[0], ylims[0])), np.max((xlims[1], ylims[1]))]
#     print('lims=', lims)
#     plt.xlim([lims[0], lims[1]])
#     plt.ylim([lims[0], lims[1]])
#     plt.plot(lims, lims, color='k', zorder=-20)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/'+savename+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_v2'+plot_type)
#     plt.show()

    
# def plot_scenario_comparison(complete_model_list, model_params_list, obs_data_param, var='circ_intensity', fig=None, subplot=111, ylabel='Circulation Intensity (h Pa day$^{-1}$)', region='SW', param='A', model_labels_list=['AMIP 2001-2014', 'AMIP 1979-2014', 'piControl', 'abrupt-4xCO2'], lon_min=165, lon_max=235, lat_min=-30, lat_max=30, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), errorbar=True):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     markerlist=['o', '+', '<', '>']
#     if fig == None:
#         fig = plt.figure(0)
#     ax = fig.add_subplot(subplot)
#     obs_var = var
#     if var == 'circ_intensity':
#         obs_var = 'Circ Intensity'
#     elif var == 'circ_mode':
#         obs_var = 'Circ Mode'
#     if errorbar:
#         if var in ['A', 'B', 'C', 'D']:
#             for ii, (model, label) in enumerate(zip(model_params_list, model_labels_list)):
#                 plt.errorbar(np.arange(len(complete_model_list))+1, [model[k][region][param]['param'][ord(var)-65] for k in complete_model_list], yerr=[[model[k][region][param]['param'][ord(var)-65]-np.min([a[ord(var)-65] for a in model[k][region][param]['bootstrap_param']]) for k in complete_model_list], [np.max([a[ord(var)-65] for a in model[k][region][param]['bootstrap_param']])-model[k][region][param]['param'][ord(var)-65] for k in complete_model_list]], color=colorlist2[ii], marker=markerlist[ii], linestyle='', label=label, capsize=4)
#             plt.errorbar(np.zeros(1), obs_data_param[region][param]['param'][ord(var)-65], yerr=np.array([[obs_data_param[region][param]['param'][ord(var)-65]-np.min([a[ord(var)-65] for a in obs_data_param[region][param]['bootstrap_param']])], [np.max([a[ord(var)-65] for a in obs_data_param[region][param]['bootstrap_param']])-obs_data_param[region][param]['param'][ord(var)-65]]]), marker='*', color='k', label='Obs')
#         else:
#             for ii, (model, label) in enumerate(zip(model_params_list, model_labels_list)):
#                 plt.errorbar(np.arange(len(complete_model_list))+1, [model[k][var] for k in complete_model_list], yerr=[[model[k][var]-np.min([a for a in model[k][var+'_bootstrap']]) for k in complete_model_list], [np.max([a for a in model[k][var+'_bootstrap']])-model[k][var] for k in complete_model_list]], color=colorlist2[ii], marker=markerlist[ii], linestyle='', label=label)
#             plt.errorbar(np.zeros(1), obs_data_param[obs_var], yerr=np.array([obs_data_param[obs_var]-np.min([a for a in obs_data_param[var+'_bootstrap']]), np.max([a for a in obs_data_param[var+'_bootstrap']])-obs_data_param[obs_var]])[:,None], marker='*', color='k', label='Obs')
#     else:
#         if var in ['A', 'B', 'C', 'D']:
#             for ii, (model, label) in enumerate(zip(model_params_list, model_labels_list)):
#                 plt.scatter(np.arange(len(complete_model_list))+1, [model[k][region][param]['param'][ord(var)-65] for k in complete_model_list], color=colorlist2[ii], marker=markerlist[ii], label=label, capsize=4)
#             plt.scatter(np.zeros(1), obs_data_param[region][param]['param'][ord(var)-65], marker='*', color='k', label='Obs')
#         else:
#             for ii, (model, label) in enumerate(zip(model_params_list, model_labels_list)):
#                 plt.scatter(np.arange(len(complete_model_list))+1, [model[k][var] for k in complete_model_list], color=colorlist2[ii], marker=markerlist[ii], label=label)
#             plt.scatter(np.zeros(1), obs_data_param[obs_var], marker='*', color='k', label='Obs')
#     plt.xlim([-1,len(complete_model_list)+1])
#     plt.xticks(np.arange(len(complete_model_list)+1), ['Observations',]+complete_model_list, rotation=90)
#     plt.legend(loc=0)
#     plt.ylabel(ylabel)
#     fig.tight_layout()
#     plt.savefig('/home/users/phill/images/CIRCULATES/scenario_model_comparison'+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'_'+''.join(model_labels_list).replace(' ','_')+'_'+ylabel.replace(' (h Pa day$^{-1}$)', '').replace(' ', '_').replace(',','')+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type)
#     plt.show()


# def get_picontrol_data(spatial_av_scale=2.0, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, model_list=picontrol_dict.keys(), yearlist=range(150)):
#     '''
#     Get 150 year means from piControl
#     '''
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     global_mean_ts,regional_mean_sw_all,regional_mean_sw_clr,regional_mean_lw_all,regional_mean_lw_clr  = ({} for __ in range(5))
#     w500_hist, w500_sw_cre_hist, w500_lw_cre_hist, sw_clr_sum, sw_cre_sum, sw_cre_sum_sq, sw_all_sum, lw_clr_sum, lw_cre_sum, lw_cre_sum_sq, lw_all_sum = get_cmip6_dist(spatial_av_scale=spatial_av_scale, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='PiControl', yearlist=yearlist) # Get w500 data as already stored
#     for kk in model_list:
#         print('kk=',kk)
#         print('global_mean_ts=', global_mean_ts)
#         global_mean_ts.update({kk:-9999})
#         regional_mean_sw_all.update({kk:-9999})
#         regional_mean_sw_clr.update({kk:-9999})
#         regional_mean_lw_all.update({kk:-9999})
#         regional_mean_lw_clr.update({kk:-9999})
#         pkl_filename = '/home/users/phill/w500_cre_pkldir/piControl_150yr_mean_data_'+kk+'_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_v2area_weighted.pkl'
#         if isfile(pkl_filename):
#             print('Reading '+pkl_filename)
#             with open(pkl_filename, 'rb') as fp:
#                 global_mean_ts[kk], regional_mean_sw_all[kk], regional_mean_sw_clr[kk], regional_mean_lw_all[kk], regional_mean_lw_clr[kk] = cPickle.load(fp)
#         else:      
#             if (kk == 'HadGEM3-GC31-LL'):
#                 ts_filelist = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/piControl/r1i1p1f1/Amon/ts/gn/latest/ts_Amon_HadGEM3-GC31-LL_piControl_r1i1p1f1_gn_*.nc')
#             elif (kk == 'UKESM1-0-LL'):
#                 ts_filelist = glob.glob('/gws/nopw/j04/circulates_vol2/PHill/CMIP6/CMIP/MOHC/UKESM1-0-LL/piControl/r1i1p1f2/Amon/ts/gn/latest/ts_Amon_UKESM1-0-LL_piControl_r1i1p1f2_gn_*.nc')
#             else:
#                 ts_filelist = glob.glob(picontrol_dict[kk].replace('wap', 'ts'))
#             print('kk,ts_filelist=', kk,ts_filelist)
#             area_filelist = glob.glob(picontrol_dict[kk].replace('piControl', '*').replace('r1i1p1f1', '*').replace('r1i1p1f2', '*').replace('r1i1p1f3', '*').replace('r1i1p2f1', '*').replace('wap', 'areacella').replace('Emon', 'fx').replace('Amon', 'fx'))
#             print("picontrol_dict[kk].replace('piControl', '*').replace('r1i1p1f1', '*').replace('r1i1p1f2', '*').replace('r1i1p1f3', '*').replace('r1i1p2f1', '*').replace('wap', 'areacella').replace('Emon', 'fx').replace('Amon', 'fx')=", picontrol_dict[kk].replace('piControl', '*').replace('r1i1p1f1', '*').replace('r1i1p1f2', '*').replace('r1i1p1f3', '*').replace('r1i1p2f1', '*').replace('wap', 'areacella').replace('Emon', 'fx').replace('Amon', 'fx'))
#             olr_filelist = glob.glob(picontrol_dict[kk].replace('wap', 'rlut').replace('Emon', 'Amon'))
#             olr_clr_filelist = glob.glob(picontrol_dict[kk].replace('wap', 'rlutcs').replace('Emon', 'Amon'))
#             osr_filelist = glob.glob(picontrol_dict[kk].replace('wap', 'rsut').replace('Emon', 'Amon'))
#             osr_clr_filelist = glob.glob(picontrol_dict[kk].replace('wap', 'rsutcs').replace('Emon', 'Amon'))
#             w500, olr, olr_clr, osr, osr_clr, olr_mean, olr_clr_mean, osr_mean, osr_clr_mean, global_mean_ts_list = ([] for __ in range(10))
#             ind_list, [ts_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist] = get_matched_time_ind(ts_filelist, [olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist], yearlist=yearlist)
#             print('ind_list=', ind_list)
#             print('ts_filelist, area_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist=', ts_filelist, area_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist)
#             for filename in ts_filelist:
#                 print('filename=', filename)
#                 print('area_filelist=', area_filelist)
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     ff = cf.read(filename, select='ncvar%ts')[0]
#                 else:
#                     ff = cf.read(filename, external=area_filelist[0], select='ncvar%ts')[0]
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     global_mean_ts_list += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data).array[:,0,0]]
#                 else:
#                     global_mean_ts_list += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#             global_mean_ts[kk] = np.concatenate(global_mean_ts_list)[ind_list[0]].mean()
#             new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min, lon_max-0.01, 2)+1, 'degreesE'))
#             new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min, lat_max-0.01, 2)+1, 'degreesN'))
#             for filename in olr_filelist:
#                 print('filename=', filename)
#                 print('area_filelist=', area_filelist)
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     ff = cf.read(filename, select='toa_outgoing_longwave_flux')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     olr_mean += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data)]
#                 else:
#                     ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_longwave_flux')[0]
#                     olr_mean += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#                 olr += [ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
# #            return olr
#             olr = np.concatenate(olr, axis=0)[ind_list[1]]
#             regional_mean_lw_all[kk] = np.concatenate(olr_mean)[ind_list[1]].mean() # Now area weighted
#             for filename in olr_clr_filelist:         
#                 print('filename=', filename)
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     ff = cf.read(filename, select='toa_outgoing_longwave_flux_assuming_clear_sky')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     olr_clr_mean += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data)]
#                 else:
#                     ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_longwave_flux_assuming_clear_sky')[0]
#                     olr_clr_mean += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#                 olr_clr += [ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             olr_clr = np.concatenate(olr_clr, axis=0)[ind_list[2],:,:]
#             regional_mean_lw_clr[kk] = np.concatenate(olr_clr_mean)[ind_list[2]].mean() # Now area weighted
#             for filename in osr_filelist:          
#                 print('filename=', filename)
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     ff = cf.read(filename, select='toa_outgoing_shortwave_flux')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     osr_mean += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data)]
#                 else:
#                     ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_shortwave_flux')[0]
#                     osr_mean += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#                 osr += [ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             osr = np.concatenate(osr, axis=0)[ind_list[3],:,:]
#             regional_mean_sw_all[kk] = np.concatenate(osr_mean)[ind_list[3]].mean() # Now area weighted
#             for filename in osr_clr_filelist:         
#                 print('filename=', filename)
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     ff = cf.read(filename, select='toa_outgoing_shortwave_flux_assuming_clear_sky')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     osr_clr_mean += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data)]
#                 else:
#                     ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_shortwave_flux_assuming_clear_sky')[0]
#                     osr_clr_mean += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#                 osr_clr += [ff.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             osr_clr = np.concatenate(osr_clr, axis=0)[ind_list[4],:,:]
#             regional_mean_sw_clr[kk] = np.concatenate(osr_clr_mean)[ind_list[4]].mean() # Now area weighted
#             with open(pkl_filename, 'wb') as fp:   
#                 cPickle.dump([global_mean_ts[kk],regional_mean_sw_all[kk],regional_mean_sw_clr[kk],regional_mean_lw_all[kk],regional_mean_lw_clr[kk]], fp, protocol=4)
#     return global_mean_ts,regional_mean_sw_all,regional_mean_sw_clr,regional_mean_lw_all,regional_mean_lw_clr, w500_hist, w500_sw_cre_hist, w500_lw_cre_hist, sw_clr_sum, sw_cre_sum, sw_cre_sum_sq, sw_all_sum, lw_clr_sum, lw_cre_sum, lw_cre_sum_sq, lw_all_sum  


# def get_abrupt4co2_data(spatial_av_scale=2.0, w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2), lon_min=165, lon_max=235, lat_min=-30, lat_max=30, model_list=abrupt4co2_dict.keys()):
#     if int(lon_min) == lon_min: lon_min=int(lon_min)
#     if int(lon_max) == lon_max: lon_max=int(lon_max)
#     if int(lat_min) == lat_min: lat_min=int(lat_min)
#     if int(lat_max) == lat_max: lat_max=int(lat_max)
#     global_mean_ts,regional_mean_sw_all,regional_mean_sw_clr,regional_mean_lw_all,regional_mean_lw_clr, regional_mean_sw_cre, regional_mean_lw_cre, regional_mean_w500_dist, regional_mean_olr_vs_w500_dist, regional_mean_lw_cre_vs_w500_dist, regional_mean_osr_vs_w500_dist, regional_mean_sw_cre_vs_w500_dist  = ({} for __ in range(12))
#     for kk in model_list:
#         for dict in [global_mean_ts,regional_mean_sw_all,regional_mean_sw_clr,regional_mean_lw_all,regional_mean_lw_clr, regional_mean_sw_cre, regional_mean_lw_cre, regional_mean_w500_dist, regional_mean_olr_vs_w500_dist, regional_mean_lw_cre_vs_w500_dist, regional_mean_osr_vs_w500_dist, regional_mean_sw_cre_vs_w500_dist]:
#             dict.update({kk:-9999})
#         pkl_filename = '/home/users/phill/w500_cre_pkldir/'+kk+'_abrupt4CO2_annual_data_lon'+str(lon_min)+'to'+str(lon_max)+'_lat'+str(lat_min)+'to'+str(lat_max)+'w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'_crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+'_v2area_weighted.pbz2'
#         if isfile(pkl_filename):
#             print('Reading '+pkl_filename)
#             with bz2.BZ2File(pkl_filename, 'rb') as fp:
#                global_mean_ts[kk],regional_mean_sw_all[kk],regional_mean_sw_clr[kk],regional_mean_lw_all[kk],regional_mean_lw_clr[kk], regional_mean_sw_cre[kk], regional_mean_lw_cre[kk], regional_mean_w500_dist[kk], regional_mean_olr_vs_w500_dist[kk], regional_mean_lw_cre_vs_w500_dist[kk], regional_mean_osr_vs_w500_dist[kk], regional_mean_sw_cre_vs_w500_dist[kk] = cPickle.load(fp)
#         else:      
#             wap_filelist = glob.glob(abrupt4co2_dict[kk])
#             area_filelist = glob.glob(abrupt4co2_dict[kk].replace('abrupt-4xCO2', '*').replace('r1i1p1f1', '*').replace('r1i1p1f2', '*').replace('r1i1p1f3', '*').replace('r1i1p2f1', '*').replace('wap', 'areacella').replace('Emon', 'fx').replace('Amon', 'fx'))
#             ts_filelist = glob.glob(abrupt4co2_dict[kk].replace('wap', 'ts').replace('Emon', 'Amon'))
#             olr_filelist = glob.glob(abrupt4co2_dict[kk].replace('wap', 'rlut').replace('Emon', 'Amon'))
#             olr_clr_filelist = glob.glob(abrupt4co2_dict[kk].replace('wap', 'rlutcs').replace('Emon', 'Amon'))
#             osr_filelist = glob.glob(abrupt4co2_dict[kk].replace('wap', 'rsut').replace('Emon', 'Amon'))
#             osr_clr_filelist = glob.glob(abrupt4co2_dict[kk].replace('wap', 'rsutcs').replace('Emon', 'Amon'))
#             w500, olr, olr_clr, osr, osr_clr = ([] for __ in range(5))
#             ind_list, [wap_filelist, ts_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist] = get_matched_time_ind(wap_filelist, [ts_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist], yearlist=range(150))
#             global_mean_ts_list = np.zeros(0)
#             for filename in ts_filelist:
#                 print('filename=', filename)
#                 print('area_filelist=', area_filelist)
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     ff = cf.read(filename, select='ncvar%ts')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     global_mean_ts_list = np.concatenate((global_mean_ts_list, np.convolve(ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data).array[:,0,0], np.ones(12)/12., mode='same')))
#                 else:
#                     ff = cf.read(filename, external=area_filelist[0], select='ncvar%ts')[0]
#                     global_mean_ts_list = np.concatenate((global_mean_ts_list, np.convolve(ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0], np.ones(12)/12., mode='same')))
#             global_mean_ts[kk] = (np.array(global_mean_ts_list).flatten())[ind_list[1]][6::12]
#             for filename in wap_filelist:
#                 print('filename=', filename)
#                 ff = cf.read(filename, select='lagrangian_tendency_of_air_pressure')[0]
#                 lon = ff.coord('longitude').array
#                 lat = ff.coord('latitude').array
#                 try:
#                     pressure = ff.coord('air_pressure').array
#                     ind_p = np.argmin(abs(pressure-50000.))
#                     w500_temp = 24*6*6*ff[:,ind_p,:,:]
#                 except:
#                     print('filename=', filename)
#                 new_lon = cf.DimensionCoordinate(data=cf.Data(np.arange(lon_min, lon_max-0.01, 2)+1, 'degreesE'))
#                 new_lat = cf.DimensionCoordinate(data=cf.Data(np.arange(lat_min, lat_max-0.01, 2)+1, 'degreesN'))
#                 area_weights = np.repeat(np.cos(np.pi*new_lat.array[:,None]/180),new_lon.size, axis=1)
#                 area_weights = area_weights/area_weights.sum()
#                 w500 += [w500_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             w500 = np.concatenate(w500, axis=0)
#             w500 = w500[ind_list[0],:,:]
#             w500 = w500.reshape(int(w500.shape[0]/12), 12, w500.shape[2], w500.shape[3])
#             w500_hist = []
#             area_weights_full = np.repeat(area_weights[None,:,:],12, axis=0)
#             for i in range(w500.shape[0]):
#                 w500_hist_temp, _ = np.histogram(w500[i].flatten(), bins=w500_bins, weights=area_weights_full.flatten()) 
#                 w500_hist += [w500_hist_temp]
#             regional_mean_w500_dist[kk] = np.array(w500_hist)
#             print('regional_mean_w500_dist[kk]=', regional_mean_w500_dist[kk])
#             olr_mean = []
#             for filename in olr_filelist:   
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     olr_temp = cf.read(filename, select='toa_outgoing_longwave_flux')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     olr_mean += [olr_temp.collapse('mean', weights=(ff.weights(weights=None)*area_weights).data, axes=['X', 'Y']).array]
#                 else:
#                     olr_temp = cf.read(filename, external=area_filelist[0], select='toa_outgoing_longwave_flux')[0]     
#                     olr_mean += [olr_temp.collapse('mean', weights='area', axes=['X', 'Y']).array]
#                 olr += [olr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             olr = np.concatenate(olr, axis=0)[ind_list[2],:,:]
#             olr = olr.reshape(int(olr.shape[0]/12), 12, olr.shape[1], olr.shape[2])
#             regional_mean_lw_all[kk] = np.convolve(np.concatenate(olr_mean)[ind_list[2],0,0], np.ones(12)/12, mode='same')[6::12] # NB this now area weighted, but w500 and w500-CRE distributions are not, which is not consistent.
#             lw_all_mean = []
#             for i in range(olr.shape[0]):
#                 lw_all_mean_temp, _ = np.histogram(w500[i].flatten(), bins=w500_bins, weights=olr[i].flatten()*area_weights_full.flatten()) 
#                 lw_all_mean += [lw_all_mean_temp]
#             regional_mean_olr_vs_w500_dist[kk] = np.array(lw_all_mean)
#             olr_clr_mean = []
#             for filename in olr_clr_filelist:         
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     olr_clr_temp = cf.read(filename, select='toa_outgoing_longwave_flux_assuming_clear_sky')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     olr_clr_mean += [olr_temp.collapse('mean', weights=(ff.weights(weights=None)*area_weights).data, axes=['X', 'Y']).array]
#                 else:
#                     olr_clr_temp = cf.read(filename, select='toa_outgoing_longwave_flux_assuming_clear_sky', external=area_filelist[0])[0]
#                     olr_clr_mean += [olr_clr_temp.collapse('mean', weights='area', axes=['X', 'Y']).array]
#                 olr_clr += [olr_clr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             olr_clr = np.concatenate(olr_clr, axis=0)[ind_list[3],:,:]
#             olr_clr = olr_clr.reshape(int(olr_clr.shape[0]/12), 12, olr_clr.shape[1], olr_clr.shape[2])
#             regional_mean_lw_clr[kk] = np.convolve(np.concatenate(olr_clr_mean)[ind_list[2],0,0], np.ones(12)/12, mode='same')[6::12] # Now area weighted?
#             regional_mean_lw_cre[kk] = regional_mean_lw_clr[kk] - regional_mean_lw_all[kk]
#             lw_cre_mean = []
#             for i in range(olr.shape[0]):
#                 lw_cre_mean_temp, _ = np.histogram(w500[i].flatten(), bins=w500_bins, weights=(olr_clr[i]-olr[i]).flatten()*area_weights_full.flatten()) 
#                 lw_cre_mean += [lw_cre_mean_temp]
#             regional_mean_lw_cre_vs_w500_dist[kk] = np.array(lw_cre_mean)
#             osr_mean = []
#             for filename in osr_filelist:          
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     osr_temp = cf.read(filename, select='toa_outgoing_shortwave_flux')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     osr_mean += [olr_temp.collapse('mean', weights=(ff.weights(weights=None)*area_weights).data, axes=['X', 'Y']).array]
#                 else:
#                     osr_temp = cf.read(filename, select='toa_outgoing_shortwave_flux', external=area_filelist[0])[0]
#                     osr_mean += [osr_temp.collapse('mean', weights='area', axes=['X', 'Y']).array]
#                 osr += [osr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             osr = np.concatenate(osr, axis=0)[ind_list[4],:,:]
#             osr = osr.reshape(int(osr.shape[0]/12), 12, osr.shape[1], osr.shape[2])
#             regional_mean_sw_all[kk] = np.convolve(np.concatenate(osr_mean)[ind_list[2],0,0], np.ones(12)/12, mode='same')[6::12] # Now area weighted
#             sw_all_mean = []
#             for i in range(osr.shape[0]):
#                 sw_all_mean_temp, _ = np.histogram(w500[i].flatten(), bins=w500_bins, weights=osr[i].flatten()*area_weights_full.flatten()) 
#                 sw_all_mean += [sw_all_mean_temp]
#             regional_mean_osr_vs_w500_dist[kk] = np.array(sw_all_mean)
#             osr_clr_mean = []
#             for filename in osr_clr_filelist:         
#                 if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                     osr_clr_temp = cf.read(filename, select='toa_outgoing_shortwave_flux_assuming_clear_sky')[0]
#                     lon = ff.coord('longitude').array
#                     lat = ff.coord('latitude').array
#                     area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                     osr_clr_mean += [olr_temp.collapse('mean', weights=(ff.weights(weights=None)*area_weights).data, axes=['X', 'Y']).array]
#                 else:
#                     osr_clr_temp = cf.read(filename, select='toa_outgoing_shortwave_flux_assuming_clear_sky', external=area_filelist[0])[0]
#                     osr_clr_mean += [osr_clr_temp.collapse('mean', weights='area', axes=['X', 'Y']).array]
#                 osr_clr += [osr_clr_temp.regrids({'latitude': new_lat, 'longitude': new_lon}, method='linear', src_cyclic=True, dst_cyclic=False).array]
#             osr_clr = np.concatenate(osr_clr, axis=0)[ind_list[5],:,:]
#             osr_clr = osr_clr.reshape(int(osr_clr.shape[0]/12), 12, osr_clr.shape[1], osr_clr.shape[2])
#             regional_mean_sw_clr[kk] = np.convolve(np.concatenate(osr_clr_mean)[ind_list[2],0,0], np.ones(12)/12, mode='same')[6::12] # Now area weighted
#             regional_mean_sw_cre[kk] = regional_mean_sw_clr[kk] - regional_mean_sw_all[kk]
#             sw_cre_mean = []
#             for i in range(osr.shape[0]):
#                 sw_cre_mean_temp, _ = np.histogram(w500[i].flatten(), bins=w500_bins, weights=(osr_clr[i]-osr[i]).flatten()*area_weights_full.flatten()) 
#                 sw_cre_mean += [sw_cre_mean_temp]
#             regional_mean_sw_cre_vs_w500_dist[kk] = np.array(sw_cre_mean)
#             with bz2.BZ2File(pkl_filename, 'w') as fp:   
#                 cPickle.dump([global_mean_ts[kk],regional_mean_sw_all[kk],regional_mean_sw_clr[kk],regional_mean_lw_all[kk],regional_mean_lw_clr[kk], regional_mean_sw_cre[kk], regional_mean_lw_cre[kk], regional_mean_w500_dist[kk], regional_mean_olr_vs_w500_dist[kk], regional_mean_lw_cre_vs_w500_dist[kk], regional_mean_osr_vs_w500_dist[kk], regional_mean_sw_cre_vs_w500_dist[kk]], fp, protocol=4)
#     return global_mean_ts,regional_mean_sw_all,regional_mean_sw_clr,regional_mean_lw_all,regional_mean_lw_clr, regional_mean_sw_cre, regional_mean_lw_cre, regional_mean_w500_dist, regional_mean_olr_vs_w500_dist, regional_mean_lw_cre_vs_w500_dist, regional_mean_osr_vs_w500_dist, regional_mean_sw_cre_vs_w500_dist



# def decompose_rad(control_rad_hist, exper_rad_hist, control_w500_hist, exper_w500_hist, forcing=0, fixed_w500_hist=[-9999], fixed_rad_hist=[-9999]):
#     if fixed_w500_hist[0] != -9999:
#         thermodynamic = np.nansum(fixed_w500_hist * ((exper_rad_hist - control_rad_hist)-forcing))
#     else:
#         thermodynamic = np.nansum(control_w500_hist * ((exper_rad_hist - control_rad_hist)-forcing))
#     if fixed_rad_hist[0] != -9999:
#         dynamic = np.nansum(fixed_rad_hist * (exper_w500_hist - control_w500_hist))
#     else:
#          dynamic = np.nansum(control_rad_hist * (exper_w500_hist - control_w500_hist))
#     co_variation = np.nansum(((exper_rad_hist - control_rad_hist)-forcing) * (exper_w500_hist - control_w500_hist))
#     return dynamic, thermodynamic, co_variation


def plot_w500_freq_map(yearlist=range(2001,2015), spatial_av_scale=2, time_av_scale=720, lon_min=0, lon_max=360, lat_min=-30, lat_max=30, rad_source='CERES_EBAF', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
    '''
    Makes plot showing where different w500 regimes are most likely to occur

    Want to know whether local minimum in magnitude of SW CRE is linked to
    errors in the way models predicr Sc vs Cu. Try to investigate this by
    looking at where the different circulation regimes occur.
    '''
#   Read cre-w500 data to get mean SW CRE for each w500 bin
    era5_data = match_omega500_rad_reanalyses_obs(w500_source='ERA5', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
    era5_data = era5_data['Ann']
    jra55_data = match_omega500_rad_reanalyses_obs(w500_source='JRA55', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
    jra55_data = jra55_data['Ann']
    merra2_data = match_omega500_rad_reanalyses_obs(w500_source='MERRA2', rad_source=rad_source, w500_bins=w500_bins, spatial_av_scale=2, time_av_scale=time_av_scale, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, yearlist=yearlist)
    merra2_data = merra2_data['Ann']
    obs_data = {}
    for kk in ['sw_cre_hist', 'sw_cre_sum', 'lw_cre_hist', 'lw_cre_sum', 'w500_hist', 'w500_hist_lw', 'sw_cre_adj_hist', 'lw_cre_adj_hist', 'sw_cre_adj_sum', 'lw_cre_adj_sum', 'sw_cre_adj2_hist', 'lw_cre_adj2_hist', 'sw_cre_adj2_sum', 'lw_cre_adj2_sum']: # Check w500_hist_lw and adj2 variables  will work for CERES_EBAF
        obs_data[kk] = era5_data[kk] + merra2_data[kk] + jra55_data[kk]
    for kk in ['sw_cre_mean', 'lw_cre_mean', 'sw_cre_adj_mean', 'lw_cre_adj_mean', 'sw_cre_adj2_mean', 'lw_cre_adj2_mean']:# Check adj2 variables  will work for CERES_EBAF
        obs_data[kk]= np.nanmean((era5_data[kk][:,None], merra2_data[kk][:,None], jra55_data[kk][:,None]), axis=0)[:,0]
#   Get AMIP data so can show multi-model mean bias
    AMIP_params_long = get_cmip6_param_data(spatial_av_scale=2.0, w500_bins=w500_bins, cre_bins=cre_bins, lon_min=lon_min, lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, experiment='AMIP', n_bootstrap=2, seed=1, time_av_scale=time_av_scale, yearlist=range(1979,2015), fit_param=False)
    AMIP_params_long['multi_model_mean'] = {'w500_hist' : np.array([AMIP_params_long[model]['w500_hist'] for model in amip_p4k_dict.keys()]).mean(axis=0),
                                            'sw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_long[model]['sw_cre_mean'] for model in amip_p4k_dict.keys()]), axis=0),
                                            'lw_cre_adj2_mean' : np.nanmean(np.array([AMIP_params_long[model]['lw_cre_mean'] for model in amip_p4k_dict.keys()]), axis=0)
                                            }
#   Now get w500 data for maps
    w500_regridded = []
#   ERA5:
    w500, month_w500 = read_w500_data('ERA5', yearlist[0],360, 0, 30, -30)
    print('w500.shape=', w500.shape)
    n_lat = w500.shape[1]
    n_lon = w500.shape[2]
    w500_lat = np.arange(-30,30.0001, 0.25)
    area_weights = np.cos(np.pi*w500_lat/180)
    spatial_av_scale_era5 = int(spatial_av_scale * 4) # Since ERA5 resolution is 0.25 degrees need to multiply by 4.
    for year in yearlist:
        w500, month_w500 = read_w500_data('ERA5', year,360, 0, 30, -30)
        w500_regridded += [0.5*(uniform_filter(w500*area_weights[None,:,None], (time_av_scale,spatial_av_scale_era5+1,spatial_av_scale_era5+1), mode='wrap')+uniform_filter(w500*area_weights[None,:,None], (time_av_scale,spatial_av_scale_era5-1, spatial_av_scale_era5-1), mode='wrap'))[int(time_av_scale/2)::time_av_scale,int(spatial_av_scale_era5/2):1+n_lat-int(spatial_av_scale_era5/2):int(spatial_av_scale_era5),int(spatial_av_scale_era5/2):1+n_lon-int(spatial_av_scale_era5/2):int(spatial_av_scale_era5)]]#  average w500 to CERES-SYN spatial scale.
#   JRA55:
    w500, month_w500 = read_w500_data('JRA55', yearlist[0],360, 0, 30, -30)
    print('w500.shape=', w500.shape)
    n_lat = w500.shape[1]
    n_lon = w500.shape[2]
    w500_lat = np.arange(-29.75, 29.8,0.5)
    area_weights = np.cos(np.pi*w500_lat/180)
    spatial_av_scale_jra55 = int(spatial_av_scale * 2) # Since JRA55 resolution is 0.5 degrees need to multiply by 2.
    time_av_scale_jra55 = int(time_av_scale / 6)
    for year in yearlist:
        w500, month_w500 = read_w500_data('JRA55', year,360, 0, 30, -30)
        w500_regridded += [uniform_filter(w500*area_weights[None,:,None], (time_av_scale_jra55,spatial_av_scale_jra55+1,spatial_av_scale_jra55+1), mode='wrap')[int(time_av_scale_jra55/2)::time_av_scale_jra55,int(spatial_av_scale_jra55/2):1+n_lat-int(spatial_av_scale_jra55/2):int(spatial_av_scale_jra55),int(spatial_av_scale_jra55/2):1+n_lon-int(spatial_av_scale_jra55/2):int(spatial_av_scale_jra55)]]#  average w500 to CERES-SYN spatial scale.
#   MERRA2:
    w500, month_w500 = read_w500_data('MERRA2', yearlist[0],360, 0, 30, -30)
    print('w500.shape=', w500.shape)
    n_lat = w500.shape[1]
    n_lon = w500.shape[2]
    w500_lat = np.arange(-29.75, 29.8,0.5)
    area_weights = np.cos(np.pi*w500_lat/180)
    spatial_av_scale_merra2 = int(spatial_av_scale * 2) # Since MERRA2 resolution is 0.5 degrees need to multiply by 2.
    for year in yearlist:
        w500, month_w500 = read_w500_data('MERRA2', year,360, 0, 30, -30)
        w500_regridded += [uniform_filter(w500*area_weights[None,:,None], (time_av_scale,spatial_av_scale_merra2+1,spatial_av_scale_merra2+1), mode='wrap')[int(time_av_scale/2)::time_av_scale,int(spatial_av_scale_merra2/2):1+n_lat-int(spatial_av_scale_merra2/2):int(spatial_av_scale_merra2),int(spatial_av_scale_merra2/2):1+n_lon-int(spatial_av_scale_merra2/2):int(spatial_av_scale_merra2)]]#  average w500 to CERES-SYN spatial scale.
    w500_regridded = np.array(w500_regridded)
    w500_freq_map_plot(w500_regridded, obs_data, AMIP_params_long, yearlist=range(2001,2015), spatial_av_scale=2, time_av_scale=720, lon_min=0, lon_max=360, lat_min=-30, lat_max=30, rad_source='CERES_EBAF', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2))
    return w500_regridded, obs_data, AMIP_params_long


def w500_freq_map_plot(w500_regridded, obs_data, AMIP_params_long, yearlist=range(2001,2015), spatial_av_scale=2, time_av_scale=720, lon_min=0, lon_max=360, lat_min=-30, lat_max=30, rad_source='CERES_EBAF', w500_bins=np.arange(-700,700.01,2), cre_bins=np.arange(-400,400.01,0.2)):
    w500_bins_mid = 0.5*(w500_bins[1:]+w500_bins[:-1])
    cent_lon = lon_min+(lon_max-lon_min)/2
    lon = np.arange(1,360,2)
    lat = np.arange(-29,30,2)
    proj=ccrs.PlateCarree(central_longitude=cent_lon)
    fig = plt.figure(0, figsize=(5,8))
    for ii in range(5):
        mymap = fig.add_subplot(511+ii, projection=proj)
        mymap.add_feature(feature.COASTLINE, linewidth=1)
        mymap.set_extent((-180, 180, -30, 30), crs=proj)
        cs = mymap.pcolormesh(lon, lat, ((w500_regridded > ii*10)  & (w500_regridded <= (ii+1)*10)).sum(axis=(0,1))[::-1,:], transform=ccrs.PlateCarree(), zorder=-20)
        cb = fig.colorbar(cs, orientation='vertical', extend='both', label='Frequency')
        mymap.set_rasterization_zorder(-10)
        plt.title(str(ii*10)+'<$\omega_{500}$$\leq$'+str((ii+1)*10)+' (hPa day$^{-1}$)'+'\nObserved mean SW CRE={:.2f}'.format(np.sum(obs_data['sw_cre_adj2_sum'][((10*ii <= w500_bins_mid) & (w500_bins_mid < 10*(ii+1)))])/np.sum(obs_data['w500_hist'][(10*ii <= w500_bins_mid) & (w500_bins_mid < 10*(ii+1))]))+' (W m$^{-2}$)'+'\nAMIP multi-model mean SW CRE={:.2f}'.format(np.sum(AMIP_params_long['multi_model_mean']['sw_cre_adj2_mean'][((10*ii <= w500_bins_mid) & (w500_bins_mid < 10*(ii+1)))]*AMIP_params_long['multi_model_mean']['w500_hist'][((10*ii <= w500_bins_mid) & (w500_bins_mid < 10*(ii+1)))])/np.sum(AMIP_params_long['multi_model_mean']['w500_hist'][(10*ii <= w500_bins_mid) & (w500_bins_mid < 10*(ii+1))]))+' (W m$^{-2}$)')
    fig.tight_layout()
    plt.savefig('/home/users/phill/images/CIRCULATES/w500_regime_occurence_map_'+str(yearlist[0])+'-'+str(yearlist[-1])+'_w500bin_width'+'{:.2f}'.format(w500_bins[1]-w500_bins[0]).replace('.', 'pt')+'_w500bin_max'+'{:.2f}'.format(w500_bins[-1]).replace('.', 'pt')+'crebin_width'+'{:.2f}'.format(cre_bins[1]-cre_bins[0]).replace('.', 'pt')+'_crebin_max'+'{:.2f}'.format(cre_bins[-1]).replace('.', 'pt')+plot_type, dpi=my_dpi)
    plt.show()
    

# def calc_global_feedback(yearlist=range(1979,2015)):
#     '''
#     Calculates total feedback for whole globe for climate models

#     This is used in paper to calculate ECS and hence impact of observationally
#     constraining cloud feedbacks in the tropics
#     '''
#     '''
#     Get omega500 and CRE as a function of omega500 for AMIP CMIP6 models

#     Only MOHC provides wap at timescales other than Amon 
#     '''
#     net_feedback, olr_amip, osr_amip, olr_4k, osr_4k = ({} for __ in range(5))
#     complete_model_list = []
#     for model in amip_p4k_dict.keys():
#         if (model in amip_dict.keys()):
#             complete_model_list += [model]
#     complete_model_list.sort()
#     for kk in complete_model_list:
#         net_feedback[kk] = 0
#         wap_filelist = glob.glob(amip_dict[kk])
#         olr_filelist = glob.glob(amip_dict[kk].replace('wap', 'rlut').replace('Emon', 'Amon'))
#         olr_clr_filelist = glob.glob(amip_dict[kk].replace('wap', 'rlutcs').replace('Emon', 'Amon'))
#         osr_filelist = glob.glob(amip_dict[kk].replace('wap', 'rsut').replace('Emon', 'Amon'))
#         osr_clr_filelist = glob.glob(amip_dict[kk].replace('wap', 'rsutcs').replace('Emon', 'Amon'))
#         area_filelist = glob.glob(picontrol_dict[kk].replace('piControl', '*').replace('r1i1p1f1', '*').replace('r1i1p1f2', '*').replace('r1i1p1f3', '*').replace('r1i1p2f1', '*').replace('wap', 'areacella').replace('Emon', 'fx').replace('Amon', 'fx'))
#         olr, osr = ([] for __ in range(2))
#         ind_list, [wap_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist] = get_matched_time_ind(wap_filelist, [olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist], yearlist=yearlist)
#         for filename in olr_filelist:     
#             print('filename=', filename)
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                 ff = cf.read(filename, select='toa_outgoing_longwave_flux')[0]
#             else:
#                 ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_longwave_flux')[0]
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use
#                 lon = ff.coord('longitude').array
#                 lat = ff.coord('latitude').array
#                 area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                 olr += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data).array[:,0,0]]
#             else:
#                 olr += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
# #                return olr, np.concatenate(olr)[ind_list[0]].mean(), ind_list, area_filelist
#         olr_amip[kk] = np.concatenate(olr)[ind_list[0]].mean()
# #        return olr, olr_amip, ind_list
#         net_feedback[kk] += olr_amip[kk]
#         for filename in osr_filelist:     
#             print('filename=', filename)
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                 ff = cf.read(filename, select='toa_outgoing_shortwave_flux')[0]
#             else:
#                 ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_shortwave_flux')[0]
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use
#                 lon = ff.coord('longitude').array
#                 lat = ff.coord('latitude').array
#                 area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                 osr += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data).array[:,0,0]]
#             else:
#                 osr += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#         osr_amip[kk] = np.concatenate(osr)[ind_list[0]].mean()
#         net_feedback[kk] += osr_amip[kk]
#         wap_filelist = glob.glob(amip_p4k_dict[kk])
#         olr_filelist = glob.glob(amip_p4k_dict[kk].replace('wap', 'rlut').replace('Emon', 'Amon'))
#         olr_clr_filelist = glob.glob(amip_p4k_dict[kk].replace('wap', 'rlutcs').replace('Emon', 'Amon'))
#         osr_filelist = glob.glob(amip_p4k_dict[kk].replace('wap', 'rsut').replace('Emon', 'Amon'))
#         osr_clr_filelist = glob.glob(amip_p4k_dict[kk].replace('wap', 'rsutcs').replace('Emon', 'Amon'))
#         area_filelist = glob.glob(picontrol_dict[kk].replace('piControl', '*').replace('r1i1p1f1', '*').replace('r1i1p1f2', '*').replace('r1i1p1f3', '*').replace('r1i1p2f1', '*').replace('wap', 'areacella').replace('Emon', 'fx').replace('Amon', 'fx'))
#         olr, osr = ([] for __ in range(2))
#         ind_list, [wap_filelist, olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist] = get_matched_time_ind(wap_filelist, [olr_filelist, olr_clr_filelist, osr_filelist, osr_clr_filelist], yearlist=yearlist)
#         for filename in olr_filelist:     
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                 ff = cf.read(filename, select='toa_outgoing_longwave_flux')[0]
#             else:
#                 ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_longwave_flux')[0]
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use
#                 lon = ff.coord('longitude').array
#                 lat = ff.coord('latitude').array
#                 area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                 olr += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data).array[:,0,0]]
#             else:
#                 olr += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#         olr_4k[kk] = np.concatenate(olr)[ind_list[0]].mean()
#         net_feedback[kk] -= olr_4k[kk]
#         for filename in osr_filelist:     
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use 
#                 ff = cf.read(filename, select='toa_outgoing_shortwave_flux')[0]
#             else:
#                 ff = cf.read(filename, external=area_filelist[0], select='toa_outgoing_shortwave_flux')[0]
#             if kk == 'BCC-CSM2-MR': # No area_filelist for BCC so use
#                 lon = ff.coord('longitude').array
#                 lat = ff.coord('latitude').array
#                 area_weights = np.repeat(np.cos(np.pi*lat[:,None]/180),lon.size, axis=1)
#                 osr += [ff.collapse('area: mean', weights=(ff.weights(weights=None)*area_weights).data).array[:,0,0]]
#             else:
#                 osr += [ff.collapse('area: mean', weights=ff.weights('area')).array[:,0,0]]
#         osr_4k[kk] = np.concatenate(osr)[ind_list[0]].mean()
#         net_feedback[kk] -= osr_4k[kk]
#         net_feedback[kk] = net_feedback[kk] / 4.0
#         net_feedback[kk] = net_feedback[kk] + 0.5 # To compensate for the lack of polar warming and sea ice reduction on the total radiative feedback in atmosphere-only experiment e.g. Qin et al 2022.
    
#     return net_feedback, olr_amip, osr_amip, olr_4k, osr_4k

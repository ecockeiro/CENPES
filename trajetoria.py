#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 18:45:17 2023

@author: everson
"""
from mpl_toolkits.basemap import shiftgrid
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd
import glob

lonmin, lonmax = -55, -30
latmin, latmax = -40, -15

fig = plt.figure(figsize=(10,6))
axx = fig.add_subplot(111)
m = Basemap(projection='merc', resolution="f", llcrnrlon=lonmin, llcrnrlat=latmin, urcrnrlon=lonmax, urcrnrlat=latmax)

m.drawcoastlines(color='k',linewidth=0.5,zorder=3)
m.drawcountries(color='k',linewidth=0.1,zorder=3)

parallelmin = int(latmin)
parallelmax = int(latmax)+1
m.drawparallels(np.arange(parallelmin, parallelmax,5,dtype='int16').tolist(),labels=[1,0,0,0],linewidth=0,fontsize=10, zorder=3)

meridianmin = int(lonmin)
meridianmax = int(lonmax)+1
m.drawmeridians(np.arange(meridianmin, meridianmax,5,dtype='int16').tolist(),labels=[0,0,0,1],linewidth=0,fontsize=10, zorder=3)

colors = ['C0','C1','C3','C2','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'] #default colors from Python (can be automated if the order is not important)
datafiles = glob.glob("/home/everson/CENPES/Track_planilhas_recortas/*.csv") #to read individual data files containing the coordinates of the track for each typhoon


for jj in range(2):
    dff = pd.read_csv(datafiles[jj],sep=',', dtype={'time': object}) #read data file and time as string
    dff['Longitude'] = (((dff['Longitude'] + 180) % 360) - 180)

    rodada = datafiles[0].split('/')[5].split('.')[0] #extract rodada information from the filename
    track_name = datafiles[0].split('/')[5].split('.')[0]#extract track information from the filename
    track_name = track_name.capitalize()

    ## extract lat and lon info from pandas data frame and convert to map scale
    lons = dff['Longitude'].values
    lats = dff['Latitude'].values
    x, y = m(lons, lats)

    ## plot the track
    m.plot(x, y,color=colors[jj],ms=4, zorder=4, label=f"TRACK {jj} ({rodada})")






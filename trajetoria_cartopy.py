#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:23:05 2023

@author: ladsin
"""
from mpl_toolkits.basemap import shiftgrid
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd
import glob
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader # Import shapefiles

lonmin, lonmax = -55, -30
latmin, latmax = -40, -15

# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(111)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

args = dict(color='gray',
            alpha=1.0, 
            linestyle='--', 
            linewidth=0.5,
            xlocs=np.arange(-180, 180, 30), 
            ylocs=np.arange(-90, -45, 10), 
            draw_labels=True)

gl = ax.gridlines(crs=ccrs.PlateCarree(), **args)
gl.xlabel_style = {'size': 15, 'color': 'black', 'rotation': 0}
gl.ylabel_style = {'size': 15, 'color': 'Gray', 'rotation': 0}
gl.top_labels = True
gl.right_labels = True
gl.bottom_labels = True
gl.rotate_labels = True
ax.set_extent([lonmin, lonmax, latmin, latmax], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.coastlines(resolution='50m', color='black', linewidth=1)

shapefile = list(
    shpreader.Reader(
    '/work/archive/Everson/Coqueiro/dados/br_unidades_da_federacao/BR_UF_2019.shp'
    ).geometries()
    )
ax.add_geometries(
    shapefile, ccrs.PlateCarree(), 
    edgecolor = 'black', 
    facecolor='none', 
    linewidth=0.5
    )

# m = Basemap(projection='merc', resolution="f", llcrnrlon=lonmin, llcrnrlat=latmin, urcrnrlon=lonmax, urcrnrlat=latmax)

# m.drawcoastlines(color='k',linewidth=0.5,zorder=3)
# m.drawcountries(color='k',linewidth=0.1,zorder=3)

# parallelmin = int(latmin)
# parallelmax = int(latmax)+1
# m.drawparallels(np.arange(parallelmin, parallelmax,5,dtype='int16').tolist(),labels=[1,0,0,0],linewidth=0,fontsize=10, zorder=3)

# meridianmin = int(lonmin)
# meridianmax = int(lonmax)+1
# m.drawmeridians(np.arange(meridianmin, meridianmax,5,dtype='int16').tolist(),labels=[0,0,0,1],linewidth=0,fontsize=10, zorder=3)

colors = ['C0','C1','C3','C2','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'] #default colors from Python (can be automated if the order is not important)
datafiles = glob.glob("/work/archive/Everson/Coqueiro/CENPES/DADOS/Track_recortados/*.csv") #to read individual data files containing the coordinates of the track for each typhoon
datafiles.sort()

for jj in range(6):
    #abre uma planilha por vez
    dff = pd.read_csv(datafiles[jj],sep=',', dtype={'time': object}) #read data file and time as string
    
    #converte a longitude de 0 - 360 para -180 a 180
    dff['Longitude'] = (((dff['Longitude'] + 180) % 360) - 180)
    
    # arredonda para resolução de 0.25 graus
    dff['Latitude'] = round(dff.Latitude / 0.25) * 0.25
    dff['Longitude'] = round(dff.Longitude / 0.25) * 0.25

    rodada = datafiles[0].split('/')[5].split('.')[0] #extract rodada information from the filename
    track_name = datafiles[0].split('/')[5].split('.')[0]#extract track information from the filename
    track_name = track_name.capitalize()
    
    
    lons = dff['Longitude'].values
    lats = dff['Latitude'].values
    # x, y = ax(lons, lats)
    

    # ## plot the track
    ax.plot(lons, lats,color=colors[jj],ms=4, zorder=4,  label=f"TRACK {jj} ({rodada})", )
    
    

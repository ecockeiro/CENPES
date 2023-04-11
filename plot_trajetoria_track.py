#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:23:05 2023

@author: everson

Esse script plota todas as trajetória dentro 
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader # Import shapefiles


# dataset
datafiles = glob.glob("/media/ladsin/DATA/Everson/Cenpes/Dados/planilhas_recortadas/*.csv")
datafiles.sort(reverse=True)

lonmin, lonmax = -55, -39
latmin, latmax = -40, -25

# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(111)
#to read individual data files containing the coordinates of the track for each typhoon
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

args = dict(draw_labels=True,
            linewidth=1, color='gray', 
            alpha=0.5, linestyle='--', 
            xlocs=np.arange(-180, 180, 3), 
            ylocs=np.arange(-50, 0, 3))


gl = ax.gridlines(crs=ccrs.PlateCarree(), **args)
gl.xlabel_style = {'size': 15, 'color': 'black', 'rotation': 0}
gl.ylabel_style = {'size': 15, 'color': 'black', 'rotation': 0}
gl.top_labels = False
gl.right_labels = False
gl.bottom_labels = True
gl.rotate_labels = True
ax.set_extent([lonmin, lonmax, latmin, latmax], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
# ax.add_feature(cfeature.OCEAN)
ax.coastlines(resolution='50m', color='black', linewidth=1)

shapefile = list(
    shpreader.Reader(
    '/media/ladsin/DATA/Heloisa/BR_UF_2021/BR_UF_2021.shp'
    ).geometries()
    )
ax.add_geometries(
    shapefile, ccrs.PlateCarree(), 
    edgecolor = 'black', 
    facecolor='none', 
    linewidth=0.5
    )

colors = ['C0','C1','C3','C2','C4','C5','C6','C7','C8','C9'] #default colors from Python (can be automated if the order is not important)


# Quantidade de ciclones para plotar
numero = 9

for jj in range(numero):
    #abre uma planilha por vez
    dff = pd.read_csv(datafiles[jj],sep=',', dtype={'Data': object}) #read data file and time as string
    
    #converte a longitude de 0 - 360 para -180 a 180
    dff['Longitude'] = (((dff['Longitude'] + 180) % 360) - 180)
    
    # arredonda para resolução de 0.25 graus
    # dff['Latitude'] = round(dff.Latitude / 0.25) * 0.25
    # dff['Longitude'] = round(dff.Longitude / 0.25) * 0.25

    rodada = datafiles[jj].split('/')[8].split('.')[0] #extract rodada information from the filename
    track_name = datafiles[0].split('/')[8].split('.')[0]#extract track information from the filename
    track_name = track_name.capitalize()
    
    lons = dff['Longitude'].values
    lats = dff['Latitude'].values
   
    ax.plot(lons, lats,color=colors[jj],linestyle='--', marker='o', ms=4, zorder=4, label=f"TRACK {jj} ({rodada})")
    ax.set_title(f"Trajetória do Yakecan - {(numero)} tracks", 
                 fontweight='bold', 
                 fontsize=20,)
    ax.legend(loc='upper left')
    
    plt.savefig(f'/media/ladsin/DATA/Everson/Cenpes/Dados/imagens/trajetória_yakecan_{(numero)}_tracks.png', bbox_inches='tight')

    




    
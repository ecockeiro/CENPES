#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 09:43:04 2023

@author: everson
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.feature as cfeature
import numpy as np

#dataset
df = pd.read_csv('/work/archive/Everson/Coqueiro/CENPES/DADOS/Tracks_planilhas/d-12.csv', sep=',')

#lat e lon extend da imagem
latmin, latmax = -45, -20
lonmin, lonmax = -60, -35

        
#converte e recorta latitude/longitude
df['Longitude'] = (((df['Longitude']+180) %360) -180)
data = df[(df.Longitude>=-55) & (df.Longitude<=-40) & (df.Latitude<=-29) & (df.Latitude>=-38)].copy()

#salva a planilha recortada
data.to_csv('/work/archive/Everson/Coqueiro/CENPES/DADOS/Track_recortados/d-12.csv')    

#plota os tracks
fig = plt.figure(figsize=(10,5))
args = dict(color='gray',
            alpha=1.0, 
            linestyle='--', 
            linewidth=0.5,
            xlocs=np.arange(lonmin, lonmax, 10), 
            ylocs=np.arange(latmin, latmax, 10), 
            draw_labels=True)

ax = plt.axes(projection=ccrs.PlateCarree())
gl = ax.gridlines(crs=ccrs.PlateCarree(), **args)
gl.xlabel_style = {'size': 15, 'color': 'black', 'rotation': 0}
gl.ylabel_style = {'size': 15, 'color': 'Gray', 'rotation': 0}
gl.top_labels = False
gl.right_labels = False
gl.bottom_labels = True
gl.rotate_labels = True
ax.set_extent([lonmin, lonmax, latmin, latmax], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.coastlines(resolution='50m', color='black', linewidth=1)

#one_ciclone = data[(data.N_do_Ciclone == 200)].copy()
def plot_cyclones(ciclone):

    for i in range(len(ciclone)-1):
        #print(range(len(ciclone)))
        #print(i)
        ciclone1 = ciclone.iloc[i]
        ciclone2 = ciclone.iloc[i+1]
        if i == 0:
            frist_lat, frist_lon = ciclone1.Latitude, ciclone1.Longitude
            second_lat, second_lon = ciclone2.Latitude, ciclone2.Longitude
            plt.plot([frist_lon, second_lon], [frist_lat, second_lat],
                     color='red',linewidth=0.5,
                     transform=ccrs.PlateCarree()
                     )
        else:
            if i == len(ciclone)-2:
                frist_lat, frist_lon = ciclone1.Latitude, ciclone1.Longitude
                second_lat, second_lon = ciclone2.Latitude, ciclone2.Longitude
                plt.plot([frist_lon, second_lon], [frist_lat, second_lat],
                     color='black',linewidth=0.5,
                     transform=ccrs.PlateCarree()
                     )
            else:
                frist_lat, frist_lon = ciclone1.Latitude, ciclone1.Longitude
                second_lat, second_lon = ciclone2.Latitude, ciclone2.Longitude
                plt.plot([frist_lon, second_lon], [frist_lat, second_lat],
                     color='blue',linewidth=0.5,
                     transform=ccrs.PlateCarree()
                     )



ciclones = list( dict.fromkeys(data.N_do_Ciclone) )

for Ciclone in ciclones:
    one_ciclone = data[(data.N_do_Ciclone == Ciclone)].copy()
    plot_cyclones(one_ciclone)
    
    
    
plt.show()

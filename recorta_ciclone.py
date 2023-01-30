#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 09:43:04 2023

@author: everson
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd

df = pd.read_csv('/home/everson/CENPES/dados_track/d_1705.csv')

dia_inicial = int(17)
dia_final = int(20)

df2 = pd.DataFrame()
for linha in df.itertuples():
	#print(linha.Data)
	dia = linha.Data.split()[0]
	if int(dia[-2:]) >= dia_inicial and int(dia[-2:]) <=dia_final:
		#print(linha.split())
		df2 = df2.append(pd.DataFrame([linha]), ignore_index=True)
		#print(df2.head())
		#break
        
#df2 = df[(df.Longitude>=0) & (df.Latitude<=-29) & (df.Latitude>=-38)].copy()
df2 = df[(df.Longitude>=308) & (df.Longitude<=342) & (df.Latitude<=-29) & (df.Latitude>=-38)].copy()

df2.to_csv('d_1705_nova.csv')    



data = pd.read_csv('d_1705_nova.csv')
ax = plt.axes(projection=ccrs.Robinson())
ax.coastlines()

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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 11:56:31 2023

@author: bjerknes
"""
import metpy.calc as mpcalc
from metpy.units import units
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.feature as cfeature
import glob 
import os
import xarray as xr



# Calculo da vorticidade relativa em 850hPa

# Dataset vento
vento = xr.open_mfdataset('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/nc/dados_extraidos/vento/*.nc')

# Seleciona o nivel
vento_850 = vento.sel(level0=850)

# Atribuiçao de nome mais elucidativo 
vento['u'] = vento_850['U_GRD_L100'].copy()
vento['v'] = vento_850['V_GRD_L100'].copy()

# Vai preenchendo o np.array...
vort_850= mpcalc.vorticity(vento.u, vento.v)

# Cria o datarray dentro da estrutura do dado 
vento['vo'] = vento['u'].copy()
vento['vo'].data = vort_850
vento['vo'] = xr.DataArray(vort_850, dims = ['time','lat','lon'])   
vento['vo'].attrs['standard_name'] = 'atmosphere_relative_vorticity'
vento['vo'].attrs['long_name'] = 'Vorticity (relative)'
vento['vo'].attrs['units'] = 's**-1'
vento['lat'].attrs['units'] = 'degrees_north'
vento['lon'].attrs['units'] = 'degrees_east'

# Deixa somente o vort_850 dentro do data
vor = vento[['vo']]
vor = vor.chunk()
##########################################################################################################################

# Dataset pressao
pressao = xr.open_mfdataset('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/nc/dados_extraidos/pressao/*.nc')

# Diretório com os CSVs
directory = glob.glob('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Ciclones/novo_extra/*.csv')



analise_era_5 = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Raoni/Tracks_recortados/analise_era5_raoni.csv')
analise_era_5['Data'] = analise_era_5['Data'].str.replace('"', '')
analise_era_5['Data'] = analise_era_5['Data'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

planilha_total = pd.DataFrame({'Date': analise_era_5['Data']})
plt.figure(figsize=(15,10))
for j, csv_file in enumerate(directory):
    
    csv = pd.read_csv(csv_file)
    col = csv_file.split('/')[-1].split('.')[0]
    planilha_total[col] = csv['Vorticidade']
    planilha_total_nan =  planilha_total.dropna()
    plt.plot(planilha_total_nan['Date'], planilha_total_nan[col] * -1, label=f'{col}')
    
    plt.xticks(rotation=45)

plt.legend()
plt.show()

# Cores para atribuir a cada DataFrame
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Criar uma figura para o gráfico
plt.figure(figsize=(10, 6))

# Loop para ler cada CSV e atribuir uma cor
for i, csv_file in enumerate(datafiles):
    csv_data = pd.read_csv(csv_file)
    color = colors[i % len(colors)]  # Cicla as cores se houver mais CSVs do que cores
    plt.plot(csv_data['Data'], csv_data['Vorticidade'] * -1, label=f'Dados {i}', color=color)

plt.xlabel('Data')
plt.ylabel('Vorticidade')
plt.title('Vorticidade de Todos os CSVs')
# plt.grid(True)
plt.legend()
plt.show()

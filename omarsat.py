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
import numpy as np




# Dataset vento
diretorio_pastas = '/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/Ciclones/Yakecan/dados_nc/Yakecan/vento'

# função que lê as pastas em um diretório
def get_folders(directory):
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

# lista de pasta para serem selecionadas
folders = get_folders(diretorio_pastas)
folders.sort(reverse=False)

nome_ciclone = diretorio_pastas.split('/')[10]

# Converte as componentes u e v em vorticidade relativa 
for j in range(len(folders)):
    
    csv = pd.read_csv(f'/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/Ciclones/Yakecan/Todos/{folders[j]}.csv')
    csv['Data'] = csv['Data'].str.replace(' "', '').str.replace(' ', 'T').str.replace('"', '.000000000')
    
    
    path_name = os.path.join(diretorio_pastas, folders[j])
    vento = xr.open_mfdataset(f'{path_name}/*.nc')
    
    pressao_name = path_name.replace('vento', 'pressao')
   
    csv_novo = pd.DataFrame({'N_do_Ciclone': csv['N_do_Ciclone'].values,'date': csv['Data'].values, 'lat': csv['Latitude'].values, 'lon': csv['Longitude'].values, 'vento_mag': csv['Data'].values, 'vort':csv['Data'].values, 'pressao':csv['Data'].values })
    
    if folders[j] == '0_ERA5':
        pressao_era5 = xr.open_mfdataset(f'{pressao_name}/*.nc')
        vort_era5 = xr.open_dataset('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/Ciclones/Yakecan/dados_nc/Yakecan/vorticidade/era_vort.nc')
        vento_era5 = xr.open_mfdataset(f'{path_name}/*.nc')
        
        for k in range(len(csv['Data'])):
            
            tempo = csv['Data'][k]
            latitude = csv['Latitude'][k]
            longitude = csv['Longitude'][k]
            
            mag_vento = np.sqrt(vento_era5.u**2 + vento_era5.u**2)
            vento_mag = mag_vento.sel(time=tempo, latitude=latitude, longitude=longitude, level=900, method='nearest')
            vento_magnitude = vento_mag.values.tolist()  # Converte os valores em uma lista
            csv_novo.loc[k,'vento_mag'] = vento_magnitude
            
            vorticidade = vort_era5.vo.sel(time=tempo, latitude=latitude, longitude=longitude, method='nearest')
            vor_list =  vorticidade.values.tolist()
            csv_novo.loc[k, 'vort'] = vor_list
            
            pressao_nc = pressao_era5.msl.sel(time=tempo, latitude=latitude, longitude=longitude, method='nearest')/100
            pressao_list = pressao_nc.values.tolist()
            csv_novo.loc[k, 'pressao'] = pressao_list
            
            csv_novo.to_csv(f'/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/{nome_ciclone}/{folders[j]}.csv', index=False)
    
    else:
        pressao = xr.open_mfdataset(f'{pressao_name}/*.nc')
        pressao = pressao.assign_coords(dict(lon = (((pressao.lon.values + 180) % 360) - 180))).sortby('lon')
        vento = vento.assign_coords(dict(lon = (((vento.lon.values + 180) % 360) - 180))).sortby('lon')   
        # Calculo da vorticidade relativa em 850hPa
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
        
        for i in range(len(csv['Data'])):
            tempo = csv['Data'][i]
            latitude = csv['Latitude'][i]
            longitude = csv['Longitude'][i]
            
            mag_vento = np.sqrt(vento.U_GRD_L100**2 + vento.V_GRD_L100**2)
            vento_mag = mag_vento.sel(time=tempo, level0 = 900, lat=latitude, lon=longitude, method='nearest')
            vento_magnitude = vento_mag.values.tolist()  # Converte os valores em uma lista
            csv_novo.loc[i,'vento_mag'] = vento_magnitude
            
            vorticidade = vor.vo.sel(time=tempo, lat=latitude, lon=longitude, method='nearest')
            vor_list =  vorticidade.values.tolist()
            csv_novo.loc[i, 'vort'] = vor_list
            
            pressao_nc = pressao.PRMSL_L101.sel(time=tempo, lat=latitude, lon=longitude, method='nearest')/100
            pressao_list = pressao_nc.values.tolist()
            csv_novo.loc[i, 'pressao'] = pressao_list
            
            csv_novo.to_csv(f'/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/{nome_ciclone}/{folders[j]}.csv', index=False)
        

##########################################################################################################################


# Lista de arquivos CSV na pasta
pasta_plan = sorted(glob.glob('/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/Yakecan/*.csv'))
variaveis_name = ['Vorticidade relativa negativa', 'Pressao', 'Vento (900 Hpa)']

# Lê a primeira planilha e converte as datas
plan_fixa = pd.read_csv(pasta_plan[0])
plan_fixa['date'] = pd.to_datetime(plan_fixa['date'])

# Extrai o nome do arquivo (sem caminho e extensão)
rodada_name = os.path.basename(pasta_plan[0]).split('.')[0]

# Cria um DataFrame vazio para armazenar os dados combinados
combined_data = plan_fixa[['date']]

# Configuração para criar subplots com espaço entre eles
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(18, 12), sharex=True, gridspec_kw={'hspace': 0.2})

# Variáveis a serem plotadas
variables = ['vort', 'pressao', 'vento_mag']

# Lista para armazenar as alças das legendas
legend_handles = []

# Cores e marcadores personalizados
custom_colors = ['blue', 'red', 'gold', 'cyan', 'brown', 'darkgreen', 'dimgray', 'darkorchid', 'lightsteelblue', 'lightpink']
custom_markers = ['o', 's', '^', 'v', 'x', '+', '*', 'D', '|', '_']

# Loop sobre as variáveis
for i, var_name in enumerate(variables):
    
    # Loop sobre os arquivos
    for j, arquivo in enumerate(pasta_plan[:10]):
        plan_var = pd.read_csv(arquivo)
        plan_var['date'] = pd.to_datetime(plan_var['date'])
        plan_var['vort'] = plan_var['vort']*10**5
    
        # Extrai o nome do arquivo (sem caminho e extensão)
        rodada_name = os.path.basename(arquivo).split('.')[0]
    
        # Mescla os DataFrames com base na coluna 'date'
        combined_data_new = combined_data.merge(plan_var[['date', var_name]], on='date', how='left')
    
        # Define a cor e marcador da série atual
        line_color = custom_colors[j] if j < 10 else 'gray'  # Usar cores personalizadas
        line_marker = custom_markers[j] if j < 10 else 'o'  # Usar marcadores personalizados
    
        # Plotar a série temporal da planilha atual no subplot correspondente com a cor e marcador definidos
        axes[i].plot(combined_data_new['date'], combined_data_new[var_name], label=rodada_name, color=line_color, marker=line_marker)
    
    # Adicionar o nome da variável à esquerda de cada gráfico
    axes[i].set_ylabel(variaveis_name[i], fontsize=16)
    axes[i].tick_params(axis='x', labelrotation=45, labelsize=18)
    
    # Coletar alças das legendas
    handles, labels = axes[i].get_legend_handles_labels()
    legend_handles.extend(handles)

# Título da figura como um todo com posição ajustada
fig.suptitle('Yakecan', fontsize=30, y=1.02)

# Adicionar a única legenda centralizada no lado direito
plt.legend(legend_handles, labels, loc='center right', bbox_to_anchor=(1.15, 1.6), fontsize=14)

plt.tight_layout()
plt.show()

# Salvar a figura em um arquivo PNG
fig.savefig(f'/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/imagens/{nome_ciclone}.png', bbox_inches='tight', dpi=300)  # Substitua o caminho pelo desejado

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 15:52:58 2023

@author: everson

Esse script faz os seguintes ajustes:

    I - Carrega a pasta contendo todas as planilhas dos Tracks
    II - Adiciona os rótulos nas colunas, pois quando o track gera as planilhas geram planilhas sem rótulos
    III - Converte as longitudes para -180 a 180 graus
    IV - Remove a ocorrencia de ciclones a partir de um numero pré-definido
    V - Salva a planilha dentro da pasta automaticamente a partir do rotulo 'Data'
    
"""

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.feature as cfeature
import numpy as np
import glob 
import os


# I.1 - Carrega as pastas contendo todas as planilhas dos Tracks, dentro de um diretório

# A função abaixo é usada para quando você tiver pasta de arquivos track, se o seu caso for uma unica pasta 
#com multiplas planilhas utilize o comando I.2

# # função que lê as pastas em um diretório
# def get_folders(directory):
#     return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
# # diretório
# directories = '/media/ladsin/DATA/Everson/Cenpes/Dados/Tracks_planilhas'

# # lista de pasta para serem selecionadas
# folders = get_folders(directories)


# # loop através de cada diretório e ler arquivos csv
# for j in range(len(folders)):
#     path_name = str(directories) + '/' + str(folders[j])
#     datafiles = glob.glob(f'{path_name}/*.csv')
#     datafiles.sort()

# I.2 - Carrega a pasta contendo todas as planilhas dos Tracks

datafiles = glob.glob('/media/ladsin/DATA/Everson/Cenpes/Dados/Tracks_planilhas/*.csv')
datafiles.sort()

# range = ao numero de meses, poderia usar o range(len(datafiles))
for i in range(len(datafiles)):
    
    
    # II - Adiciona os rótulos nas colunas, pois quando o track gera as planilhas geram planilhas sem rótulos
    
    #seleciona a planilha
    path = np.array(pd.read_csv(datafiles[i], sep=',', usecols=[0, 1, 2, 3, 4]))
    
    #adiciona os rotulos das colunas
    df = pd.DataFrame(path, columns = ['N_do_Ciclone', 'Data', 'Longitude', 'Latitude', 'Vorticidade'])
    
    data = datafiles[i].split('/')[8].split('.')[0]
    
    
    # III - Converte as longitudes para -180 a 180 graus
    
    # converte e recorta latitude/longitude
    df['Longitude'] = (((df['Longitude']+180) %360) - 180)
    
    df = df[(df.Longitude>=-52) & (df.Longitude<=-40) & (df.Latitude<=-27) & (df.Latitude>=-39)].copy()
    
    
    # IV - Remove a ocorrencia de ciclones a partir de um numero pré-definido (exemplo = 4)
    
    # Conta a ocorrência de cada item
    counts = df['N_do_Ciclone'].value_counts()
    
    # Cria uma lista com os ciclones a serem removidos
    itens_para_remover = counts[counts < 7].index.tolist()
    
    # Remove os ciclones da lista do DataFrame
    df = df[~df['N_do_Ciclone'].isin(itens_para_remover)]
    
    
    # V - Salva a planilha dentro da pasta automaticamente a partir do rotulo 'Data'
    
    #salva a planilha recortada
    df.to_csv(f'/media/ladsin/DATA/Everson/Cenpes/Dados/planilhas_recortadas/{(data)}.csv', index=False)    
    
    
    '''
    # plota os tracks
    # Caso queira plotar as saídas das planilhas descomente essa parte!
    
    #lat e lon extend da imagem
    latmin, latmax = -45, -20
    lonmin, lonmax = -65, -30
    
    fig = plt.figure(figsize=(10,5))
    args = dict(color='gray',
                alpha=1.0, 
                linestyle='--', 
                linewidth=0.5,
                xlocs=np.arange(lonmin, lonmax, 10), 
                ylocs=np.arange(latmin, latmax, 10), 
                draw_labels=True)
    
    
    # Criação da projeção cartesiana

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
    
    
    # # Criação da projeção polar centrada na Antártica

    # ax = plt.axes(projection=ccrs.SouthPolarStereo())

    # gl = ax.gridlines(crs=ccrs.PlateCarree(), **args)
    # gl.xlabel_style = {'size': 15, 'color': 'black', 'rotation': 0}
    # gl.ylabel_style = {'size': 15, 'color': 'Gray', 'rotation': 0}
    # gl.top_labels = False
    # gl.right_labels = False
    # gl.bottom_labels = True
    # gl.rotate_labels = True
    # ax.set_extent([lonmin, lonmax, latmin, latmax], ccrs.PlateCarree())
    # ax.add_feature(cfeature.LAND)
    # ax.coastlines(resolution='50m', color='black', linewidth=1)
    
    
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



    ciclones = list( dict.fromkeys(df.N_do_Ciclone) )

    for Ciclone in ciclones:
        one_ciclone = df[(df.N_do_Ciclone == Ciclone)].copy()
        plot_cyclones(one_ciclone)
        
        
        
    plt.show()
    '''
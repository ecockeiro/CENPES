#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:45:00 2023

@author: ladsin
"""
import math
import glob 
import pandas as pd
import numpy as np
from collections import OrderedDict


def calcular_distancia(lat1, lon1, lat2, lon2):
    # Converter graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Raio médio da Terra em km
    raio = 6371

    # Diferenças de latitude e longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Distância em km
    distancia = round(raio * c, 2)

    return distancia


# dataset
rodada = glob.glob("/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/Planilhas_normalizadas/Rodadas/*.csv")
rodada.sort(reverse=True)

referencia = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/Planilhas_normalizadas/Analise/analise_era5.csv')
ref_count = len(referencia['N_do_Ciclone'])

# Hora de previsao
hf= 0

# Nova planilha
columns = []
index = []
df = pd.DataFrame()

for i in range(len(rodada[:11])):
    comparacao = pd.read_csv(rodada[i])
    comp_count = len(comparacao['N_do_Ciclone'])
    if comp_count > ref_count:
        for k in range(len(comparacao[:ref_count])):
            distancia = calcular_distancia(comparacao['Latitude'][k], comparacao['Longitude'][k], referencia['Latitude'][k], referencia['Longitude'][k])
            distancia = round(distancia, 2)
           
            nome = rodada[i].split('/')
            rodada_nome = nome[-1].split('.')[0]
            
        
            data_comp = referencia['Data'][k].split('"')[1]
            nome_comp = rodada_nome + '/' + data_comp
            
            data_ref = referencia['Data'][k].split('"')[1]
            nome_ref = 'analise ERA5' + '/' + data_ref
            
            hora_dia = comparacao['Data'][k].split(' ')[2].split(':')[0] + 'Z' + comparacao['Data'][k].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][k].split(' ')[1].split('"')[1].split('-')[1]
            index.append(hora_dia)
        # columns.append(f'{hf}h')
 

            
            # print("Distância entre {} e {}:".format(nome_ref,nome_comp), distancia, "km")
            
    
    
    else:
        for l in range(len(comparacao[:comp_count])):        
            distancia = calcular_distancia(comparacao['Latitude'][l], comparacao['Longitude'][l], referencia['Latitude'][l], referencia['Longitude'][l])
            distancia = round(distancia, 2)
            
            nome = rodada[i].split('/')
            rodada_nome = nome[-1].split('.')[0]
            
        
            data_comp = referencia['Data'][l].split('"')[1]
            nome_comp = rodada_nome + '/' + data_comp
            
            data_ref = referencia['Data'][l].split('"')[1]
            nome_ref = 'analise ERA5' + '/' + data_ref
             
            
            # print("Distância entre {} e {}:".format(nome_ref,nome_comp), distancia, "km")
            data = comparacao['Data'][l].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][l].split(' ')[1].split('"')[1].split('-')[1]
            hora_dia = comparacao['Data'][l].split(' ')[2].split(':')[0] + 'Z' + data
            index.append(hora_dia)
        
    
    columns.append(f'{hf}h')
    hf +=24
    print(index)
    valores_1705 = set([valor for valor in index if valor.endswith(data)])
    
    
index_sorted = sorted(list(set(index)))
df = pd.DataFrame(columns,index)
print(df)
# hora_dict = {}
# for i in range(len(rodada[:11])):
#     comparacao = pd.read_csv(rodada[i])
#     comp_count = len(comparacao['N_do_Ciclone'])
#     if comp_count > ref_count:
#         for k in range(len(comparacao[:ref_count])):
#             hora_dia = comparacao['Data'][k].split(' ')[2].split(':')[0] + 'Z' + comparacao['Data'][k].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][k].split(' ')[1].split('"')[1].split('-')[1]
#             if hora_dia not in hora_dict.values():
#                 for l, col in enumerate(columns):
#                     if col.endswith('h'):
#                         hora_dict.setdefault(col, [])
#                         hora_dict[col].append(hora_dia)
                        
#     else:
#         for l in range(len(comparacao[:comp_count])):
#             hora_dia = comparacao['Data'][l].split(' ')[2].split(':')[0] + 'Z' + comparacao['Data'][l].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][l].split(' ')[1].split('"')[1].split('-')[1]
#             if hora_dia not in hora_dict.values():
#                 for m, col in enumerate(columns):
#                     if col.endswith('h'):
#                         hora_dict.setdefault(col, [])
#                         hora_dict[col].append(hora_dia)
                        
    #         d_list = []
    #         d_list.append(distancia)
            
            
    #         distancia.append()
    #         data = {f'{hf}h': [distancia, 2, 3],
    #         'Coluna 2': [4, 5, 6],
    #         'Coluna 3': [7, 8, 9]}
    # df = pd.DataFrame(data, index=['Linha 1', 'Linha 2', 'Linha 3'])

        
    # for j in range(len(referencia['Data'])):
    #     nome = rodada[i].split('/')
    #     rodada_nome = nome[-1].split('.')[0]
        
    
    #     data_comp = referencia['Data'][j].split('"')[1]
    #     nome_comp = rodada_nome + '/' + data_comp
        
    #     data_ref = referencia['Data'][j].split('"')[1]
    #     nome_ref = 'analise ERA5' + '/' + data_ref
         
        
    #     distancia = calcular_distancia(comparacao['Latitude'][j], comparacao['Longitude'][j], referencia['Latitude'][j], referencia['Longitude'][j])
    #     distancia = round(distancia, 2)
    #     print("Distância entre {} e {}:".format(nome_ref,nome_comp), distancia, "km")
    #     print(distancia)
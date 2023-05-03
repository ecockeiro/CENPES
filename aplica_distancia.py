#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:21:31 2023

@author: bjerknes
"""

import math
import glob 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

planilha_nova = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/distancia/distancia_yakecan.csv')
count_hora = 0

# Loop de planilhas csv
for i in range(len(rodada[:11])):
    


    comparacao = pd.read_csv(rodada[i])
    comp_count = len(comparacao['N_do_Ciclone'])
    
    # Loop de linhas 
    if comp_count > ref_count:
        for k in range(len(comparacao[:ref_count])-1):
            distancia = calcular_distancia(comparacao['Latitude'][k], comparacao['Longitude'][k], referencia['Latitude'][k], referencia['Longitude'][k])
            dist = round(distancia, 2)
            
            planilha_nova[f'{count_hora}h'][k] = dist 
            
        count_hora += 24
        
    
    else:
        for l in range(len(comparacao[:comp_count])-1):        
            distancia = calcular_distancia(comparacao['Latitude'][l], comparacao['Longitude'][l], referencia['Latitude'][l], referencia['Longitude'][l])
            dist = round(distancia, 2)
        
            planilha_nova[f'{count_hora}h'][l] = dist 
            
        count_hora += 24
    
planilha_nova.to_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/distancia/dist_yakecan.csv', index=False, header=True)


            
           
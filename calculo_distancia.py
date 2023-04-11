#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:45:00 2023

@author: ladsin
"""
import math
import glob 
import pandas as pd

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
datafiles = glob.glob("/work/archive/Everson/Coqueiro/CENPES/DADOS/Yakecan/Planilhas_normalizadas/*.csv")
datafiles.sort(reverse=True)

referencia = pd.read_csv(datafiles[0])

for i in range(1,len(datafiles[1:])):
    comparacao = pd.read_csv(datafiles[i])
    
    for j in range(len(referencia['Data'])):
        rodada = datafiles[i].split('/')[9].split('.')[0]      
        data_comp = referencia['Data'][j].split('"')[1]
        nome_comp = rodada + '/' + data_comp
        
        analise = datafiles[0].split('/')[9].split('.')[0]
        data_ref = referencia['Data'][j].split('"')[1]
        nome_ref = analise + '/' + data_ref
         
        
        distancia = calcular_distancia(comparacao['Latitude'][j], comparacao['Longitude'][j], referencia['Latitude'][j], referencia['Longitude'][j])
        distancia = round(distancia, 2)
        print("Distância entre {} e {}:".format(nome_ref,nome_comp), distancia, "km")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:48:18 2023

@author: bjerknes
"""

import math
import glob 
import pandas as pd
import numpy as np

# dataset
rodada = glob.glob("/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/Planilhas_normalizadas/Rodadas/*.csv")
rodada.sort(reverse=True)

referencia = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/Planilhas_normalizadas/Analise/analise_era5.csv')


# Hora de previsao

# Nova planilha
columns = []
index = []
list_hora = []
df = pd.DataFrame()
hf= 0
ref_count = len(referencia['N_do_Ciclone'])
hora = 0

for i in range(len(rodada[:11])):
    comparacao = pd.read_csv(rodada[i])
    comp_count = len(comparacao['N_do_Ciclone'])
    if comp_count > ref_count:
        for k in range(len(comparacao[:ref_count])-1):
 
            data_1 = comparacao['Data'][k].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][k].split(' ')[1].split('"')[1].split('-')[1]
            data_2 = comparacao['Data'][k+1].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][k+1].split(' ')[1].split('"')[1].split('-')[1]

            hora_dia = comparacao['Data'][k].split(' ')[2].split(':')[0] + 'Z' + data_1
            index.append(hora_dia)
            print(hora_dia)

    else:
        for l in range(len(comparacao[:comp_count])-1):        

            data_1 = comparacao['Data'][l].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][l].split(' ')[1].split('"')[1].split('-')[1]
            data_2 = comparacao['Data'][l+1].split(' ')[1].split('"')[1].split('-')[2] + comparacao['Data'][l+1].split(' ')[1].split('"')[1].split('-')[1]

            hora_dia = comparacao['Data'][l].split(' ')[2].split(':')[0] + 'Z' + data_1
            index.append(hora_dia)
            print(hora_dia)


    columns.append(f'{hf}h')
    
    hf +=24
    print(columns)    
        
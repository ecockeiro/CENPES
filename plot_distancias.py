#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:58:32 2023

@author: ladsin
"""

import matplotlib.pyplot as plt
import datetime
import pandas as pd

df = pd.read_csv('/home/ladsin/Coqueiro/Tracks_planilhas/tabela_distancia.csv')
    

# Criando o gráfico de linhas
plt.figure(figsize=(12, 10)) # Define o tamanho da figura
plt.plot(df['Data'], df['D-0'], label='D-0')
plt.plot(df['Data'], df['D-1'], label='D-1')
plt.plot(df['Data'], df['D-2'], label='D-2')
plt.plot(df['Data'], df['D-3'], label='D-3')
plt.plot(df['Data'], df['D-4'], label='D-4')
plt.plot(df['Data'], df['D-5'], label='D-5')
plt.plot(df['Data'], df['D-6'], label='D-6')
plt.plot(df['Data'], df['D-7'], label='D-7')

# Configurando os eixos e a legenda
plt.xlabel('Dia e hora')
plt.ylabel('Distância em Km entre a rodada e o observado')
plt.legend(title='Rodadas')

plt.savefig(f'/home/ladsin/Coqueiro/Tracks_planilhas/imagens/distancias_tracks.png', bbox_inches='tight')
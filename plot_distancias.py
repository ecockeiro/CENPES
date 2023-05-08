#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:58:32 2023

@author: ladsin
"""

import matplotlib.pyplot as plt
import datetime
import pandas as pd

df = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Sintese/Extratropical/Distancia/Extra_distancia.csv')
    

# Criando o gráfico de linhas
plt.figure(figsize=(23, 10), dpi=300) # Define o tamanho da figura
# plt.plot(df['Data'], df['0h'], label='D-0')
# plt.plot(df['Data'], df['24h'], label='D-1')
# plt.plot(df['Data'], df['48h'], label='D-2')
# plt.plot(df['Data'], df['72h'], label='D-3')
# plt.plot(df['Data'], df['96h'], label='D-4')
# plt.plot(df['Data'], df['120h'], label='D-5')
# plt.plot(df['Data'], df['144h'], label='D-6')
# plt.plot(df['Data'], df['168h'], label='D-7')

plt.plot(df['Data'], df['0h'], label='0h')
plt.plot(df['Data'], df['24h'], label='24h')
plt.plot(df['Data'], df['48h'], label='48h')
plt.plot(df['Data'], df['72h'], label='72h')
plt.plot(df['Data'], df['96h'], label='96h')
plt.plot(df['Data'], df['120h'], label='120h')
plt.plot(df['Data'], df['144h'], label='144h')
plt.plot(df['Data'], df['168h'], label='168h')
plt.plot(df['Data'], df['192h'], label='192h')
plt.plot(df['Data'], df['216h'], label='216h')
plt.plot(df['Data'], df['240h'], label='240h')

# Configurando os eixos e a legenda
plt.xlabel('Dia e hora', fontsize=20)
plt.ylabel('Distância em Km entre a rodada e o observado', fontsize=20)
plt.xlabel_style = {'size': 15, 'color': 'black'}
plt.ylabel_style = {'size': 15, 'color': 'black'}
plt.legend(title='Rodadas', loc='upper right', fontsize=15, title_fontsize=20)
plt.title('Extratopical', fontsize=24)

plt.savefig(f'/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/Imagens/Gráficos/Extratropical/Extratropical_hora.png', bbox_inches='tight')
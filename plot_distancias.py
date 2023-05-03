#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:58:32 2023

@author: ladsin
"""

import matplotlib.pyplot as plt
import datetime
import pandas as pd

df = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Yakecan/distancia/dist_yakecan.csv')
    

# Criando o gráfico de linhas
plt.figure(figsize=(20, 10)) # Define o tamanho da figura
plt.plot(df['Data'], df['0h'], label='D-0')
plt.plot(df['Data'], df['24h'], label='D-1')
plt.plot(df['Data'], df['48h'], label='D-2')
plt.plot(df['Data'], df['72h'], label='D-3')
plt.plot(df['Data'], df['96h'], label='D-4')
plt.plot(df['Data'], df['120h'], label='D-5')
plt.plot(df['Data'], df['144h'], label='D-6')
plt.plot(df['Data'], df['168h'], label='D-7')

# plt.plot(df['Data'], df['0h'], label='0h')
# plt.plot(df['Data'], df['24h'], label='24h')
# plt.plot(df['Data'], df['48h'], label='48h')
# plt.plot(df['Data'], df['72h'], label='72h')
# plt.plot(df['Data'], df['96h'], label='96h')
# plt.plot(df['Data'], df['120h'], label='120h')
# plt.plot(df['Data'], df['144h'], label='144h')
# plt.plot(df['Data'], df['168h'], label='168h')

# plt.plot(df['Data'], df['192h'], label='D-8')
# plt.plot(df['Data'], df['216h'], label='D-9')
# plt.plot(df['Data'], df['240h'], label='D-10')

# Configurando os eixos e a legenda
plt.xlabel('Dia e hora')
plt.ylabel('Distância em Km entre a rodada e o observado')
plt.legend(title='Rodadas')
plt.title('Yakecan')

plt.savefig(f'/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/Imagens/Gráficos/Yakecan/Yakecan_delay.png', bbox_inches='tight')
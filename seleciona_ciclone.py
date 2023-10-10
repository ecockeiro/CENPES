#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 14:15:53 2023

@author: bjerknes
"""

import pandas as pd
import numpy as np
import glob
import os

# Supondo que seus dados estejam em um arquivo CSV chamado 'dados.csv' com cabeçalhos de coluna 'A', 'B', 'C', 'D', 'E'
# Você pode carregar os dados em um DataFrame do Pandas

master = glob.glob('/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Extratropical/planilhas_csv/*.csv')
filtrada = '/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Ciclones/Extratropical/'

for i in master:
    
    name_final = i.split('/')[-1].split('.')[0]
    name_csv = i.split('/')[-1]
    path_master = np.array(pd.read_csv(i, sep=',', usecols=[0, 1, 2, 3, 4]))
    #adiciona os rotulos das colunas
    df = pd.DataFrame(path_master, columns = ['N_do_Ciclone', 'Data', 'Longitude', 'Latitude', 'Vorticidade'])
    # converte e recorta latitude/longitude
    df['Longitude'] = (((df['Longitude']+180) %360) - 180)
    
    path_filtrada = pd.read_csv(os.path.join(filtrada, name_csv), sep=',', usecols=[0, 1, 2, 3, 4])
    
    
    # Agrupe os dados com base no valor da primeira coluna (Coluna1)
    grupos = df.groupby('N_do_Ciclone')
    
    # Selecione o grupo específico com o número desejado (por exemplo, número 2)
    numero_desejado = path_filtrada['N_do_Ciclone'][0]
    grupo_selecionado = grupos.get_group(numero_desejado)
    grupo_selecionado.to_csv(f'/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Ciclones/novo_extra/{name_final}.csv',index=False)
    
    


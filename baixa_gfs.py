#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 17:12:16 2022

@author: everson
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from netCDF4 import num2date
from siphon.catalog import TDSCatalog


dia = 17
count = 0
forecast = 0 #+8

# Contador de dias com delay
while count <= 13:
    # Abre o catalogo
    dados_gfs = TDSCatalog(f'https://rda.ucar.edu/thredds/catalog/files/g/ds084.1/2022/202205{dia}/catalog.xml')
    validade = dados_gfs.datasets[:25+forecast]
    
    for indice in range(len(validade)):
        print (indice)
        for rodada in validade[indice]:
            print(rodada)
        

count = count + 1
forecast = forecast + 8    
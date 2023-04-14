#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:19:09 2023

@author: ladsin
"""
import os
import tarfile
import glob



# Diretorio de arquivos .tar
arq_tar = glob.glob('/work/archive/Everson/Coqueiro/CENPES/DADOS/dados-raoni/dados_tar/*.tar')

# Define o diretório onde as pastas serão criadas
pasta_dir = "/work/archive/Everson/Coqueiro/CENPES/DADOS/dados-raoni/dados_input_vort/"

# Lista de rodadas 00Z
list_rod = ['gfs.0p25.2021062900.f000.grib2.nc', 
            'gfs.0p25.2021062800.f000.grib2.nc', 
            'gfs.0p25.2021062700.f000.grib2.nc', 
            'gfs.0p25.2021062600.f000.grib2.nc',
            'gfs.0p25.2021062500.f000.grib2.nc', 
            'gfs.0p25.2021062400.f000.grib2.nc', 
            'gfs.0p25.2021062300.f000.grib2.nc', 
            'gfs.0p25.2021062200.f000.grib2.nc', 
            'gfs.0p25.2021062100.f000.grib2.nc', 
            'gfs.0p25.2021062000.f000.grib2.nc', 
            'gfs.0p25.2021061900.f000.grib2.nc',
            'gfs.0p25.2021061800.f000.grib2.nc',
            'gfs.0p25.2021061700.f000.grib2.nc',]

for k in arq_tar:
    # Abre o arquivo .tar usando o comando tarfile.open()
    with tarfile.open(k, "r") as tar:
        # Obtém uma lista de todos os arquivos .nc no arquivo .tar
        arquivos_nc = [f for f in tar.getnames() if f.endswith(".nc")]
        membros = tar.getmembers()
        
        for j, membros in enumerate(membros):
            for membros in tar.getmembers():
                if any(nome_arquivo in membros.name for nome_arquivo in list_rod):
                    print(f"O arquivo {membros.name} está na posição {j} no arquivo .tar")
        
    
    
        # Define o tamanho do grupo de arquivos .nc que serão extraídos juntos
        tamanho_grupo = 20
    
        # Loop através dos arquivos .nc em grupos de tamanho_grupo
        for i in range(0, len(arquivos_nc), tamanho_grupo):
            # Cria uma nova pasta para cada grupo de arquivos .nc
            nome_pasta = "Pasta {}".format(i // tamanho_grupo + 1)
            os.mkdir(os.path.join(pasta_dir, nome_pasta))
    
            # Extrai cada arquivo .nc do grupo para a pasta correspondente
            for arquivo_nc in arquivos_nc[i:i + tamanho_grupo]:
                tar.extract(arquivo_nc, os.path.join(pasta_dir, nome_pasta))
    
                # Renomeia o arquivo para incluir o nome da pasta
                novo_nome = "{}_{}".format(nome_pasta, os.path.basename(arquivo_nc))
                os.rename(os.path.join(pasta_dir, nome_pasta, arquivo_nc),
                          os.path.join(pasta_dir, nome_pasta, novo_nome))
                tamanho_grupo += 8


'''
# listas de pastas

# diretório
path_dir = '/work/archive/Everson/Coqueiro/CENPES/DADOS/dados-raoni'

num_pastas = 13
dia_ini = 29
delay = 0

# loop atraves do numero de pastas e cria cada uma delas
for i in range (num_pastas):
    
    # define o nome da pasta com base no numero atual do loop
    nome_pasta = "{}062021_D-{}".format(dia_ini,delay)
    dia_ini -= 1
    delay += 1
    
    os.mkdir(os.path.join(path_dir, nome_pasta))

'''
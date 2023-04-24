#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:57:20 2023

@author: everson
"""

import os

# Defina o caminho para a pasta contendo os dados .nc
caminho_dados = "/home/everson/TRACK-1.5.0/indat"

# # Percorra todos os arquivos .nc na pasta e execute o comando bin/track.linux com o filtro especificado em specfiltT42.in
for arquivo in os.listdir(caminho_dados):
    sorted(arquivo)
    if arquivo.endswith(".nc"):
        nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
        comando = f"/home/everson/TRACK-1.5.0/bin/track.linux -i {arquivo} -f filt < /home/everson/TRACK-1.5.0/filtro_gfs.in"
        os.system(comando)
        caminho_origem = os.path.join("/home/everson/TRACK-1.5.0/outdat", "specfil.filt_band000")
        caminho_destino = os.path.join("/home/everson/TRACK-1.5.0/outdat", nome_arquivo_sem_extensao + ".dat")
        os.rename(caminho_origem, caminho_destino)
        caminho_origem = caminho_destino
        caminho_destino = os.path.join(caminho_dados, nome_arquivo_sem_extensao + ".dat")
        os.rename(caminho_origem, caminho_destino)
        
        
# Percorra todos os arquivos .dat na pasta indat e execute o comando ./master com as opções especificadas
for arquivo in os.listdir(caminho_dados):
    if arquivo.endswith(".dat"):
        nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
        comando = f"./master -c={nome_arquivo_sem_extensao} -d=now -e=track.linux -i={arquivo} -f=vo1991 -n=1,1000,1 -o=/home/everson/CENPES/tracks_rodadados_tr_passo_3/Extratropical -r=RUN_AT_ -s=RUNDATIN.VOR -j=RUN_AT.in"
        os.system(comando)

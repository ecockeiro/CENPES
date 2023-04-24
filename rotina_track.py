#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 11:57:20 2023

@author: everson
"""

import os

# Defina o caminho para a pasta contendo os dados .nc
caminho_dados = "/home/bjerknes/TRACK-1.5.0/indat"

# # Percorra todos os arquivos .nc na pasta e execute o comando bin/track.linux com o filtro especificado em specfiltT42.in
for arquivo in os.listdir(caminho_dados):
    sorted(arquivo)
    if arquivo.endswith(".nc"):
        nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
        comando = f"/home/bjerknes/TRACK-1.5.0/bin/track.linux -i {arquivo} -f filt < /home/bjerknes/TRACK-1.5.0/filtro_gfs.in"
        os.system(comando)
        
        caminho_origem = os.path.join("/home/bjerknes/TRACK-1.5.0/outdat", "specfil.filt_band000")
        caminho_destino = os.path.join("/home/bjerknes/TRACK-1.5.0/outdat", nome_arquivo_sem_extensao + ".dat")
        os.rename(caminho_origem, caminho_destino)
        
        caminho_origem = caminho_destino
        caminho_destino = os.path.join(caminho_dados, nome_arquivo_sem_extensao + ".dat")
        os.rename(caminho_origem, caminho_destino)
        
# Percorra todos os arquivos .dat na pasta indat e execute o comando ./master com as opções especificadas
for arquivo in os.listdir(caminho_dados):
    if arquivo.endswith(".dat"):
        nome_arquivo_sem_extensao = os.path.splitext(arquivo)[0]
        comando = f"./master -c={nome_arquivo_sem_extensao} -d=now -e=track.linux -i={arquivo} -f=vo1991 -n=1,1000,1 -o=/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Raoni/track_raoni/master_raoni_novo -r=RUN_AT_ -s=RUNDATIN.VOR -j=RUN_AT.in"
        os.system(comando)
        
   
 
# Definindo o caminho para a pasta onde estão os arquivos .gz
caminho_dados = "/media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Raoni/track_raoni/master_raoni_novo"

# Percorrer cada diretório e descompactar o arquivo tr_trs_neg.gz
for diretorio in os.listdir(caminho_dados):
    if os.path.isdir(os.path.join(caminho_dados, diretorio)):
        caminho_arquivo_gz = os.path.join(caminho_dados, diretorio, "tr_trs_neg.gz")
        if os.path.exists(caminho_arquivo_gz):
            comando = f"gunzip {caminho_arquivo_gz}"
            os.system(comando)
            
            dia = diretorio[:2]
            mes = diretorio[2:4]
            ano = diretorio[4:8]
            hora = '00'
            data = ano+mes+dia+hora
            
            caminho_arquivo_descompactado = os.path.join(caminho_dados, diretorio, "tr_trs_neg")
            comando = f"mv {caminho_arquivo_descompactado} /home/bjerknes/TRACK-1.5.0/utils/bin"
            os.system(comando)
            
            # Muda para o diretrotio /utils/bin/
            os.chdir('/home/bjerknes/TRACK-1.5.0/utils/bin/')    
            
            comando = f"./count tr_trs_neg 0 0 5 4 0 {data} 3"
            os.system(comando)
            
            comando = f"mv tr_trs_neg.new {diretorio}"
            os.system(comando)
            
            comando = f"tr2csv {diretorio}"
            os.system(comando)
            
            comando = f"mv alltr.csv  {diretorio}.csv"
            os.system(comando)
            
            comando = f"mv {diretorio}.csv /media/bjerknes/HD_todo_pod/Everson/Coqueiro/CENPES/DADOS/Raoni/track_raoni/Raoni_planilhas_csv/{diretorio}.csv"
            os.system(comando)
           
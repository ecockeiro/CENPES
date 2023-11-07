#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 09:56:11 2023

@author: bjerknes
"""

import pandas as pd
import glob
import numpy as np

era_5 = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/Yakecan/0_AnaGFS.csv')

planilhas = sorted(glob.glob('/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/Yakecan/*.csv'))

ciclones = ['Yakecan']
csv = pd.DataFrame({'Ciclones': ['Yakecan']})
legend_name = ['Dia 0', 'Dia - 1', 'Dia - 2', 'Dia - 3', 'Dia - 4', 'Dia - 5', 'Dia - 6']
variveis = ['pressao', 'vort', 'vento_mag']
# Lista para armazenar as estatísticas
estatisticas = []

for i, arq, in enumerate(planilhas[4:11]):
    plan = pd.read_csv(arq)
    
    # Calcular métricas para a comparação
    correlacao = era_5['pressao'].corr(plan['pressao'])
    amostras = len(plan['pressao'])
    bias = (era_5['pressao'] - plan['pressao']).mean()
    erro_medio = np.abs(era_5['pressao'] - plan['pressao']).mean()
    erro_medio_quadratico = np.sqrt(((era_5['pressao'] - plan['pressao']) ** 2).mean())
    
    # Calcular os resíduos
    residuos = era_5['pressao'] - plan['pressao']
    desvio_padrao_residuos = residuos.std()
    
    # Armazenar estatísticas em uma lista
    estatisticas.append({
        'Variável': f'{legend_name[i]} (Amostras:{amostras})',
        'Correlação': f'{correlacao:.2f}',
        'Bias': f'{bias:.2f}',
        'EM': f'{erro_medio:.2f}',
        'EMQ': f'{erro_medio_quadratico:.2f}',
        'Desvio Padrão dos Resíduos': f'{desvio_padrao_residuos:.2f}'
    })

# Criar um DataFrame a partir da lista de estatísticas
estatisticas_df = pd.DataFrame(estatisticas)

# Salvar as estatísticas em um arquivo CSV
estatisticas_df.to_csv('/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/estatisticas/Yakecan/pressao.csv', index=False)


import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt

# Carregar os dados do arquivo '0_AnaGFS.csv' como era_5
era_5 = pd.read_csv('/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/Yakecan/0_ERA5.csv')

# Lista de planilhas
planilhas = sorted(glob.glob('/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/planilhas_extraidas/Yakecan/*.csv'))

# Lista de nomes de ciclones
ciclones = ['Yakecan']

# DataFrame para armazenar os resultados
resultado = pd.DataFrame({'Ciclones': ['Yakecan']})

# Lista de nomes de dias de antecedência
legend_name = ['Dia 0', 'Dia - 1', 'Dia - 2', 'Dia - 3', 'Dia - 4', 'Dia - 5', 'Dia - 6']

# Lista de variáveis a serem analisadas
variaveis = ['pressao', 'vort', 'vento_mag']

# Loop sobre as variáveis
for var in variaveis:
    estatisticas = []  # Lista para armazenar as estatísticas para cada variável
    
    # Loop sobre os dias de antecedência
    for i, arq in enumerate(planilhas[4:11]):
        plan = pd.read_csv(arq)
        plan['vort'] = plan['vort']*10**5
        # Calcular métricas para a comparação
        correlacao = era_5[var].corr(plan[var])
        amostras = len(plan[var])
        bias = (era_5[var] - plan[var]).mean()
        erro_medio = np.abs(era_5[var] - plan[var]).mean()
        erro_medio_quadratico = np.sqrt(((era_5[var] - plan[var]) ** 2).mean())
        
        # Calcular os resíduos
        residuos = era_5[var] - plan[var]
        desvio_padrao_residuos = residuos.std()
        
        # Armazenar estatísticas em uma lista
        estatisticas.append({
            'Dia de Antecedência': legend_name[i],
            'Correlação': correlacao,
            'Bias': bias,
            'EM': erro_medio,
            'EMQ': erro_medio_quadratico,
            'Desvio Padrão dos Resíduos': desvio_padrao_residuos
        })
    
    # Criar um DataFrame a partir da lista de estatísticas
    estatisticas_df = pd.DataFrame(estatisticas)
    
    # Plotar o gráfico de linha
    plt.figure(figsize=(10, 6))
    for col in estatisticas_df.columns[1:]:
        plt.plot(estatisticas_df['Dia de Antecedência'], estatisticas_df[col], marker='o', label=col)
    plt.title(f'{var}')
    plt.xlabel('Dias de Antecedência')
    plt.ylabel('Valores de Estatísticas')
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))  # Coloque a legenda fora do gráfico
    plt.xticks(rotation=45)
    
    # Salvar o gráfico em um arquivo
    plt.savefig(f'/media/bjerknes/HD_todo_pod/Everson/Atmosmarine/OMARSAT/imagens/Yakecan/{var}_line.png', bbox_inches='tight')
    plt.close()  # Feche o gráfico para liberar memória

print("Gráficos de linha com legendas fora do gráfico salvos com sucesso.")


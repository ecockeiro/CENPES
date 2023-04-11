"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Created on Fri Nov 11 12:52:28 2022

@author: everson

Esse script serve para coverter as componentes U e V do GFS e converte-las em vorticidade
"""

from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units
import numpy as np
import xarray as xr
import os


# função que lê as pastas em um diretório
def get_folders(directory):
    return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

# diretório
directories = '/work/archive/Everson/Coqueiro/CENPES/DADOS/dados_input_raoni'

# lista de pasta para serem selecionadas
folders = get_folders(directories)
folders.sort(reverse=True)

# # dia com delay selecione de acordo com a ordem dos seus dados
delay = 0

# loop através de cada diretório e ler arquivos csv
for j in range(len(folders)):
    # path_name = str(directories) + '/' + str(folders[j])
    
    path_name = os.path.join(directories, folders[j])
    
    ## Abre os dados na pasta
    data = xr.open_mfdataset(f'{path_name}/*grib2.nc')
    data['u'] = data['U_GRD_L100'].copy()
    data['v'] = data['V_GRD_L100'].copy()
    
    Data = str(folders[j])
    
    # data = data.sel(level=850)
    
    # Vai preenchendo o np.array...
    vort_850= mpcalc.vorticity(data.u, data.v)
    
    
    #sys.exit()    
    # Cria o datarray dentro da estrutura do data 
    data['vo'] = data['u'].copy()
    data['vo'].data = vort_850
    data['vo'] = xr.DataArray(vort_850, dims = ['time','lat','lon'])   
    data['vo'].attrs['standard_name'] = 'atmosphere_relative_vorticity'
    data['vo'].attrs['long_name'] = 'Vorticity (relative)'
    data['vo'].attrs['units'] = 's**-1'
    data['lat'].attrs['units'] = 'degrees_north'
    data['lon'].attrs['units'] = 'degrees_east'
    
    
    # Deixa somente o vort_850 dentro do data
    data = data[['vo']]
    
    # Salva no arquivo netcdf
    fname = '/work/archive/Everson/Coqueiro/CENPES/DADOS/velocidade_convertidade_raoni/{(Data)}_D-{(delay)}.nc'
    data.to_netcdf(f'/work/archive/Everson/Coqueiro/CENPES/DADOS/velocidade_convertidade_raoni/{(Data)}_D-{(delay)}.nc')
    
    os.system("ncap2 -O -s 'time=double(time)' {} {}".format(fname,fname))

    delay +=1
    
    print ('finished saving')
    
    
    ## após criar o dado, dar o comando seguinte no terminal na pasta que salvou o dado para converter o reftime
    ##> ncap2 -O -s 'time=double(time)' D.nc D.nc
 

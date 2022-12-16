#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:52:28 2022

@author: ladsin
"""
from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units
import numpy as np
import xarray as xr
import sys

## Abre os dados na pasta
data = xr.open_mfdataset('/home/ladsin/Downloads/gfs_dados/*.grib2.nc4')

## Retira o nivel 1 individual do dado
data = data.sel(isobaric=85000).squeeze()

## Seleciona as latitudes e longitudes
lats = data.variables['latitude'][:].values
lons = data.variables['longitude'][:].values

# Criar um np.array de zeros
vort_850 = np.zeros([len(data['time']),len(data['latitude']),len(data['longitude'])])

for i in range(len(data['time'])):
    u_wind = units('m/s') * data['u-component_of_wind_isobaric'].isel(time=i).squeeze()
    v_wind = units('m/s') * data['v-component_of_wind_isobaric'].isel(time=i).squeeze()
    
    dx, dy =  mpcalc.lat_lon_grid_deltas(data['longitude'], data['latitude'])
        
    # Vai preenchendo o np.array...
    vort_850[i,:,:] = mpcalc.vorticity(u_wind, v_wind, dx=dx, dy=dy)*10**5


#sys.exit()    
# Cria o datarray dentro da estrutura do data 
data['vo'] = data['u-component_of_wind_isobaric'].copy()
data['vo'].data = vort_850
data['vo'] = xr.DataArray(vort_850, dims = ['time','latitude','longitude'])   
data['vo'].attrs['standard_name'] = 'atmosphere_relative_vorticity'
data['vo'].attrs['long_name'] = 'Vorticity (relative)'
data['vo'].attrs['units'] = 's**-1'
data['latitude'].attrs['units'] = 'degrees_north'
data['longitude'].attrs['units'] = 'degrees_east'


# Deixa somente o vort_850 dentro do data
data = data[['vo']]

# Salva no arquivo netcdf
data.to_netcdf('/work/archive/Everson/Coqueiro/CENPES/DADOS/dados_novos/D.nc')

print ('finished saving')


## após criar o dado, dar o comando seguinte no terminal na pasta que salvou o dado para converter o reftime
##> ncap2 -s 'time=double(time)' D.nc D_2.nc
 
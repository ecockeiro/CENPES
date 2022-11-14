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

data = xr.open_mfdataset('/home/everson/CENPES/Dados_netcdf/Previsões/D-12/*.grib2.nc')

#seleciona as fatias de lat e lon
lon_slice = slice(-180., 180.)
lat_slice = slice(0., -50.)

lats = data.variables['lat'][:].squeeze()
lons = data.variables['lon'][:].squeeze()

# Criar um np.array de zeros
vort_850 = np.zeros([len(data['time']),len(lats),len(lons)])

for i in range(len(data['time'])):
    u_wind = units('m/s') * data['U_GRD_L100'][i,:,:].squeeze()
    v_wind = units('m/s') * data['V_GRD_L100'][i,:,:].squeeze()
    
    dx, dy =  mpcalc.lat_lon_grid_deltas(lons, lats)
        
    # Vai preenchendo o np.array...
    vort_850[i,:,:] = mpcalc.vorticity(u_wind, v_wind, dx=dx, dy=dy)*10**5
    
# Cria o datarray dentro da estrutura do data 
data['vort_850'] = xr.DataArray(vort_850, dims = ['time','lat','lon'])   
data['vort_850'].attrs['name'] = 'vort_850'
data['vort_850'].attrs['long_name'] = 'Vorticidade 850 hPa'
data['vort_850'].attrs['units'] = '1/second'

# Deixa somente o vort_850 dentro do data
data = data[['vort_850']]

# Salva no arquivo netcdf
data.to_netcdf('/home/everson/CENPES/Dados_netcdf/Previsões/vorticidade_850/D-12.nc')

print ('finished saving')
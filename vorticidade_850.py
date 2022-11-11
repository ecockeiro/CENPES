#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:52:28 2022

@author: ladsin
"""
from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units
from netCDF4 import MFDataset
from netCDF4 import num2date
import numpy as np
import xarray as xr

data = MFDataset('/work/archive/Everson/Coqueiro/CENPES/DADOS/Dados netcdf/Previsões /D/*.grib2.nc')

#seleciona as fatias de lat e lon
lon_slice = slice(-180., 180.)
lat_slice = slice(0., -50.)

lats = data.variables['lat'][:].squeeze()
lons = data.variables['lon'][:].squeeze()

for i in range(len(data['time'])-1):
    u_wind = units('m/s') * data.variables['U_GRD_L100'][i,:,:].squeeze()
    v_wind = units('m/s') * data.variables['V_GRD_L100'][i,:,:].squeeze()
    
    dx, dy =  mpcalc.lat_lon_grid_deltas(lons, lats)
        
    vort_850 = mpcalc.vorticity(u_wind, v_wind, dx=dx, dy=dy, x_dim=- 1, y_dim=- 2)*10**5
    
    
# vort_850 = 'vort_850'
# vort_850.attrs['long_name'] = 'Vorticidade 850 hPa'
# vort_850.attrs['units'] = '1 / second'

# novo = './vort_850_72h.nc'

data.to_netcdf()
print ('finished saving')
    

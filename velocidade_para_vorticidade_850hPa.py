#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:52:28 2022

@author: ladsin
"""
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

# lista de diretórios a serem verificados
directories = '/work/archive/Everson/Coqueiro/CENPES/DADOS/dados_input'

# lista de anos para serem selecionados
dia = ['20220505', '20220506', '20220507', '20220508', '20220509', '20220510', '20220511', '20220512', '20220513', '20220514', '20220515', '20220516', '20220517', 'analise+previsão_all_17-20']
delay = 12

# loop através de cada diretório e ler arquivos csv
for j in range(len(dia)):
    path_name = str(directories) + '/' + str(dia[j])

    ## Abre os dados na pasta
    data = xr.open_mfdataset(f'{path_name}/*.grib2.nc')
    
    Data = str(dia[j])
    
    
    ## Seleciona as lats e lons
    lats = data.variables['lat'][:].values
    lons = data.variables['lon'][:].values
    
    # Criar um np.array de zeros
    vort_850 = np.zeros([len(data['time']),len(data['lat']),len(data['lon'])])
    
    for i in range(len(data['time'])):
        u_wind = units('m/s') * data['U_GRD_L100'].isel(time=i).squeeze()
        v_wind = units('m/s') * data['V_GRD_L100'].isel(time=i).squeeze()
        
        dx, dy =  mpcalc.lat_lon_grid_deltas(data['lon'], data['lat'])
            
        # Vai preenchendo o np.array...
        vort_850[i,:,:] = mpcalc.vorticity(u_wind, v_wind, dx=dx, dy=dy)*10**5
    
    
    #sys.exit()    
    # Cria o datarray dentro da estrutura do data 
    data['vo'] = data['U_GRD_L100'].copy()
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
    data.to_netcdf(f'/work/archive/Everson/Coqueiro/CENPES/DADOS/dados_novos/{(Data)}_D-{(delay)}.nc')
    
    delay -=1
    
    print ('finished saving')
    
    
    ## após criar o dado, dar o comando seguinte no terminal na pasta que salvou o dado para converter o reftime
    ##> ncap2 -s 'time=double(time)' D.nc D_2.nc
 

# -*- coding: utf-,8 -*-
"""
Spyder Editor
"""

import cdsapi

url = 'https://cds.climate.copernicus.eu/api/v2'
key = {my api-key}
verify = 0

def retriveERA5Data(yearStr,formatStr,fileName):
    c = cdsapi.Client()
    
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': formatStr,
            'variable': [
                '10m_u_component_of_wind', '10m_v_component_of_wind',
            ],
            'year': yearStr,
            'pressure_level': '1000',
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'area': [ 50, -45, 15,  0, ],
        },
        fileName)


listYear = [ 1959, 1960,]
    

# THE CODE STARTS HERE:
for i in listYear:
    fileName='download_'+str(i)+'.nc'
    #print (i,"-",fileName)
    retriveERA5Data(i,'netcdf',fileName)

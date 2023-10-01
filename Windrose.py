# -*- coding: utf-8 -*-
"""
Created on Sun Oct 01 10:06:17 2023

@author: Paulo
"""

import numpy as np
from netCDF4 import Dataset
import math

def readNetCDF(file):
    '''
    Description
    -----------
        Function to create an object of type dataset (netCDF object)
        Parameters
    ----------
    file : string
        String with the file name or the path
    Returns
    -------
    ds : object from class netCDF4._netCDF4.Dataset 
        Returns the dataset object
    '''
    ds = Dataset(file, 'r')
    return ds


def getDirInt(val_U,val_V):
    '''
    Description
    ------------
        Function to compute the direction and intensity
        of wind from U and V vector components 

    Parameters
    ----------
    val_U : float
        Value of U vector component of Wind at 10 meters.
    val_V : float
        Value of V vector component of Wind at 10 meters.

    Returns
    -------
    direction : float
        Angle in degrees from 0 to 360 of the wind vetor at 10 meters.
    intensity : float
        Intensity of wind at 10 meters (units: m.s**-1).
    intensityKTS : float
        Intensity of wind at 10 meters (units: knots or nautical miles per hour).
    '''
    if val_U==-32767 or val_V==-32767:
        return 0,0,0
    else:
        intensity=math.sqrt((val_U**2)+(val_V**2))
        intensityKTS=(intensity*3600)/1852
        angleRad=math.atan2(val_U,val_V)
        if val_U>=0 and val_V>=0:
            angleDir=angleRad
        elif val_U<=0 and val_V>=0:
            angleDir=(2*math.pi)+angleRad
        elif val_U>=0 and val_V<=0:
            angleDir=angleRad
        elif val_U<=0 and val_V<=0:
            angleDir=(2*math.pi)+angleRad
    direction=math.degrees(angleDir)
    return direction,intensity,intensityKTS


def functPlotWindrose(vectorDir,vectorInt,posLat,posLon):
    '''
    Description
    ------------
        Function to compute the direction and intensity
        of wind from U and V vector components 
    Parameters
    ----------
    vectorDir : list
        list of values with wind direction (float).
    vectorInt : list
        list of values with wind speed (float).
    posLat : float
        value of the latitude of point (is used if you want write the lat lon in windrose legend).
    posLon : float
        value of the latitude of point (is used if you want write the lat lon in windrose legend).

    Returns
    -------
    None.

    '''
    from windrose import WindroseAxes
    from matplotlib import cm
    ax = WindroseAxes.from_ax()
    ax.box(vectorDir, vectorInt, normed=True, bins=np.arange(0,16,1),cmap=cm.gist_rainbow)
    ax.set_legend().set_title("Wind Speed (m/s)") #coloca a legenda completa
    fig = ax.get_figure()
    nameFile='windrose_1960_figure.svg'
    fig.savefig(nameFile)



def computeWindVectors(file,lat,lon):
    '''
    Description
    ------------
        Function to open a ERA5 model NetCDF file with the U and V vector components
        of wind at 10 meters, compute the direction and intensity of wind for a specific
        point (lat,lon) and output two lists, one with the wind direction values and another
        with wind speed.     

    Parameters
    ----------
    file : string
        NetCDF file name or path.
    lat : float
        latitude of the point for where the user wants compute the wind direction
        and wind speed.
    lon : float
        longitude of the point for where the user wants compute the wind direction
        and wind speed.
        
    Returns
    -------
    wd : string
        list with all wind direction values.
    ws : list
        list with all wind speed values.

    '''
    # read the netCDF file and get an netCDF4 dataset object
    f=readNetCDF(file)
    lats = f.variables['latitude'][:] 
    lons = f.variables['longitude'][:]
    time = f.variables['time'][:]
    u10 = f.variables['u10'][:]
    v10 = f.variables['v10'][:]
    # this is to get the vector index corresponding to the specific lat and lon
    lat_ind = np.where(lats == lat)
    lon_ind = np.where(lons == lon)
    wd = []
    ws = []
    
    # for loop to get wind direction and intensity for all hours in the position defined by user
    for i in range(len(time)):
        direction,intensity,intensityKTS = getDirInt(u10[i,lat_ind,lon_ind],v10[i,lat_ind,lon_ind])
        # this if block is to invert the direction because normally the
        # windrose show the direction from where wind blows
        if direction <=180:
            direction = direction + 180
        else:
            direction = direction - 180
        wd.append(direction)
        ws.append(intensity)
    f.close()
    return wd,ws


file='download_1960.nc'
posLat=38.75
posLon=-9.50
wd,ws=computeWindVectors(file,posLat,posLon)
functPlotWindrose(wd,ws,posLat,posLon)


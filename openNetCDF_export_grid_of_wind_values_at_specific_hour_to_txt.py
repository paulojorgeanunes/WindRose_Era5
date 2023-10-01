# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:53:28 2022


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

def hoursFromRef(strTimeStamp):
    '''
    Description
    ------------
        This function computes the number of hours from a date and time
        since one datetime reference.
        The reference is: '1/01/1900 00:00:00.000000' --> time origin of ERA 5 model 
        NetCDF time variable. 

    Parameters
    ----------
    strTimeStamp : string
        String with the date and time when the user wants compute the grid
        example: '1/01/1960 02:00:00.000000'.

    Returns
    -------
    year : integer
        The year of a datetime object.
    hoursDiff : integer
        The number of hours between a datetime and a reference datetime.
    '''
    import datetime as dt
    start='1/01/1900 00:00:00.000000'
    end = '1/01/1960 02:00:00.000000' 
    # this is the string format for datetime inputs
    date_format_str = '%d/%m/%Y %H:%M:%S.%f'
    startT = dt.datetime.strptime(start, date_format_str)
    endT =   dt.datetime.strptime(end, date_format_str)
    difference = endT - startT
    # get the year of prediction
    year=endT.year
    hoursDiff=int(difference.total_seconds()/3600)
    return year,hoursDiff


def exportToTxtFile(strTimeStamp):
    '''
    Description
    ------------
        Function to open a ERA5 model NetCDF file with the U and V vector components
        of wind at 10 meters, compute the direction and intensity of wind and export
        the result for a plain text file.     

    Parameters
    ----------
    strTimeStamp : string
        String with the date and time when the user wants compute the grid
        example: '1/01/1960 02:00:00.000000'.

    Returns
    -------
    None.

    '''
    # get the number of hours from the ERA5 time variable origin reference
    year,hoursDiff=hoursFromRef(strTimeStamp)
    path = "file_wind_grid.txt" #Path or File name to output data
    fileToExport=open(path,'w')
    # print a file header line
    str2Print='Latitude,Longitude,direction,intensity,intensityKts\n'
    fileToExport.write(str2Print)
    fileInPath='download_'+str(year)+'.nc'
    # read the netCDF file and get an netCDF4 dataset object
    f=readNetCDF(fileInPath)
    lats = f.variables['latitude'][:] 
    lons = f.variables['longitude'][:]
    time = f.variables['time'][:]
    u10 = f.variables['u10'][:]
    v10 = f.variables['v10'][:]
    # Time variable is reference in hours, this 
    time_ind = np.where(time == hoursDiff)
    # for loop to get wind direction and intensity in all points (regular grid)
    for i in range(len(lats)):
        for k in range(len(lons)):
            direction,intensity,intensityKTS = getDirInt(u10[time_ind,i,k],v10[time_ind,i,k])
            str2Print=str(lats[i])+';'+str(lons[k])+';'+str(direction)+ ';'+str(intensity)+ ';'+str(intensityKTS)+'\n'  
            fileToExport.write(str2Print)            
    f.close()
    fileToExport.close()

# ------- the main program starts here -------       
strTimeStamp='1/01/1960 02:00:00.000000' 
exportToTxtFile(strTimeStamp)

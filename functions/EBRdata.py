import urllib.request
from datetime import date
import pandas as pd
import numpy as np
import astral.sun as AS
from astral import LocationInfo


def read_file(year, month, day):

    """
    Given a date (year, month, day), get its geomagnetic data
    from OE web and read it taking into account OE's file formats.
    Missing data will be added. OUTPUT: pandas dataframe

     >> Files from 2011 and before have an introduction
        of 12 lines to be skipped. Have: EBRH,EBRZ,EBRF
                                   To be added: EBRX,EBRY

     >> Files between 2011 and 2017 (not included) generally have
        an introduction of 26 lines to be skipped. Have: EBRX,EBRY,EBRZ,EBRF
                                                   To be added: EBRH
          - Files from 2012 must skip 27 lines
          - 21-06-2015 special case with 34 lines to be skipped

     >> Files from 2017 and after generally have an introduction
        of 26 lines to be skipped. Have: EBRX,EBRY,EBRZ
                                   To be added: EBRF
    """

    # Adapt url to desired date

    year = str(year)
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_name = month_list[int(month)-1]

    url = (
        f'http://www.obsebre.es/php/geomagnetisme/dhorta/{year}/' +
        f'{month_name}/ebr{year}{month}{day}dmin.min'
        )
    # hdr required to access the files
    hdr = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome' +
            '/84.0.4147.105 Safari/537.36',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    req = urllib.request.Request(url, headers=hdr)
    file = urllib.request.urlopen(req)


    # Read requested file according to its format and compute
    # the missing variables

    if 2011 < float(year) <2017:
        if (year == '2015' and month == '06' and day == '21'):
            intro = 34
        elif year == '2012':
            intro = 27
        else:
            intro = 26
        data = pd.read_csv(file, skiprows=intro, delimiter='\\s+')
        #Horitzontal module EBRF is missing
        data['EBRH'] = np.sqrt(data['EBRX']**2+data['EBRY']**2)

    elif float(year) >= 2017:
        data = pd.read_csv(file, skiprows=26, delimiter='\\s+')
        #Total module EBRF is missing
        data['EBRF'] = np.sqrt(data['EBRX']**2+data['EBRY']**2+data['EBRZ']**2)

    else:
        data = pd.read_csv(file, skiprows=12, delimiter='\\s+')
        #X and Y components are missing
        data['EBRX'] = data['EBRH']*np.cos(np.radians(data['EBRD']/60))
        data['EBRY'] = data['EBRH']*np.sin(np.radians(data['EBRD']/60))

    return data


def day_times(year, month, day):
    """
    Given a date (year, month, day), get the corresponding sunrise
    time, noon time and sunset time. Matrix also contains the matching
    day minute, useful for time series with minute interval starting at 00:00.

    OUTPUT: [[sunrise datetime, sunrise day minute],
             [  noon datetime ,  noon day minute  ],
             [ sunset datetime, sunset day minute ]]
    """

    studied_day = date(year, month, day)
                                                    # Latitude, Longitude
    city = LocationInfo("EBR", "Catalunya", "Europe", 40.820817, 0.495186)

    daylight = AS.daylight(city.observer, studied_day)
    noon = AS.noon(city.observer, studied_day)

    sunrise_index = (daylight[0].hour)*60 + daylight[0].minute
    noon_index = (noon.hour)*60 + noon.minute
    sunset_index = (daylight[1].hour)*60 + daylight[1].minute

    rise_noon_set_indexes = [[daylight[0], sunrise_index],
                             [noon, noon_index],
                             [daylight[1], sunset_index]]

    return rise_noon_set_indexes

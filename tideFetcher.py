# #############################################
# tideFetcher.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

import urllib.request
import json

# Returns a dictionary containing the high and low tides for
# three days starting with the date provided 
# The station parameter is the NOAA tide station number
# Data is fetched from the NOAA CO-OPS tide API
def getTides(startDate, station):
    urlString = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?" \
        "begin_date=" + startDate + "" \
        "&range=72" \
        "&station=" + station + "" \
        "&product=predictions&datum=mllw&units=english&time_zone=gmt" \
        "&application=ted_falasco&format=json&interval=hilo"
    
    tideData = urllib.request.urlopen(urlString)
    tidesDict = json.load(tideData)

    return tidesDict
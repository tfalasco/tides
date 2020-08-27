# #############################################
# tides.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

from datetime import datetime, timedelta
from dateutil import tz

# from tidePlotter import TurtlePlotter
from tidePlotter import MatPlotPlotter
import tideFetcher

seconds_per_day = 86400
seconds_per_minute = 60

def main():
    print("Tides")

    # Create a MatPlotPlotter
    m = MatPlotPlotter()

    # Grab the current datetime in UTC and find yesterday's date
    utc_now = datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=tz.tzutc())
    local_now = utc_now.astimezone(tz.tzlocal())
    yesterday = utc_now - timedelta(days=1)

    # Fetch three days of tide hi-lo information from NOAA's CO-OPS API
    tides = tideFetcher.getTides(yesterday.strftime("%Y%m%d"), "8661070")

    # Plot the tides
    # Each tide segment should be scaled in the x-axis for time and in
    # the y-axis for relative tide height.
    if len(tides) > 0:

        for i in range(len(tides['predictions']) - 1):
            # Get the current and next tide heights
            start_tide_height = float(tides['predictions'][i]['v'])
            end_tide_height = float(tides['predictions'][i + 1]['v'])

            # Get the current and next tide times
            start_tide_datetime = datetime.fromisoformat(tides['predictions'][i]['t'])
            end_tide_datetime = datetime.fromisoformat(tides['predictions'][i + 1]['t'])

            # Offset tide times to get local time
            start_tide_datetime = start_tide_datetime.replace(tzinfo=tz.tzutc())
            start_tide_local_datetime = start_tide_datetime.astimezone(tz.tzlocal())
            end_tide_datetime = end_tide_datetime.replace(tzinfo=tz.tzutc())
            end_tide_local_datetime = end_tide_datetime.astimezone(tz.tzlocal())

            # Calculate the x and y values for the current tide segment
            m.calculateTideSegment(start_tide_height, end_tide_height, start_tide_local_datetime, end_tide_local_datetime)            

    # Plot a line indicating the current datetime
    m.calculateNowLine(local_now)
    
    # Show the plot
    m.displayPlot()

if __name__ == '__main__':
    main()

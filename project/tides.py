# #############################################
# tideFetcher.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

import turtle
from datetime import datetime, timedelta

import tidePlotter
import tideFetcher

def main():
    print("Tides")

    # Create a turtle for plotting
    t = turtle.Turtle()
    t.hideturtle()

    # Grab the current datetime in UTC and find yesterday's date
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    # Fetch three days of tide hi-lo information from NOAA's CO-OPS API
    tides = tideFetcher.getTides(yesterday.strftime("%Y%m%d"), "8661070")

    # Plot the axes
    tidePlotter.plotAxes(t)

    # Plot the tides
    # Each tide segment should be scaled in the x-axis for time and in
    # the y-axis for relative tide height.
    if len(tides) > 0:

        for i in range(len(tides['predictions']) - 1):
            # Get the current and next tide heights
            startTide = float(tides['predictions'][i]['v'])
            endTide = float(tides['predictions'][i + 1]['v'])

            # Calculate the minutes between tides
            startTideDateTime = datetime.fromisoformat(tides['predictions'][i]['t'])
            endTideDateTime = datetime.fromisoformat(tides['predictions'][i + 1]['t'])
            tideMinutes = (((endTideDateTime - startTideDateTime).days * 86400) + ((endTideDateTime - startTideDateTime).seconds)) // 60

            # Calculate the x offset
            xOffset = (((startTideDateTime - now).days * 86400) + ((startTideDateTime - now).seconds)) // 60

            # Plot the current tide segment
            tidePlotter.plotTideSegment(t, startTide, endTide, tideMinutes, xOffset)            

    # Plot a line indicating the current datetime
    xOffset = (now.hour * 60) + now.minute
    tidePlotter.plotNowLine(t, xOffset)

    turtle.done()


if __name__ == '__main__':
    main()

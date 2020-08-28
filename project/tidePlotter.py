# #############################################
# tidePlotter.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import numpy
import turtle
import math
from datetime import datetime, timedelta
from dateutil import tz

class MatPlotPlotter:
    def __init__(self):

        # The figure and axes for this plotter
        self.fig, self.ax = plt.subplots(figsize=[10.0, 8.0])

        # Adjust this value to change the choppiness/smoothness of
        # the plotted tide curve.
        # This is used to plot both the tides and the now-line
        self.curvePrecision = 20

        # Create an empty list for all x values
        self.all_x_values = []

        # Create an empty list for all y values
        self.all_y_values = []

        # Create an empty list for the now x values
        self.now_x_values = []

        # Create an empty list for the now y values
        self.now_y_values = []
    

    # Calculates the x and y values of the tide segment
    # Does a cosine interpolation between startTide and endTide to smooth the curve
    # Scales the x-axis based on the number of minutes between  startTide and endTide
    def calculateTideSegment(self, start_tide_height, end_tide_height, start_tide_datetime, end_tide_datetime):
        # Adjust timezone info to prevent auto-correcting local time to UTC
        start_tide_datetime = start_tide_datetime.replace(tzinfo=tz.tzutc())
        end_tide_datetime = end_tide_datetime.replace(tzinfo=tz.tzutc())

        # Prepare raw x and y value arrays
        x_values = numpy.arange(start_tide_datetime, end_tide_datetime, (end_tide_datetime - start_tide_datetime) / self.curvePrecision)
        zero_to_pi = numpy.arange(0, math.pi, math.pi / self.curvePrecision)
        y_values = numpy.cos(zero_to_pi)

        # Scale and offset the y-axis
        y_scale = (start_tide_height - end_tide_height) / 2
        y_offset = (start_tide_height + end_tide_height) / 2
        y_values = (y_values * y_scale) + y_offset
        
        # Accumulate x and y values
        for x in x_values:
            self.all_x_values.append(x)
        for y in y_values:
            self.all_y_values.append(y)
    
    def calculateNowLine(self, now_datetime):
        # Adjust timezone info to prevent auto-correcting local time to UTC
        now_datetime = now_datetime.replace(tzinfo=tz.tzutc())

        # Find min and max y values
        min_y = self.all_y_values[0]
        max_y = self.all_y_values[0]

        for y in self.all_y_values:
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        # Create two points to plot the now line
        self.now_x_values.append(now_datetime)
        self.now_y_values.append(min_y)

        self.now_x_values.append(now_datetime)
        self.now_y_values.append(max_y)


    def displayPlot(self, now_datetime):
        # Adjust timezone info to prevent auto-correcting local time to UTC
        now_datetime = now_datetime.replace(tzinfo=tz.tzutc())        

        # Limit x-axis to +/- 12 hours from now
        x_min = now_datetime - timedelta(hours = 11, minutes = now_datetime.minute)
        x_max = now_datetime + timedelta(hours = 12, minutes = 60 - now_datetime.minute)
        self.ax.set_xlim(x_min, x_max)

        # Plot the x and y values           
        self.ax.plot_date(self.all_x_values, self.all_y_values, 'b-', 'America/New York')
        self.ax.plot_date(self.now_x_values, self.now_y_values, 'r-', 'America/New York')

        # Configure gridlines
        xticks = numpy.arange(x_min, x_max, (x_max - x_min) / 4)
        self.ax.set_xticks(xticks)
        plt.grid(b = True, which = 'major', axis = 'both', color='grey')
        plt.minorticks_on()
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(4))
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(6))
        plt.grid(b = True, which = 'minor', axis = 'both', color='lightsteelblue')
        
        # Configure axis labels        
        self.ax.set_ylabel('Tide Height (ft)')       
        self.ax.set_xlabel('Time (24-hour)') 

        # Configure x-axis labels  
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H')) 
        self.ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))

        # Show the axes
        plt.show()

class TurtlePlotter:
    def __init__(self):
        # Instantiate a turtle for plotting and hide the turtle
        self.theTurtle = turtle.Turtle()
        self.theTurtle.hideturtle()

        # Adjust this value to change how "wide" the tides plot is
        # This is used to plot both the tides and the now-line
        self.xScaleFactor = 7.5

        # Adjust this value to change how "tall" the tides plot is
        # This is used to plot both the tides and the y-axis ticks
        self.yScale = 50

        # Adjust this value to change the choppiness/smoothness of
        # the plotted tide curve.
        # This is used to plot both the tides and the now-line
        self.curvePrecision = 20

    def __del__(self):
        # Keep the screen open
        turtle.done()

    # Plots the tide segment
    # Does a cosine interpolation between startTide and endTide to smooth the curve
    # Scales the x-axis based on the number of minutes between  startTide and endTide
    def plotTideSegment(self, startTide, endTide, segmentMinutes, xOffset):

        # Calculate the scale and offset for the x-axis
        xScale = segmentMinutes / self.xScaleFactor
        xOffset = (xOffset * math.pi) / self.xScaleFactor

        # The curved cosine interpolation line is composed of a number of straight lines
        # The choppiness/smoothness of the end result is dependent on curvePrecision
        for line in range (self.curvePrecision + 1):
            
            # Do the cosine interpolation for the y-axis value
            x = line * (math.pi / self.curvePrecision)
            y = ((math.cos(x) * ((startTide - endTide) / 2)) + ((startTide + endTide) / 2))

            # Scale and offset the x-axis and y-axis values
            x = (x * xScale) + xOffset
            y = y * self.yScale

            # Move to the starting point without drawing a line
            # Only draw a line if within the range of the plotted area
            if line == 0:
                self.theTurtle.penup()
            elif (x > -400) and (x < 400):
                self.theTurtle.pensize(5)
                self.theTurtle.pencolor("Blue")
                self.theTurtle.pendown()
            else:
                self.theTurtle.penup()

            # Plot the line
            self.theTurtle.goto(x, y)

    # Plots the x- and y-axes
    def plotAxes(self):

        # Plot the main axes
        self.theTurtle.penup()
        self.theTurtle.goto(-400, 350)

        self.theTurtle.pensize(3)
        self.theTurtle.pencolor("Black")
        self.theTurtle.pendown()
        self.theTurtle.goto(-400, -350)
        self.theTurtle.goto(-400, 0)
        self.theTurtle.goto(400, 0)

        # Plot the y-axis tick marks
        self.theTurtle.pensize(1)
        self.theTurtle.pencolor("Grey")

        for y in range(-350, 351, self.yScale):
            if y != 0:
                self.theTurtle.penup()
                self.theTurtle.goto(-400, y)

                self.theTurtle.pendown()
                self.theTurtle.goto(400, y)

    # Plots a line indicating the current datetime
    def plotNowLine(self, xOffset):

        xOffset = ((xOffset * math.pi) / self.xScaleFactor) / self.curvePrecision

        self.theTurtle.penup()
        self.theTurtle.goto(0, -350)

        self.theTurtle.pensize(3)
        self.theTurtle.pencolor("Red")

        self.theTurtle.pendown()
        self.theTurtle.goto(0, 350)
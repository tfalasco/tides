# #############################################
# tidePlotter.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

import turtle
import math

# Adjust this value to change how "wide" the tides plot is
# This is used to plot both the tides and the now-line
xScaleFactor = 7.5

# Adjust this value to change how "tall" the tides plot is
# This is used to plot both the tides and the y-axis ticks
yScale = 50

# Adjust this value to change the choppiness/smoothness of
# the plotted tide curve.
# This is used to plot both the tides and the now-line
curvePrecision = 20

# Plots the tide segment
# Does a cosine interpolation between startTide and endTide to smooth the curve
# Scales the y-axis based on the number of minutes between  startTide and endTide
def plotTideSegment(theTurtle, startTide, endTide, segmentMinutes, xOffset):

    # Calculate the scale and offset for the x-axis
    xScale = segmentMinutes / xScaleFactor
    xOffset = (xOffset * math.pi) / xScaleFactor

    # The curved cosine interpolation line is composed of a number of straight lines
    # The choppiness/smoothness of the end result is dependent on curvePrecision
    for line in range (curvePrecision + 1):
        
        # Do the cosine interpolation for the y-axis value
        x = line * (math.pi / curvePrecision)
        y = ((math.cos(x) * ((startTide - endTide) / 2)) + ((startTide + endTide) / 2))

        # Scale and offset the x-axis and y-axis values
        x = (x * xScale) + xOffset
        y = y * yScale

        # Move to the starting point without drawing a line
        # Only draw a line if within the range of the plotted area
        if line == 0:
            theTurtle.penup()
        elif (x > -400) and (x < 400):
            theTurtle.pensize(5)
            theTurtle.pencolor("Blue")
            theTurtle.pendown()
        else:
            theTurtle.penup()

        # Plot the line
        theTurtle.goto(x, y)

# Plots the x- and y-axes
def plotAxes(theTurtle):

    # Plot the main axes
    theTurtle.penup()
    theTurtle.goto(-400, 350)

    theTurtle.pensize(3)
    theTurtle.pencolor("Black")
    theTurtle.pendown()
    theTurtle.goto(-400, -350)
    theTurtle.goto(-400, 0)
    theTurtle.goto(400, 0)

    # Plot the y-axis tick marks
    theTurtle.pensize(1)
    theTurtle.pencolor("Grey")

    for y in range(-350, 351, yScale):
        if y != 0:
            theTurtle.penup()
            theTurtle.goto(-400, y)

            theTurtle.pendown()
            theTurtle.goto(400, y)

# Plots a line indicating the current datetime
def plotNowLine(theTurtle, xOffset):

    xOffset = ((xOffset * math.pi) / xScaleFactor) / curvePrecision

    theTurtle.penup()
    theTurtle.goto(0, -350)

    theTurtle.pensize(3)
    theTurtle.pencolor("Red")

    theTurtle.pendown()
    theTurtle.goto(0, 350)
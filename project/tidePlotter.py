# #############################################
# tidePlotter.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

import turtle
import math

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
    # Scales the y-axis based on the number of minutes between  startTide and endTide
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
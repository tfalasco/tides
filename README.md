# tides

## Overview
This project aims to display the current tide conditions, along with some recent and future tides, in an easy to understand visual layout.  The main idea of the layout is a sinusoidal curve that shows tide heights (MLLW) for high and low tide and is scaled for time along the x-axis.  There should be an indicator which shows where on the curve the current time falls.

![Example visual layout](images/visual-layout-example.png?raw=true "Example visual layout")

## Project Goals
### Graphics
One goal of this project is to learn about graphics in Python.  The first pass used Turtle for the graphics and improving the graphical performance was left for a future enhancement.  The current iteration now uses matplotlib to plot the tides and the performance improved drastically over using Turtle.

### API Access
Another goal of this project is to work with the NOAA CO-OPS API to request and deal with tide data.  Proper API usage is an important part of integrating with external systems and this project presents an opportunity to practice just that.

### Smoothing Algorithms
Lastly, this project was born from me wondering how to create a smooth-line transition between data points such as high and low tide.  Research into that topic revealed a fairly easy-to-implement smoothing algorithm called cosine interpolation, which works particularly well for alternating high/low data points, such as tide heights.

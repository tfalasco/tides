# #############################################
# tides.py
#
# Author: Ted Falasco
# Date created: 8/18/2020
#
# #############################################

import tkinter 
from tkinter import ttk
from datetime import datetime, timedelta
from dateutil import tz

from tidePlotter import MatPlotPlotter
import tideFetcher

def plot_button_pressed(m, parent_widget, station):
    # Grab the current datetime in UTC and find yesterday's date
    utc_now = datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=tz.tzutc())
    local_now = utc_now.astimezone(tz.tzlocal())
    yesterday = utc_now - timedelta(days=1)

    # Fetch three days of tide hi-lo information from NOAA's CO-OPS API
    tides = tideFetcher.getTides(yesterday.strftime("%Y%m%d"), station)

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
    m.displayPlot(parent_widget, local_now)

def quit(root):
    root.quit()
    root.destroy()

def main():
    # Create a MatPlotPlotter
    m = MatPlotPlotter()
    
    # Set up the main window and frame
    root = tkinter.Tk()
    root.title("Tides")
    root.geometry("1010x839")
    main_frame = ttk.Frame(root, padding="3 3 12 12")
    main_frame.grid(column = 0, row = 0, sticky = (tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    root.columnconfigure(0, weight = 1)
    root.rowconfigure(0, weight = 1)

    # Set up the graph frame
    graph_frame = ttk.Frame(main_frame, padding = "2 2 2 2")
    graph_frame.grid(column = 0, row = 1, columnspan = 3, sticky = (tkinter.N, tkinter.W, tkinter.E, tkinter.S))

    # Set up the user-entry frame
    station_id = tkinter.StringVar()
    entry_frame = ttk.Frame(main_frame, padding = "2 2 2 2")
    entry_frame.grid(column = 0, row = 0, sticky = (tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    ttk.Label(entry_frame, text = "Station ID:").grid(column = 0, row = 0, sticky = tkinter.W)
    station_entry = ttk.Entry(entry_frame, textvariable = station_id)
    station_entry.grid(column = 1, row = 0, sticky = tkinter.W)
    # TODO: Remove this hard-coded station ID
    station_entry.delete(0, tkinter.END)
    station_entry.insert(0, "8661070")
    station_id.set("8661070")
    ttk.Button(entry_frame, text = "Get Tides", command = lambda: plot_button_pressed(m, graph_frame, station_id.get())).grid(column = 2, row = 0, sticky = tkinter.E)

    root.protocol("WM_DELETE_WINDOW", lambda: quit(root))
    root.mainloop()
    
if __name__ == '__main__':
    main()

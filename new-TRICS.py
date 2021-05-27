# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, asksaveasfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
input_csv = askopenfilename(title="Select downloaded TRICS csv file", filetypes=[("csv files", "*.csv")]) # show an "Open" dialog box and return the path to the selected file
print(input_csv)


trip_rates = pd.read_csv(input_csv, names = ['time_range',
                                       'arrival_days',
                                       'arrival_GFA',
                                       'arrival_trip_rate',
                                       'departure_days',
                                       'departure_GFA',
                                       'departure_trip_rate',
                                       'total_days',
                                       'total_GFA',
                                       'total_trip_rate'])

#clean data based on the time_range column
#remove blank rows
trip_rates = trip_rates[pd.notnull(trip_rates['time_range'])]

#convert time_range column to string
trip_rates['time_range'] = trip_rates['time_range'].apply(str)

#replace blank strings with na
trip_rates = trip_rates.replace(r'^\s*$', np.NaN, regex=True)

#remove header rows starting with values in searchfor list
search_strings = ['TRIP RATE', 'Calculation Factor','Time Range', 'Daily Trip Rates:']
trip_rates = trip_rates[~trip_rates.time_range.str.contains('|'.join(search_strings))]


#create a new column containing count type values
trip_rates['count_type'] = np.where(trip_rates.time_range.str.startswith('Count Type:', na = False), trip_rates.time_range,np.nan)


#remove the 'Count Type: ' prefix from the new column
trip_rates['count_type'] = trip_rates['count_type'].str.split(': ').str[-1]


#fill down count values
trip_rates['count_type'] = trip_rates['count_type'].ffill()


#The data tables start after the count type definitions, for example 'Count Type: TAXIS'
#remove rows before the first count type occurance
trip_rates = trip_rates[(trip_rates.time_range.str.startswith('Count Type:', na = False)).idxmax():]

#remove rows where time_range starts with 'Count Type: '
trip_rates = trip_rates[~trip_rates.time_range.str.contains('Count Type:')]


#reset index
trip_rates = trip_rates.reset_index(drop=True)

#export to csv
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
output_csv = asksaveasfilename(title="Choose where to save trip rate csv", defaultextension=".csv", filetypes=(("csv file", "*.csv"),)) # show an "Open" dialog box and return the path to the selected file
print(output_csv)

print("Exporting to "+output_csv)
trip_rates.to_csv(output_csv, index=False)
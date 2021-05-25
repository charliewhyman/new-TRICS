# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
df = pd.read_csv('TRICS.CSV', names = ['time_range',
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
df = df[pd.notnull(df['time_range'])]

#convert time_range column to string
df['time_range'] = df['time_range'].apply(str)

#replace blank strings with na
df = df.replace(r'^\s*$', np.NaN, regex=True)

#remove header rows starting with values in searchfor list
search_strings = ['TRIP RATE', 'Calculation Factor','Time Range', 'Daily Trip Rates:']
df = df[~df.time_range.str.contains('|'.join(search_strings))]


#create a new column containing count type values
df['count_type'] = np.where(df.time_range.str.startswith('Count Type:', na = False), df.time_range,np.nan)


#remove the 'Count Type: ' prefix from the new column
df['count_type'] = df['count_type'].str.split(': ').str[-1]


#fill down count values
df['count_type'] = df['count_type'].ffill()


#The data tables start after the count type definitions, for example 'Count Type: TAXIS'
#remove rows before the first count type occurance
df = df[(df.time_range.str.startswith('Count Type:', na = False)).idxmax():]

#remove rows where time_range starts with 'Count Type: '
df = df[~df.time_range.str.contains('Count Type:')]


#reset index
df = df.reset_index(drop=True)

#export to csv
df.to_csv('TRICS_export.csv')
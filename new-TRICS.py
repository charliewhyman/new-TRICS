# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
import numpy as np
trip_rates = pd.read_csv('TRICS.CSV', names = ['time_range',
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
trip_rates.to_csv('trip_rates.csv', index=False)
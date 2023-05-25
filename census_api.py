# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:08:33 2023

@author: imper
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import geopandas as gpd


#%% IMPORTING DATA FROM API AND FORMATING

# Set variable api to the American Community Survey 5-Year API endpoint for 2018 as shown below:
api = 'http://api.census.gov/data/2020/acs/acs5'

for_clause = 'place:*' # indicates what kind of geo unit should be returned
#county
#school district (unified)
#place
in_clause = 'state:36'
key_value = '98f45bb20730399804c81c734eb32ca2b92dd188' # census API key

payload = {
    'get':"NAME,B20002_001E,B01003_001E,B20003_001E,B02001_001E,B02001_002E,B20004_008E,B20004_009E"
    'for':for_clause,
    'in':in_clause,
    'key':key_value
    }

# The call will build an HTTPS query string, send it to the API endpoint, and collect the response
response = requests.get(api, payload)

if response.status_code == 200:
    print('\nAPI Success')
else:
    print('\nAPI Failure',response.status_code)
    print(response.text)
    assert False # stops script if statement is reached

# Formattting data received from API
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]

earnings = pd.DataFrame(columns = colnames, data = datarows)

# Formatting earnings
## need to drop original names df = df.drop('column_name', axis=1)
#earnings['GEOID'] = earnings['state']+earnings['county']

#   earnings
earnings['median (k)'] = earnings['B20002_001E'].astype(float)/1000 # expressing earnings in thousands
earnings['aggregate (k)'] = earnings['B20003_001E'].astype(float)/1000

#   populations
earnings['total Pop'] = earnings['B01003_001E']

#   race
earnings['total race'] = pd.to_numeric(earnings['B02001_001E'], errors='coerce')
earnings['white alone'] = pd.to_numeric(earnings['B02001_002E'], errors='coerce')
earnings['other race'] = earnings['total race'] - earnings['white alone']

#   education
earnings['less than hs'] = earnings['B20004_008E']
earnings['hs'] = earnings['B20004_009E']
earnings['some college or as'] = ['B20004_010E']




# earnings.to_csv('earnings.csv',index=False)


import geopandas as gpd
import pandas as pd
import numpy as np
import json
import os

# only for PRE- 2018
def change_bool(string):
    '''
    Changes string values to boolean
    '''
    if (string == 'Y') | (string =='y'):
        return 1
    if (string == 'N') | (string == 'n'):
        return 0
    return np.nan

def map_bool(cols, df):
    '''
    Maps string values in given columns to boolean
    '''
    for col in cols:
        if col not in list(df.columns):
            continue
        df[col] = df[col].apply(lambda x: change_bool(x))
    return df

# only for POST- 2018
def change_sex(x):
    '''
    Changes male and female vales of gender to numeric
    '''
    if (x == 1.0) | (x == 1):
        return 'M'
    elif (x == 2.0) | (x == 2):
        return 'F'
    else:
        return np.nan

def map_sex(col):
    '''
    Maps change_sex function to given gender column
    '''
    return col.apply(lambda x: change_sex(x))


# accounts for both types of formats
def clean_bool(df, yr):
    '''
    CHanges the necessary object columns to boolean
    '''
    if yr < 2018:
        c = ['sd_resident', 'searched', 'contraband_found', 'property_seized', 'arrested']
        
        return map_bool(c, df)
    
    else:
        df['gend'] = map_sex(df['gend'])
        return df


def clean_age(df, age_col = 'percieved_driver_age'):
    '''
    Filters out 'bad ages' most likely human error
    '''
    cts = df[age_col].value_counts() 
    bad_age = cts[cts <= 10].index
    return df[~df[age_col].isin(bad_age)]

def clean_time(df):
    '''
    Changes format of time to easily determine inter-twilight period 
    for Veil of Darkness
    '''
    df['time_stop'] = pd.to_datetime(df['time_stop'], format= '%H:%M', errors='coerce')
    return df


# only for POST- 2018
def map_race(df):
    '''
    Uses te existing race code map from:
    'http://seshat.datasd.org/pd/vehicle_stops_race_codes.csv'
    and observation to match the pre- 2018 race codes with the post- 2018
    '''

    race_dict = {
     'Asian' : 'A',
     'OTHER ASIAN': 'A',
     'Middle Eastern or South Asian': 'M',
     'BLACK': 'B',
     'CHINESE': 'C',
     'CAMBODIAN': 'D',
     'FILIPINO': 'F',
     'GUAMANIAN': 'G',
     'HISPANIC': 'H',
     'Hispanic/Latino/a': 'H',
     'INDIAN': 'I',
     'JAPANESE': 'J',
     'KOREAN': 'K',
     'LAOTIAN': 'L',
     'OTHER': 'O',
     'PACIFIC ISLANDER': 'P',
     'Pacific Islander': 'P',
     'SAMOAN': 'S',
     'HAWAIIAN': 'U',
     'VIETNAMESE': 'V',
     'WHITE': 'W',
     'White': 'W',
     'ASIAN INDIAN': 'Z',
     'Native American': 'N'
    }
    df['Race Code'] = df['race'].map(race_dict)
    return df

# only for POST- 2018
def map_service_area(df):
    '''
    Add an additional service area columns to the pre-existing data
    with just police beats to allow for multi- year analysis of 2018 
    with pre- 2018
    '''
    stop_beats = 'http://seshat.datasd.org/sde/pd/pd_beats_datasd.geojson'
    beats = gpd.read_file(stop_beats)
    # get unique beats
    unique_beats = beats[['beat', 'serv']].drop_duplicates('beat')
    beat_dict = dict(zip(unique_beats.beat, unique_beats.serv))
    df['service_area'] = df['beat'].map(beat_dict)
    return df

def rename_cols(df, yr):
    '''
    Renames columns to have same format pre and post 2018
    '''
    if yr < 2018:
        df = df.rename(columns={'subject_age': 'percieved_driver_age', 'subject_sex': 'driver_sex', 
                                'subject_race': 'driver_race'})
        return df
    else:
        df = df.rename(columns={'perceived_age': 'percieved_driver_age', 'gend': 'driver_sex', 
                                'Race Code': 'driver_race', 'reason_for_stop': 'stop_cause'})
        return df


'''
The following 3 functions create a feature called "outcome" for pre and post
2018. For the purpose of this study, the outcomes assigned are either:
"None", "Warning (verbal or written)", "Search of property was conducted",
"Property was seized", or "Custodial Arrest without warrant". These are chosen
because they make up the large majority of outcomes and they are consistent
across pre- and post- 2018 data.
'''

def check_outcome(row, year):
    if year < 2018:
        # check 'arrested', 'searched', 'property_seized'
        if row.arrested == 1.0:
            return 'Arrested'
        elif row.property_seized == 1.0:
            return 'Property was seized'
        elif row.searched == 1.0:
            return 'Search of property was conducted'
        return 'Not Applicable'
        
    else:
        a = row.action
        r = row.result
        
        # check worst outcome first
        if r == 'Custodial Arrest without warrant':
            return r
        elif (a == 'Search of property was conducted') | (a == 'Property was seized'):
            return a
        elif r == 'Warning (verbal or written)':
            return r
        
        return 'Not Applicable'
    
def outcome_map(df, yr):
    df_copy = df.copy()
    df_copy['outcome'] = df_copy.apply(lambda x: check_outcome(x, yr), axis=1)
    
    if yr < 2018:
        return df_copy.drop(columns=['arrested', 'property_seized', 'searched', 'obtained_consent', 'contraband_found'])
        
    return df_copy.drop(columns=['action', 'result'])


'''
The following 2 functions apply all the helper functions to clean the data
'''
def pre_2018_format(df, yr):
    df = clean_bool(df, yr)
    df = rename_cols(df, yr)
    df = clean_age(df)
    df = clean_time(df)
    df = outcome_map(df, yr)
    return df

def post_2018_format(df, yr):
    df = clean_bool(df, yr)
    df = map_race(df)
    df = map_service_area(df)
    df = rename_cols(df, yr)
    df = clean_age(df)
    df = clean_time(df)
    df = outcome_map(df, yr)
    return df


def format_df(df, yr):
    '''
    Formats the data given the year and puts the columns in the same order 
    (easier to read when looking at two df)
    '''
    if yr < 2018:
        cols = ['stop_id', 'stop_cause', 'date_stop', 'time_stop', 'outcome', 'service_area', 'driver_race', 
                'driver_sex', 'percieved_driver_age', 'sd_resident']
        df = pre_2018_format(df, yr)
        return df[cols]
    
    else:
        cols = ['stop_id', 'pid', 'stop_cause', 'reason_for_stopcode', 'date_stop', 'time_stop', 'stopduration', 
                'outcome', 'beat', 'service_area', 'driver_race', 'driver_sex', 'percieved_driver_age',
                'officer_assignment_key', 'exp_years', 'year']
        df = post_2018_format(df, yr)
        
        # check for last duplicate
        df = df.drop_duplicates(subset = ['stop_id', 'date_stop', 'time_stop', 'beat', 'officer_assignment_key'])
        
        # add year column for future concating / analysis by year
        df['year'] = [yr] * df.shape[0]
    
        return df[cols]
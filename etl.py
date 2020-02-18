import geopandas as gpd
import pandas as pd
import numpy as np
import json
import os

from cleaning import *

def get_table(yr):
    '''
    Gets a table of raw data given a year
    '''
    if yr < 2018:
        url = 'http://seshat.datasd.org/pd/vehicle_stops_{}_datasd_v1.csv'.format(yr)
        return pd.read_csv(url)
    
    else: # post- 2018
        # cols we care about
        cols_2018 = ['stop_id', 'pid', 'date_stop', 'time_stop', 'stopduration', 
                 'officer_assignment_key', 'exp_years', 'beat', 
                 'perceived_age', 'gend']

        url = 'http://seshat.datasd.org/pd/ripa_stops_datasd_v1.csv'
        df = pd.read_csv(url)
        return df[cols_2018]


def get_merge_data():
    '''
    Gets data from tables needed to add to post- 2018 basic data
    '''
    reason = 'stop_reason'
    reason_cols = ['stop_id', 'pid', 'reason_for_stop', 'reason_for_stopcode']

    result = 'stop_result'
    result_cols= ['stop_id', 'pid', 'result']

    race = 'race'
    race_cols = ['stop_id', 'pid', 'race']

    action = 'actions_taken'
    action_cols = ['stop_id', 'pid', 'action']

    base = 'http://seshat.datasd.org/pd/ripa_{}_datasd.csv'

    reason_df = pd.read_csv(base.format(reason))
    result_df = pd.read_csv(base.format(result))
    race_df = pd.read_csv(base.format(race))
    action_df = pd.read_csv(base.format(action))
    
    return [[reason_cols, result_cols, race_cols, action_cols], [reason_df, result_df, race_df, action_df]]

def gen_cols(df1, gen_df, cols):
    '''
    Merges a table of additional data with current data
    '''

    new = df1.merge(gen_df, on = ['stop_id', 'pid'])
    drop = [x for x in new.columns if x not in cols]
    new = new.drop(columns = drop).drop_duplicates(subset = ['stop_id', 'pid'])
    return new

def merge_data(tbl):
    '''
    Merges all the additional data for post- 2018 with the raw basic data
    '''

    merge_cols = get_merge_data()[0]
    merge_dfs = get_merge_data()[1]
    merged = []

    for i in range(len(merge_dfs)):
        merged.append(gen_cols(tbl, merge_dfs[i], merge_cols[i]))
          
    first = merged[0]
    for i in range(0, len(merged)):
        if i == len(merged) - 1:
            break 
        first = pd.merge(first, merged[i + 1], on =  ['stop_id', 'pid'])

    df = pd.merge(tbl, first, on = ['stop_id', 'pid'])
    df = df.drop_duplicates(subset = ['stop_id', 'pid'])
    return df


def get_data(yr):
    '''
    Gets cleaned and formatted data given the year
    '''
    tbl = get_table(yr)
    if yr < 2018:
        return format_df(tbl, yr)

    else:
        df = merge_data(tbl)
        return format_df(df, yr)
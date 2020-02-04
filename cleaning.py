c = {'col1': func1}

# helper functions for cleaning / merging
def c_bool(string):
    if (string == 'Y') | (string =='y'):
        return 1
    elif (string == 'N') | (string == 'n'):
        return 0
    else: 
        return np.nan

def make_bool(cols, df):
    for col in cols:
        if col not in list(df.columns):
            continue
        df[col] = df[col].apply(lambda x: c_bool(x))
    return df

def check_outcome(row):    
    to_check = ['arrest_made', 'property_seized']
    for check in to_check:
        if row.loc[check] == 1:
            return check
    return np.nan
    
def create_outcome(df):
    outcome = []
    for i in range(df.shape[0]):
        outcome.append(check_outcome(df.loc[i]))
    df['outcome'] = outcome
    return df

def add_stop_reason(df):
    url = 'http://seshat.datasd.org/pd/ripa_stop_reason_datasd.csv'
    reason = pd.read_csv(url)
    return df.merge(reason, on = 'stop_id').drop_duplicates()


def add_stop_outcome(df):
    url = 'http://seshat.datasd.org/pd/ripa_stop_result_datasd.csv'
    outcome = pd.read_csv(url)
    return df.merge(outcome, on = 'stop_id').drop_duplicates()

def add_data(df):
    df = add_stop_reason(df)
    df = add_stop_outcome(df)    
    return df


def clean_results(year, df):
    if int(year) < 2018:        
        # do something
        mapper = {'stop_id': 'stop_id', 'stop_cause': 'stop_cause', 'service_area': 'service_area', 
                  'subject_race': 'driver_race', 'subject_sex': 'driver_sex', 'subject_age': 'driver_age',
                  'date_stop': 'stop_date',  'time_stop': 'stop_time', 'sd_resident': 'sd_resident',
                  'arrested': 'arrest_made', 'searched': 'search_conducted', 'contraband_found': 'contraband_found',
                  'property_seized': 'property_seized'
                 }
        col_keep = list(mapper.keys())
        change_bool = ['sd_resident', 'search_conducted', 'contraband_found', 'property_seized', 'arrest_made']
        df = df[col_keep]
        df = df.rename(columns=mapper)
        df = make_bool(change_bool, df)
        df = create_outcome(df)
            
    else: # year >= 2018
        # do something else
        mapper = {'stop_id': 'stop_id', 'stop_cause': 'stop_cause', 'service_area': 'service_area', 
                  'subject_race': 'driver_race', 'gend': 'driver_sex', 'subject_age': 'driver_age',
                  'date_stop': 'stop_date',  'time_stop': 'stop_time', 'sd_resident': 'sd_resident',
                  'arrested': 'arrested', 'searched': 'searched', 'contraband_found': 'contraband_found',
                  'property_seized': 'property_seized', 'exp_years': 'exp_years', 'stopduration': 'stop_duration',
                  'address_city': 'address_city', 'beat': 'beat', 'pid': 'driver_id', 
                  'perceived_limited_english': 'perceived_limited_english'
                 }
        col_keep = list(mapper.keys())
        df = df.rename(columns=mapper)
        df = make_bool(change_bool, df)
        df = add_data(df)
    
    return df 


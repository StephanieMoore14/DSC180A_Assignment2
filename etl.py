def get_table(year):
    if int(year) < 2018:
        url = 'http://seshat.datasd.org/pd/vehicle_stops_{}_datasd_v1.csv'.format(year)
        df =  pd.read_csv(url)
        
    else: # year >= 2018
        url = 'http://seshat.datasd.org/pd/ripa_stops_datasd_v1.csv'
        df = pd.read_csv(url)
        
    return df


    # The ingestion pipeline should take in the year (between 2014 and 2019) as a parameter
def load_data(years, outpath):
    '''
    downloads and saves tables at the specified output directory
    for the given years and teams.
    :param: years: a list of seasons to collect
    :param: teams: a list of teams to collect
    :param: outpath: the directory to which to save the data.
    '''
    for year in years:
        if not os.path.exists(outpath):
            os.mkdir(outpath)

            # save df as csv
            path = '{}/sdvehicle_stops_{}.csv'.format(outpath, year)
            
            results = get_table(year)
            
            # do some cleaning
            clean_ = clean_results(year, results)    
            clean_.to_csv(path)   



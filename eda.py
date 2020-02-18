import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def null_dist(df, cols):
    
    n = df[cols].isnull().sum()
    return pd.DataFrame(n.values / df.shape[0], columns=['% Null'], index = n.index).T

def make_hist(ser, t, col):
	ser.plot.hist(bins=10000, title=t, colormap='jet', figsize=(8,8))
	plt.xlabel(col)
	plt.ylabel('FREQUENCY')
	plt.axis([0, 150, 0, 4000]);  #[xmin, xmax, ymin, ymax]


def plot_minute(df):
	d = df.dropna()
	t = d['time_stop'].apply(lambda x: int(x[-2:]))
	t.hist()
	plt.xlabel('minute')
	plt.ylabel('FREQUENCY')

def plot_outcomes(df):
    d = df[df.outcome != 'Not Applicable']

    ser = d.outcome.value_counts()
    labels = ser.index
    sizes = ser.values

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Outcome Distribution')
    plt.show()


def plot_races(df):
	df.driver_race.value_counts().plot(kind='bar')
	plt.title('Distribtion of Race Codes')
	plt.xlabel('Race Code')
	plt.ylabel('Value Counts')
	plt.show()


def outcome_dist(df, r):
    a1 = df[df['driver_race'] == r]['outcome'].value_counts()
    a2 = df['outcome'].value_counts()
    return pd.Series(np.divide(a1.values, a2.values), index=a1.index)

def get_stop_rates(df):
    d = {}
    l = ['W', 'B', 'H', 'A', 'O']
    total_pop_2010 = 3095313
    for r in l:
        d[r] = df[df.driver_race == r].shape[0] / total_pop_2010
    return pd.DataFrame(d.values(), index = d.keys(), columns=['Stop Rates']).sort_values(by='Stop Rates', ascending=False).T

'''
For Veil of Darkness Analysis
'''

def filter_stop_reason(df):
    return df[(df['stop_cause'] == 'Moving Violation') | (df['stop_cause'] == 'Equipment Violation')]    

def get_veil(df):
    inter = df[(df['time_stop'] >=  pd.to_datetime('17:39', format= '%H:%M')) & (df['time_stop'] <= pd.to_datetime('20:59', format= '%H:%M'))]
    inter['time_stop'] = inter['time_stop'].apply(lambda x: x.time())
    
    inter = filter_stop_reason(inter)
    return inter
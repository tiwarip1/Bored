import pandas as pd
import os

def add_rolling_average(df,n):
    '''This is a general function that makes a rolling average over n
    data points'''
    
    df['{}ma'.format(int(n/12))]=df['Close'].rolling(window=n,min_periods=0).mean()
    return df['{}ma'.format(int(n/12))]

def retrieve_csv(ticker):
    
    try:
        return pd.read_csv('../../stored_data/{}.csv'.format(ticker))
    except FileNotFoundError:
        return 'Not Found'

def list_files_with_data():
    
    for i in os.path('../../stored_data'):
        print(i)

def main():
    
    list_files_with_data()
import csv
import datetime
import re
import os

import pandas as pd
import requests
import numpy as np
import datetime as dt

def get_google_finance_intraday(ticker, period=300, days=60):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """

    uri = 'https://finance.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'\
          .format(ticker=ticker,period=period,days=days)
    page = requests.get(uri)
    reader = csv.reader(page.text.splitlines())
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*\
                                                      int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                            columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
    
    
def collect_data(ticker):
    '''This function will add data to a database over time'''
    
    cont = True
    
    if not os.path.exists('../../stored_data/'):
        os.makedirs('../../stored_data/')
    
    if '{}.csv'.format(ticker) in os.listdir('../../stored_data/'):
        print(ticker)
        df = get_google_finance_intraday(ticker,300)
        if 'Date' in df.columns:
            pass
        else:
            df['Date']=df.index
            df['Date'] = pd.to_datetime(df['Date'])
        df.index.name = 'Date'
    else:
        df = get_google_finance_intraday(ticker,300,300)
        if 'Date' in df.columns:
            pass
        else:
            df['Date']=df.index
            df['Date'] = pd.to_datetime(df['Date'])
        df.index.name = 'Date'
        df.to_csv('../../stored_data/{}.csv'.format(ticker))
        cont = False
    
    df1 = pd.read_csv('../../stored_data/{}.csv'.format(ticker))
    df1 = df1[np.isfinite(df1['Open'])]
    time_str = df1.iloc[len(df1)-1]['Date']
    try:
        datetime_index = dt.datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
    except ValueError:
        datetime_index = dt.datetime.strptime(time_str,'%m/%d/%Y %H:%M')
    date_data = dt.datetime.now().date()-datetime_index.date()
    
    if cont:
        df2=get_google_finance_intraday(ticker,300,date_data.days)
        if 'Date' in df2.columns:
            pass
        else:
            df2['Date']=df2.index
            df2['Date'] = pd.to_datetime(df2['Date'])
        mask = df2['Date']>datetime_index
        df2 = df2[mask]
        df1.drop('Date',axis = 1)
        df2.drop('Date',axis = 1)
        df3 = pd.concat([df1,df2],ignore_index = True)
        if 'Date' in df3.columns:
            pass
        else:
            df3['Date']= df3.index
            df3['Date'] = pd.to_datetime(df3['Date'])
        df3 = df3.loc[:, ~df3.columns.str.contains('^Unnamed')]

        os.remove('../../stored_data/{}.csv'.format(ticker))
        df3.to_csv('../../stored_data/{}.csv'.format(ticker))
        
collect_data('TSLA')

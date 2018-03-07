import bs4 as bs
import requests
import datetime as dt
import pandas as pd
import os

from visualization import save_sp500_tickers
from interested_stocks import is_worktime

def nasdaq_data(ticker = 'TSLA'):
    '''still need to add the additional data for csv's'''
    url = 'https://www.nasdaq.com/symbol/{}/real-time'.format(ticker)
          
    page = requests.get(url).text
    soup = bs.BeautifulSoup(page,'lxml')
    table = soup.find('div',{'class':'genTable'})
    
    row_l = []
    for row in table.findAll('span')[8:]:
        row=list(row)
        row_l.append(row)
        
    current_time = dt.datetime.today().replace(second = 0,microsecond = 0)
    df = pd.DataFrame(data = {'Close':float(row_l[0][0]),'Volume':int(row_l[4][0].replace(',',''))},index = [0])
    df['Date'] = pd.to_datetime(current_time)
    
    return df

def add_to_existing_csv(df,ticker):
    
    if os.exists
        
def collect_nasdaq():
    
    list_500 = save_sp500_tickers
    
    for i in list_500:
        current_time = dt.datetime.now()
        
        if is_worktime():
            df1 = nasdaq_data(i)
            
collect_nasdaq()
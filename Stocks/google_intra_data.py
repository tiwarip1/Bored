import bs4 as bs
import requests
import datetime as dt
import pandas as pd
import os
import time

from visualization import save_sp500_tickers

def nasdaq_data(ticker = 'TSLA'):
    
    session = requests.Session()
    url = 'https://www.nasdaq.com/symbol/{}/real-time'.format(ticker)
    try:
        page = requests.get(url).text
    except requests.ConnectionError:
        print('problem')
        session.close()
        time.sleep(10)
        session = requests.Session()
        page = requests.get(url).text
    soup = bs.BeautifulSoup(page,'lxml')
    table = soup.find('div',{'class':'genTable'})
    
    if type(table)==type(None):
        return 0
    
    row_l = []
    for row in table.findAll('span')[8:]:
        row=list(row)
        row_l.append(row)
        
    current_time = dt.datetime.today().replace(second = 0,microsecond = 0)
    df = pd.DataFrame(data = {'Close':float(row_l[0][0]),'Volume':int(row_l[4][0].replace(',',''))},index = [0])
    df['Date'] = pd.to_datetime(current_time)
    
    session.close()
    
    return df

def remove_unwanted_columns(df,unwanted):
    
    if '{}'.format(unwanted) in df.columns:
        df = df.drop('{}'.format(unwanted),1)
    
    return df

def is_worktime():

    now = dt.datetime.today()
    if now.date().weekday()<5 and dt.time(9,30) <= now.time() and \
    now.time() <= dt.time(16,30):
        return True
    else:
        return False

def add_to_existing_csv(ticker):
    
    df1 = nasdaq_data(ticker)
    try:
        df = pd.read_csv('../../stored_data/{}.csv'.format(ticker))
    except FileNotFoundError:
        return 
    try:
        df3 = pd.concat([df,df1],ignore_index = True)
    except TypeError:
        return
    df3 = df3.loc[:, ~df3.columns.str.contains('^Unnamed')]
    unwanted = ['300ma','100ma','60ma','40ma','20ma','double_derivative',\
                'Open','High','Low']
    for i in unwanted:
        df3 = remove_unwanted_columns(df3,i)
        
    if type(df3)!=int:
        os.remove('../../stored_data/{}.csv'.format(ticker))
        df3.to_csv('../../stored_data/{}.csv'.format(ticker))
    
        
def nasdaq(num):
    
    list_500 = save_sp500_tickers()
    start = num*125
    end = (num+1)*125
    for i in list_500[start:end]:#[start:end]:
        print(i)
        if is_worktime():
            add_to_existing_csv(i)
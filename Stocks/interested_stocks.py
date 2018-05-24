from collect_intra_data import collect_data
from visualization import save_sp500_tickers
from google_intra_data import is_worktime
import os
import time
import datetime as dt
import requests

def initial_collect():
    
    list_500 = save_sp500_tickers()

    for i in list_500:
        if not os.path.exists('../../stored_data/{}.csv'.format(i)):
            collect_data(i)
        else:
            print('I got it')
            
def collect_sp500():
    
    list_500 = save_sp500_tickers()

    for i in list_500:
        try:
            collect_data(i)
        except IndexError:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(300)
            collect_data(i)
        time.sleep(5)

def is_weekday():

    now = dt.datetime.today()
    if now.date().weekday()<5:
        return True
    else:
        return False

def update_data_every_n_minutes(n):
    
    while True:
        tock = time.time()
        if is_worktime() :
            print('yaas')
            try:
                collect_sp500()
            except KeyboardInterrupt:
                print('Manual break by user')
                return
        print('sleepytime')
        tick=time.time()

        if tick-tock<n*60:
            time.sleep(n*60-(tick-tock))

update_data_every_n_minutes(60)

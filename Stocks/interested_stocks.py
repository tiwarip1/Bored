from collect_intra_data import collect_data
from visualization import save_sp500_tickers
from google_intra_data import nasdaq,is_worktime
import os
import time
import datetime as dt

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
        time.sleep(5)

def is_weekday():

    now = dt.datetime.today()
    if now.date().weekday()<5:
        return True
    else:
        return False

def update_data_every_n_minutes(n):
    
    while True:

        if is_worktime() :
            print('yaas')
            try:
                collect_sp500()
            except KeyboardInterrupt:
                print('Manual break by user')
                return
        print('sleepytime')
        time.sleep(n*60)

update_data_every_n_minutes(60)
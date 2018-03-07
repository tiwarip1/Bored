from collect_intra_data import collect_data
from visualization import save_sp500_tickers
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

def is_weekday():

    now = dt.datetime.today()
    if now.date().weekday()<5:
        return True
    else:
        return False
    
def is_worktime():

    now = dt.datetime.today()
    if now.date().weekday()<5 and dt.time(9,30) <= now.time() and \
    now.time() <= dt.time(16,30):
        return True
    else:
        return False

def update_data_every_n_minutes(n = 15):
    
    while True:

        if is_worktime() :
            print('yaas')
            try:
                collect_sp500()
            except KeyboardInterrupt:
                print('Manual break by user')
                return
        print('sleepytime')
        time.sleep(n * 60)
    

update_data_every_n_minutes(15)

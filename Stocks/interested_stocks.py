from collect_intra_data import collect_data
from visualization import save_sp500_tickers
import os
import time
import datetime as dt

def collect_sp500():
    
    list_500 = save_sp500_tickers()

    for i in list_500:
        if not os.path.exists('../../stored_data/{}.csv'.format(i)):
            collect_data(i)
        else:
            print('I got it')
            
def update_data_every_5_minutes():
    
    while True:
        now = dt.datetime.now()
        if dt.datetime.now()==dt.datetime.weekday and \
        dt.time(9,30) <= now.time() <= dt.time(16,30):
            print('yaas')
            try:
                collect_sp500()
                time.sleep(30)
            except KeyboardInterrupt:
                print('Manual break by user')
                return

update_data_every_5_minutes()
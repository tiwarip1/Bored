from classes import transactions
from functions import n_day_RSI

import pandas as pd
import numpy as np

# =============================================================================
# thing = transactions(symbol='MAXR',number_stocks=30,convert=False)
# thing.buy(67.83)
# thing.sell(67.25,20)
# thing.override=True
# thing.sell(69.97,10)
# print(thing.total())
# =============================================================================

df = pd.read_csv('../../../daily_close/AAPL.csv')
df = n_day_RSI(20,df)
action='buy'
totals=[]
close='close'
#previous_row = pd.DataFrame()
#print(df.head())

for buy in range(0,90,5):
    inter=[]
    for sell in range(10,100,5):
        stock = transactions(symbol='NFLX')
        for index,row in df.iterrows():
            if index>1:
                if row['RSI']>=buy and action=='buy' and previous_row['RSI']<\
                row['RSI']:
                    stock.buy(row[close],100)
                    action='sell'
                elif row['RSI']<=sell and action=='sell' and \
                previous_row['RSI']>row['RSI']:
                    stock.sell(row[close],100)
                    action='buy'
            previous_row = row
        tot = stock.total()
        inter.append(tot)
        print('Buying at {} and selling at {} gives a total of {}'.format(buy,\
              sell,tot))
    totals.append(inter)
    
    
np.savetxt("RSI_testing.csv", totals, delimiter=",")
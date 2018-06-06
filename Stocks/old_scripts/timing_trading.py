import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os

'''This program will take the data that is stored and repeatedly parse through
it using the optimal setting for rolling averages and using the intersection
of these rolling averages, it will prompt the user to buy or sell a certain
stock'''

def add_rolling_average(df,n):
    '''This is a general function that makes a rolling average over n
    data points'''
    
    df['{}ma'.format(n)]=df['Close'].rolling(window=n*12,min_periods=0).mean()
    return df

def optimal_settings():
    '''Takes the optimal settings from a previously made csv'''
    
    df = pd.read_csv('../../Testing_inter/optimal_settings.csv')
    return df

def buy_or_sell(df,buying,selling):
    '''Modified correct_returns from rolling_intersections to fit the needs
    of this program, but it goes through and finds whether the time to buy or
    sell is within a certain hour range'''
    
    buy_stock = []
    sell_stock = []
    previous_row = pd.DataFrame(columns=df.columns)
    previous_row = previous_row.fillna(0) # with 0s rather than NaNs
    sell_if_can=False
    hour_range = 1
    
    for index,row in df.iterrows():
        
        Current_adj_close=row['Close']
        if previous_row.empty:
            
            pass
        
        elif row['{}ma'.format(selling)]<row['{}ma'.format(buying)] and \
        sell_if_can==False and \
        previous_row['{}ma'.format(selling)]>previous_row['{}ma'.format(buying)]:
            
            buy_stock.append(Current_adj_close)
            sell_if_can = True
            dt_object = dt.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')

            if dt_object>dt.datetime.now()-dt.timedelta(hours = hour_range):
                return ['buy',Current_adj_close]
            
        elif sell_if_can==True and \
        previous_row['{}ma'.format(selling)]<previous_row['{}ma'.format(buying)]\
        and row['{}ma'.format(selling)]>row['{}ma'.format(buying)]:
            
            sell_stock.append(Current_adj_close)
            sell_if_can=False
            dt_object = dt.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
            
            if dt_object>dt.datetime.now()-dt.timedelta(hours = hour_range):
                return ['sell',Current_adj_close]
            
        previous_row=row
        

    sell_stock.append(Current_adj_close)


def parse_old_data(settings,ticker):
    '''This function takes the stored data and parses through it using the
    most optimal settings and see if now is the correct time to buy or sell
    with a window of an hour'''
    
    '''Mask is used to take these settings and remove everything else'''
    mask = settings['Ticker']==ticker
    try:
        buy = settings[mask]['Buy'].values[0]
    except:
        #print('{} is not present in the optimal settings'.format(ticker))
        return False
    sell = settings[mask]['Sell'].values[0]

    '''Will look only at part of the data that is most relevant and add the 
    necessary rolling averages'''
    df = pd.read_csv('../../stored_data/{}.csv'.format(ticker))
    window = df.iloc[-76*sell+15:]
    window = add_rolling_average(window,buy)
    window = add_rolling_average(window,sell)

    '''This section has been edited for testing, remove allowed for fully 
    working program'''
    allowed = ['ESS','TWX','UNH','ABBV','ESRX','MS','WMB','AKAM','ABC','EL','HRL']
    
    stuff = buy_or_sell(window,buy,sell)
    if stuff==None:
        pass
    elif stuff[0]=='buy':
        #print('Buy {} at {}'.format(ticker,stuff[1]))
        pass
    elif stuff[0]=='sell' and ticker in allowed:
        print('Sell {} at {}'.format(ticker,stuff[1]))
    #print(buy_or_sell(window,sell,buy))
    '''
    plt.plot(window.index,window['Close'],alpha=.6,color='k',label='Price')
    plt.plot(window.index,window['{}ma'.format(buy)],'b--',label='Buying')
    plt.plot(window.index,window['{}ma'.format(sell)],'r--',label='Selling')
    plt.legend(loc='upper left')'''

def main():
    
    '''Takes the optimal settings for rolling averages'''
    settings = optimal_settings()
    for file in os.listdir("../../stored_data/"):
        if file.endswith(".csv"):
            ticker = file[:file.find(".csv")]
            parse_old_data(settings,ticker)

while True:
    main()

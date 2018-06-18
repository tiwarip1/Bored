import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import requests
import time
import bs4 as bs
import re
import csv
import codecs
import pickle
import pandas_datareader as web

'''This is a main python file that stores all the important functions to be 
called by other scripts'''

def bollinger(std=20,tsx=False,plot=False):
    '''This function iterates over the dataset and checks to see which stocks
    are below their bolinger band to see if they are oversold'''
    
    tsx_stocks = save_tsx()
    
    for file in os.listdir("../../../stored_data/"):
        if file.endswith(".csv"):
            ticker = file[:file.find(".csv")]
            df = pd.read_csv('../../../stored_data/{}.csv'.format(ticker))
            
            df = create_bollinger(df,std)
            try:
                if df['{} lower'.format(std)].iloc[-1]>df['Close'].iloc[-1]:
                    if ticker in tsx_stocks:
                        print('You should buy {}'.format(ticker))
            except KeyError:
                if df['{} lower'.format(std)].iloc[-1]>df['close'].iloc[-1]:
                    if ticker in tsx_stocks:
                        print('You should buy {}'.format(ticker))
                
                        plt.plot(df['close'])
                        plt.plot(df['{} upper'.format(std)])
                        plt.plot(df['{} lower'.format(std)])
                        plt.show()

    
    
    
    
def create_bollinger(df,std):
    '''This function uses a provided dataframe and adds bollinger bands for
    the upper and lower bounds to the end of the columns'''

    try:
        df['{} std'.format(std)] = df['Close'].rolling(window=std,min_periods=0).std()
        df['{} mean'.format(std)] = df['Close'].rolling(window=std,min_periods=0).mean()
    except KeyError:
        df['{} std'.format(std)] = df['close'].rolling(window=std,min_periods=0).std()
        df['{} mean'.format(std)] = df['close'].rolling(window=std,min_periods=0).mean()
    df['{} upper'.format(std)] = df['{} mean'.format(std)]+2*df['{} std'.format(std)]
    df['{} lower'.format(std)] = df['{} mean'.format(std)]-2*df['{} std'.format(std)]
    df = df.iloc[1:]
    df = remove_unwanted_columns(df,'{} std'.format(std))
    df = remove_unwanted_columns(df,'{} mean'.format(std))
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def daily_close(stock='TSLA',start=dt.datetime(2013,1,1)):
    '''This function takes the closing data at the end of the day for a number
    of stocks and stores them, this will be used to analysis over longer time
    frames'''

    now = dt.datetime.now()
    end=dt.datetime(now.year,now.month,now.day)
    
    dataframe = web.DataReader(stock,'iex',start,end)
    
    if not os.path.exists('../../../daily_close'):
        os.makedirs('../../../daily_close')
    
    dataframe.to_csv('../../../daily_close/{}.csv'.format(stock))




def add_rolling_average(df,n,name='ma',thing='Close',backwards=False):
    '''This is a general function that makes a rolling average over n
    data points'''
    if backwards:
        df['{}{}'.format(n,name)]=df[thing][::-1].rolling(window=n*12,min_periods=0).mean()
    else:
        df['{}{}'.format(n,name)]=df[thing].rolling(window=n*12,min_periods=0).mean()
    return df




def save_tsx():
    '''Basically copy pasted save_sp500_tickers and changed the url'''
    
    resp=requests.get('https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index')
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table',{'class':'wikitable sortable'})
    stock_names = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        stock_names.append(ticker)
            
    with open('tsxtickers.pickle','wb') as f:
        pickle.dump(stock_names,f)
    
    return stock_names




def n_day_RSI(n,df,plot=False):
    '''Takes the RSI and plots it over an n-day period'''
    
    previous_row=0
    gain=[]
    loss=[]
    
    for index,row in df[-100:].iterrows():
        
        if previous_row!=0:
            
            if row['Close']<previous_row:
                gain.append(0)
                loss.append(-round(row['Close']-previous_row,2))
            elif row['Close']>previous_row:
                gain.append(round(row['Close']-previous_row,2))
                loss.append(0)
        
        previous_row = row['Close']
    
    data = {'gain':gain,'loss':loss}
    df1 = pd.DataFrame(data=data)
    add_rolling_average(df1,n,'gain','gain',True)
    add_rolling_average(df1,n,'loss','loss',True)
    df1['RS']=df1['{}gain'.format(n)]/df1['{}loss'.format(n)]
    df1['RSI']=100-100/(1+df1['RS'])
    
    if plot:
        #fig=plt.figure(figsize=[20,10])
        plt.plot(df1['RSI'])
        ax=plt.gca()
        ax.set_ylim(min(df1['RSI']),max(df1['RSI']))
        ax.set_xlim(0,len(df1['RSI']))
        plt.show()
        
    return df1
    
    


def get_all_tickers():
    '''This function takes all the tickers from each exchange that we are 
    interested in'''
    
    list_500 = save_sp500_tickers()

    additional_stocks = ['TSLA','AMBD','SIN']
    additional_stocks = additional_stocks+save_tsx()
    
    for i in additional_stocks:
        list_500.append(i)

    return list_500



def collect_sp500():
    '''Collects the stocks from the sp500'''
    
    which_section = int(input("1 or 2? "))
    
    list_500 = get_all_tickers()

    if which_section==1:
        list_500= list_500[:int(len(list_500)/2)]
    elif which_section==2:
        list_500=list_500[int(len(list_500)/2):]

    for i in list_500:
        try:
            collect_data(i)
        except IndexError:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(300)
            collect_data(i)
        time.sleep(5)




def save_sp500_tickers():
    
    '''This function takes the S&P 500 list and creates csvs for each of them
    using beautiful soup'''
    
    resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table',{'class':'wikitable sortable'})
    stock_names = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        stock_names.append(ticker)
            
    with open('sp500tickers.pickle','wb') as f:
        pickle.dump(stock_names,f)
    
    return stock_names
        




def testing_rolling_data(df,ticker):
    '''This goes over each item in stored data and uses rolling averages 
    between 5 and 55 and finds how much profit would be made if a stock were 
    bought or sold at those settings by calling check_rolling_returns'''
    
    rows = []
    for i in range(5,60,5):
        columns = []
        for j in range(5,60,5):
            if i>=j:
                columns.append(0)
                continue
            df1 = df
            df1 = add_rolling_average(df1,i)
            df1 = add_rolling_average(df1,j)
            columns.append(check_rolling_returns(df1,i,j))
        rows.append(columns)

    fig=plt.figure(figsize=[20,10])
    ax1=plt.subplot((10,5),(0,0),rowspan=5,columnspan=5,ylabel='Heat Map',\
                    title=ticker)
    ax1.imshow(rows)
    ax1.colorbar()
    ax = ax1.gca()
    ax.set_xticklabels(np.arange(-5,70,10))
    ax.set_xlabel('selling')
    ax.set_yticklabels(np.arange(-5,70,10))
    ax.set_ylabel('buying')
    #plt.show()
    if not os.path.exists('Testing/'):
        os.mkdir('Testing')
    fig.savefig('Testing/{}.png'.format(ticker),dpi=200,bbox_inches='tight')




    
def check_rolling_returns(df,buying,selling):
    '''This uses a given buying or selling rolling average given in df and loops over that returning the profit made by using these averages'''
    
    buy_stock = []
    sell_stock = []
    Previous_adj_close=0
    sell_if_can=False
    sum_total = 0
    
    for index,row in df.iterrows():
        
        Current_adj_close=row['Close']
        
        if row['{}ma'.format(buying)]<Previous_adj_close and row['{}ma'.format(buying)]>\
        Current_adj_close and row['{}ma'.format(selling)]<row['{}ma'.format(buying)] and \
        sell_if_can==False:
            
            buy_stock.append(Current_adj_close)
            sell_if_can = True
            
        if sell_if_can==True and row['{}ma'.format(selling)]>Previous_adj_close and \
        row['{}ma'.format(selling)]<Current_adj_close and row['{}ma'.format(selling)]>buy_stock[-1]:
            sell_stock.append(Current_adj_close)
            sell_if_can=False
        Previous_adj_close=Current_adj_close

    sell_stock.append(Current_adj_close)

    for i in range(0,len(buy_stock)):
        
        sum_total+=sell_stock[i]-buy_stock[i]
        
    return round(sum_total,3)





def get_google_finance_intraday(ticker, period=300, days=60):
    """
    Used to take the data for a stock with a certain period

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
    reader = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    try:
        for row in reader:
            break
    except:
        print("Ran into a UnicodeEncode Error, but it was dealt with")
        time.sleep(3600)
        uri = 'https://finance.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'\
          .format(ticker=ticker,period=period,days=days)
        page = requests.get(uri)
        reader = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
        columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        rows = []
        times = []
    
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = dt.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+dt.timedelta(seconds=period*\
                                                      int(row[0])))
                rows.append(map(float, row[1:]))
    if len(rows):
        print(rows[0])
        try:
            return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                            columns=columns)
        except ValueError:
            if len(rows)<len(times):
                difference_index = -len(rows)+len(times)
                times=times[difference_index:]
            elif len(rows)>len(times):
                difference_index = len(rows)-len(times)
                rows=rows[difference_index:]
            return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                            columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))





def collect_data(ticker):
    '''This function will add data to a database over time and does all the 
    dirty work of collecting data and parsing everything to make it look nice 
    and removing the unecessary stuff'''
    
    cont = True
    
    if not os.path.exists('../../../stored_data/'):
        os.makedirs('../../../stored_data/')
    
    if '{}.csv'.format(ticker) in os.listdir('../../../stored_data/'):
        print(ticker)
        df = get_google_finance_intraday(ticker,300,2)
        if 'Date' in df.columns:
            pass
        else:
            df['Date']=df.index
            df['Date'] = pd.to_datetime(df['Date'])
        df.index.name = 'Date'
    else:
        print(ticker)
        df = get_google_finance_intraday(ticker,300,300)
        if 'Date' in df.columns:
            pass
        else:
            df['Date']=df.index
            df['Date'] = pd.to_datetime(df['Date'])
        df.index.name = 'Date'
        df.to_csv('../../../stored_data/{}.csv'.format(ticker))
        cont = False
    
    df1 = pd.read_csv('../../../stored_data/{}.csv'.format(ticker))
    try:
        df1 = df1[np.isfinite(df1['Close'])]
    except KeyError:
        pass
    time_str = df1.iloc[len(df1)-1]['Date']
    try:
        datetime_index = dt.datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
    except ValueError:
        datetime_index = dt.datetime.strptime(time_str,'%Y %H:%M')
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
        df3 = pd.concat([df1,df2],ignore_index = True)
        if 'Date' in df3.columns:
            pass
        else:
            df3['Date']= df3.index
            df3['Date'] = pd.to_datetime(df3['Date'])
        df3 = df3.loc[:, ~df3.columns.str.contains('^Unnamed')]
        try:
            df3 = df3.drop('Date.1',1)
        except ValueError:
            pass

        try:
            df3 = df3.drop('Open',1)
            df3 = df3.drop('High',1)
            df3 = df3.drop('Low',1)
            df3 = df3.drop('300ma',1)
            df3 = df3.drop('100ma',1)
            df3 = df3.drop('60ma',1)
            df3 = df3.drop('40ma',1)
            df3 = df3.drop('20ma',1)
        except ValueError:
            pass
        os.remove('../../../stored_data/{}.csv'.format(ticker))
        df3.to_csv('../../../stored_data/{}.csv'.format(ticker))





def nasdaq_data(ticker = 'TSLA'):
    '''Takes the current stock price from NASDAQ and returns it as a dataframe'''
    
    session = requests.Session()
    url = 'https://www.nasdaq.com/symb../../../real-time'.format(ticker)
    try:
        page = requests.get(url).text
    except requests.ConnectionError:
        print('problem')
        session.close()
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
    '''Removes an unwanted column from a dataframe'''
    if '{}'.format(unwanted) in df.columns:
        df = df.drop('{}'.format(unwanted),1)
    
    return df





def is_worktime():
    '''Checks if the current time aligns with regular trading times for the east coast'''
    now = dt.datetime.today()
    if now.date().weekday()<5 and dt.time(9,30) <= now.time() and \
    now.time() <= dt.time(16,30):
        return True
    else:
        return False





def add_to_existing_csv(ticker):
    '''Uses the nasdaq to take realtime data'''
    
    df1 = nasdaq_data(ticker)
    try:
        df = pd.read_csv('../../../stored_data/{}.csv'.format(ticker))
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
        os.remove('../../../stored_data/{}.csv'.format(ticker))
        df3.to_csv('../../../stored_data/{}.csv'.format(ticker))





def nasdaq(num):
    '''Does everything necessary for collecting the s&p 500 stocks from nasdaq'''
    
    list_500 = save_sp500_tickers()
    start = num*125
    end = (num+1)*125
    for i in list_500[start:end]:#[start:end]:
        print(i)
        if is_worktime():
            add_to_existing_csv(i)




def initial_collect():
    '''Initializes collecting data using google intradata'''
    
    list_500 = save_sp500_tickers()

    for i in list_500:
        if not os.path.exists('../../../stored_data/{}.csv'.format(i)):
            collect_data(i)
        else:
            print('I got it')




def update_data_every_n_minutes(n,override = False):
    '''Updates data collection to happen every n minutes, currently only for the SP 500'''
    
    while True:
        tock = time.time()
        if is_worktime() or override:
            print('yaas')
            try:
                collect_sp500()
            except KeyboardInterrupt:
                print('Manual break by user')
                return
        print('sleepytime')
        tick=time.time()
        
        if override:
            break
        
        if tick-tock<n*60:
            time.sleep(n*60-(tick-tock))



            
def testing_rolling_averages(df,ticker):
    '''Does a similar job as testing_rolling_data but instead also returns the maxes for buying and selling'''
    
    max_total = 0
    max_buy = 0
    max_sell = 0
    rows = []
    for i in range(5,60,5):
        columns = []
        for j in range(5,60,5):
            if i>=j:
                columns.append(0)
                continue
            df1 = df
            df1 = add_rolling_average(df1,i)
            df1 = add_rolling_average(df1,j)
            thing = correct_returns(df1,i,j)
            
            if thing>max_total:
                max_total=thing
                max_buy=i
                max_sell=j
                
            columns.append(thing)
        rows.append(columns)

    fig=plt.figure(figsize=[20,10])
    plt.imshow(rows)
    plt.colorbar()
    plt.title(str(ticker))
    ax = plt.gca()
    ax.set_xticklabels(np.arange(-5,70,10))
    ax.set_xlabel('selling')
    ax.set_yticklabels(np.arange(-5,70,10))
    ax.set_ylabel('buying')
    #plt.show()
    if not os.path.exists('../../../Testing_inter/'):
        os.mkdir('../../../Testing_inter')
    fig.savefig('../../../Testing_inter/{}.png'.format(ticker),dpi=200,\
                bbox_inches='tight')
    plt.close()
    return max_buy,max_sell





def correct_returns(df,buying,selling):
    '''Modified form of check_rolling_returns for the above function'''
    
    buy_stock = []
    sell_stock = []
    sell_if_can=False
    sum_total = 0
    previous_row = df.iloc[0]
    
    for index,row in df.iterrows():
        
        Current_adj_close=row['Close']
        
        if row['{}ma'.format(selling)]<row['{}ma'.format(buying)] and \
        sell_if_can==False and previous_row['{}ma'.format(selling)]>\
        previous_row['{}ma'.format(buying)]:
            
            buy_stock.append(Current_adj_close)
            sell_if_can = True
            
        if sell_if_can==True and previous_row['{}ma'.format(selling)]<\
        previous_row['{}ma'.format(buying)] and row['{}ma'.format(selling)]>\
        row['{}ma'.format(buying)]:
            
            sell_stock.append(Current_adj_close)
            sell_if_can=False
            
        previous_row = row

    sell_stock.append(Current_adj_close)
    #print(len(sell_stock),len(buy_stock))
    for i in range(0,len(buy_stock)):
        
        sum_total+=sell_stock[i]-buy_stock[i]  
    
    return round(sum_total,3)




def optimal_settings():
    '''Takes the optimal settings from a previously made csv'''
    
    df = pd.read_csv('../../../Testing_inter/optimal_settings.csv')
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
        print('{} is not present in the optimal settings'.format(ticker))
        return False
    sell = settings[mask]['Sell'].values[0]

    '''Will look only at part of the data that is most relevant and add the 
    necessary rolling averages'''
    df = pd.read_csv('../../../stored_data/{}.csv'.format(ticker))
    window = df.iloc[-76*sell+15:]
    window = add_rolling_average(window,buy)
    window = add_rolling_average(window,sell)
    
    stuff = buy_or_sell(window,buy,sell)
    if stuff==None:
        pass
    elif stuff[0]=='buy':
        print('Buy {} at {}'.format(ticker,stuff[1]))
        pass
    elif stuff[0]=='sell':
        print('Sell {} at {}'.format(ticker,stuff[1]))
    #print(buy_or_sell(window,sell,buy))
    '''
    plt.plot(window.index,window['Close'],alpha=.6,color='k',label='Price')
    plt.plot(window.index,window['{}ma'.format(buy)],'b--',label='Buying')
    plt.plot(window.index,window['{}ma'.format(sell)],'r--',label='Selling')
    plt.legend(loc='upper left')'''

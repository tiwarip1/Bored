import os
import pandas as pd
import numpy as np
import matploblib.pyplot as plt
import datetime as dt
import requests
import time
import bs4 as bs

'''This is a main python file that stores all the important functions to be called by other scripts'''

def add_rolling_average(df,n):
    '''This is a general function that makes a rolling average over n
    data points'''
    
    df['{}ma'.format(n)]=df['Close'].rolling(window=n*12,min_periods=0).mean()
    return df





def testing_rolling_data(df,ticker):
    '''This goes over each item in stored data and uses rolling averages between 5 and 55 and finds how much profit would be made if a stock were bought or sold at those settings by calling check_rolling_returns'''
    
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
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*\
                                                      int(row[0])))
                rows.append(map(float, row[1:]))
    if len(rows):
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
    '''This function will add data to a database over time and does all the dirty work of collecting data and parsing everything to make it look nice and removing the unecessary stuff'''
    
    cont = True
    
    if not os.path.exists('../../stored_data/'):
        os.makedirs('../../stored_data/')
    
    if '{}.csv'.format(ticker) in os.listdir('../../stored_data/'):
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
        df.to_csv('../../stored_data/{}.csv'.format(ticker))
        cont = False
    
    df1 = pd.read_csv('../../stored_data/{}.csv'.format(ticker))
    try:
        df1 = df1[np.isfinite(df1['Close'])]
    except KeyError:
        pass
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
        os.remove('../../stored_data/{}.csv'.format(ticker))
        df3.to_csv('../../stored_data/{}.csv'.format(ticker))





def nasdaq_data(ticker = 'TSLA'):
    '''Takes the current stock price from NASDAQ and returns it as a dataframe'''
    
    session = requests.Session()
    url = 'https://www.nasdaq.com/symbol/{}/real-time'.format(ticker)
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
        if not os.path.exists('../../stored_data/{}.csv'.format(i)):
            collect_data(i)
        else:
            print('I got it')




def update_data_every_n_minutes(n):
    '''Updates data collection to happen every n minutes, currently only for the SP 500'''
    
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
    if not os.path.exists('../../Testing_inter/'):
        os.mkdir('../../Testing_inter')
    fig.savefig('../../Testing_inter/{}.png'.format(ticker),dpi=200,\
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

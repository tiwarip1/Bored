import pandas
import math

def updatecsv():
    stock='TSLA'
    files = 'stock_dfs/Unmodified/{}.csv'.format(stock)
    mod_files='stock_dfs/Modified/{}.csv'.format(stock)
    df = pandas.read_csv(files)
    df = df.convert_objects(convert_numeric=True)
    df['Close']=round(df['Close'],2)
    df['Low']=round(df['Low'],2)
    df['Open']=round(df['Open'],2)
    df['100da']=round(df['Adj Close'].rolling(window=100,min_periods=0).mean())
    df['40da']=round(df['Adj Close'].rolling(window=40,min_periods=0).mean())
    df['20da']=round(df['Adj Close'].rolling(window=20,min_periods=0).mean())
    df['Up or Down']=(df['Close']-df['Open'])/df['Open']
    df['Up or Down']=df['Up or Down']/abs(df['Up or Down'])
    df.to_csv(mod_files)
    df = pandas.read_csv(mod_files)
    print(df.head())
    
    
updatecsv()
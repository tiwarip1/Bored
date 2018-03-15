import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
    
def add_rolling_average(df,n):
    '''This is a general function that makes a rolling average over n
    data points'''
    
    df['{}ma'.format(n)]=df['Close'].rolling(window=n*12,min_periods=0).mean()
    return df

def testing_rolling_data(df,ticker):
    
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
        
    plt.imshow(rows)
    plt.colorbar()
    plt.title(str(ticker))
    ax = plt.gca()
    ax.set_xticklabels(np.arange(5,70,10))
    ax.set_xlabel('selling')
    ax.set_yticklabels(np.arange(5,70,10))
    ax.set_ylabel('buying')
    plt.show()
            
def check_rolling_returns(df,buying,selling):
    
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

def main():
    
    for file in os.listdir("../../stored_data/"):
        if file.endswith(".csv"):
            ticker = file[:file.find(".csv")]
            df = pd.read_csv('../../stored_data/{}.csv'.format(ticker))
            testing_rolling_data(df,ticker)
            #df = add_rolling_average(df,20)
            #df = add_rolling_average(df,40)
            #df = add_rolling_average(df,60)
            #df = add_rolling_average(df,80)
            #df = add_rolling_average(df,100)
            
rows = main()
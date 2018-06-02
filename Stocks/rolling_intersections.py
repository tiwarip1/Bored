import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

'''This program is meant to analyze stock data when rolling averages intersect
one another and find the most optimal one'''

def add_rolling_average(df,n):
    '''This is a general function that makes a rolling average over n
    data points'''
    
    df['{}ma'.format(n)]=df['Close'].rolling(window=n*12,min_periods=0).mean()
    return df

def testing_rolling_averages(df,ticker):
    
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

def main():
    
    optimal_settings = {'Ticker':[],'Buy':[],'Sell':[]}
    
    for file in os.listdir("../../stored_data/"):
        if file.endswith(".csv"):
            ticker = file[:file.find(".csv")]
            print(ticker)
            df = pd.read_csv('../../stored_data/{}.csv'.format(ticker))
            max_buy,max_sell = testing_rolling_averages(df,ticker)
            optimal_settings['Ticker'].append(ticker)
            optimal_settings['Buy'].append(max_buy)
            optimal_settings['Sell'].append(max_sell)
            print('Optimal settings are:',max_buy,max_sell)
            del max_buy
            del max_sell
            
    dfo = pd.DataFrame(data=optimal_settings)
    dfo.to_csv('../../Testing_inter/optimal_settings.csv')
        
main()    
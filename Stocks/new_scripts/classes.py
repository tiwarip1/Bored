import requests
import bs4 as bs

class transactions():
    '''
    This is a class which was made to generalize buying and selling stocks and
    includes any fees that would apply. This is to be used in a loop to 
    determine whether certain alerts are profitable in the end or not and 
    converts CAD to USD and vice versa if trading occurs in different 
    currencies
    '''
    
    def __init__(self,symbol='NFLX',convert=False,number_stocks=0):
        #Initializes varaibles to be used across class
        self.symbol=symbol
        self.convert=convert
        self.buying=[]
        self.selling=[]
        self.next_action='buy'
        self.number_stocks = number_stocks
        self.service_charge = 7
        self.override = False
        
    def buy(self,buy=0,number_stocks=None):
        #If the buying action is requested, the class will save the price        
        if self.next_action=='buy' or self.override:
            
            if number_stocks==None:
                number_stocks=self.number_stocks
            else:
                self.number_stocks=number_stocks+self.number_stocks
                
            if self.convert:
                buy = self.add_fees(buy)
            self.buying.append(buy*number_stocks+self.service_charge)
            self.next_action='sell'
            
        else:
            #Prevent selling twice
            print('problem with buying')
        
    def sell(self,sell=0,number_stocks = None):
        #If the selling action is requested, the class will save the price        
        if self.next_action=='sell' or self.override:
            
            if number_stocks==None:
                number_stocks=self.number_stocks
            else:
                self.number_stocks=-number_stocks+self.number_stocks
            
            if self.convert:
                sell = self.add_fees(sell)
            self.selling.append(sell*number_stocks-self.service_charge)
            self.next_action='buy'
            
        else:
            #Prevent buying twice
            print('problem with selling')
            
    def get_conversion_rate(self):
        #Gets a realtime conversion rate at market value
        resp=requests.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=CAD')
        soup = bs.BeautifulSoup(resp.text,'lxml')
        table = soup.find('span',{'class':'uccResultAmount'})
        self.conversion = float(str(table)[30:-7])
        self.cibc_conv = self.conversion+.05
            
    def add_fees(self,price):
        #Adds any fees that would come from making a transaction, buy or sell
        self.get_conversion_rate()
        if self.next_action=='buy':
            price=price-(price*self.conversion-price*self.cibc_conv)
        else:
            price=+price+(price*self.conversion-price*self.cibc_conv)
            
        return price
    
    def total(self):
        #Returns total profit
        return -sum(self.buying)+sum(self.selling)
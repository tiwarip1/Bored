

class transactions():
    
    def __init__(self,symbol='NFLX',convert=False,number_stocks=100):
        
        self.symbol=symbol
        self.convery=convert
        self.buying=[]
        self.selling=[]
        self.next_action='buy'
        self.number_stocks = number_stocks
        
    def buying(self,buy=0):
        
        if self.next_action=='buy':
            
            self.buying.append(buy)
            self.next_action='sell'
        else:
            print('problem with buying')
        
    def selling(self,sell=0):
        
        if self.next_action=='sell':
            self.selling.append(sell)
            self.next_action='buy'
        else:
            print('problem with selling')
            
    def add_fees(self):
        
        
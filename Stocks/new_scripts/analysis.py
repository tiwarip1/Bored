from classes import transactions

thing = transactions(symbol='MAXR',number_stocks=30,convert=False)
thing.buy(67.83)
thing.sell(67.25,20)
thing.override=True
thing.sell(69.97,10)
print(thing.total())
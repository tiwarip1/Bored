import pandas as pd
import matplotlib.pyplot as plt

from functions import bollinger,create_derivative,create_exponential_moving_average,add_rolling_average

df = pd.read_csv('../../../stored_data/TSLA.csv')

df = create_exponential_moving_average(df,window=20)
df = create_derivative(df,'20ema')
df = add_rolling_average(df,20,'dma','d20ema')

#print(df)

#plt.plot(df['20ema'])
plt.plot(df['d20ema'][-100:])
plt.plot(df['20dma'][-100:])

#ran = input("Over what range? ")

#bollinger(ran,True)
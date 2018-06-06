from keras.models import Sequential
from keras.layers import Dense,Dropout
import keras
import random
import numpy as np
import pandas

random.seed()

fields = ['Open','High','Low','Volume','Up or Down','100da','40da','20da']
dataset = pandas.read_csv('stock_dfs/Modified/MMM.csv',usecols = fields[:])

X=dataset.loc[:,['Open','High','Low','Volume','100da','40da','20da']]
Y=dataset.loc[:,'Up or Down']

#print(X.head(),Y.head())

#dataset = np.loadtxt('pima-indians-diabetes.csv',
       #              delimiter=',')

#X=dataset[:,0:8]
#Y=dataset[:,-1]

model = Sequential()

model.add(Dense(512,input_dim=7,activation = keras.layers.LeakyReLU(alpha=0.2)))
#model.add(Dropout(.1))
model.add(Dense(512,activation = keras.layers.LeakyReLU(alpha=0.2)))
#model.add(Dropout(.1))
model.add(Dense(128,activation = keras.layers.LeakyReLU(alpha=0.2)))
#model.add(Dropout(.2))
model.add(Dense(1,activation = 'sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X,Y,epochs=50,batch_size=128)

scores = model.evaluate(X,Y,verbose=0)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))
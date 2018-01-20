from keras.models import Sequential
from keras.layers import Dense,Dropout
import random
import pandas

random.seed()

fields = ['Open','High','Low','Volume','Up or Down','100da','40da','20da']
dataset = pandas.read_csv('stock_dfs/Modified/MMM.csv',usecols = fields[:])

X=dataset.loc[:,['Open','High','Low','Volume','100da','40da','20da']]
Y=dataset.loc[:,'Up or Down']

#print(X.head(),Y.head())

model = Sequential()

model.add(Dense(512,input_dim=7,activation = 'relu'))
#model.add(Dropout(.1))
model.add(Dense(512,activation = 'relu'))
#model.add(Dropout(.1))
model.add(Dense(128,activation = 'relu'))
#model.add(Dropout(.2))
model.add(Dense(1,activation = 'softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X,Y,epochs=100,batch_size=128)

scores = model.evaluate(X,Y,verbose=0)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))
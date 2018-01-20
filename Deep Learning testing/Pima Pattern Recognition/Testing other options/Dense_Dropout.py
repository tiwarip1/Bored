from keras.models import Sequential
from keras.layers import Dense,Dropout
import numpy as np
import random

random.seed()

dataset = np.loadtxt('pima-indians-diabetes.csv',
                     delimiter=',')

X=dataset[:,0:8]
Y=dataset[:,-1]

model = Sequential()

model.add(Dense(512,input_dim=8,activation = 'relu'))
model.add(Dropout(.2))
model.add(Dense(128,activation = 'relu'))
#model.add(Dropout(.2))
model.add(Dense(1,activation = 'sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])

model.fit(X,Y,epochs=1000,batch_size=10)

scores = model.evaluate(X,Y,verbose=0)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))

'''Resulted in 93.36% with 2 dropouts'''
'''Resulted in 95.05% with 1 dropout'''
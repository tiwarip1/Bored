from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import random

#Random seed such that when we do all the randomizing stuff, we can reproduce
#it and won't be accused of fudging with the data or connections
random.seed()

#Loading some input and output data
dataset = np.loadtxt('pima-indians-diabetes.csv',
                     delimiter=',')

#Inputs are the first 8 values and output is the last value
#In this case, there would be 8 input dimensions
X=dataset[:,0:8]
Y=dataset[:,-1]

#This initializes the model as a linear neural network, nothing fancy yet
model = Sequential()

#We add an input layer using the class Dense to say that it is fully connected
#to each of the inputs
#The first value in Dense is the number of neurons in the layer, while the
#second tells how many inputs to connect it each to, but since we want it to
#be fully connected, we say the full 8 dimensions. The third tells what type
#of activation function should be used
model.add(Dense(512,input_dim=8,activation = 'relu'))
model.add(Dense(128,activation = 'relu'))
model.add(Dense(1,activation = 'sigmoid'))

#We made 3 fully connected layers that ends with a normalized value between
# 1 and -1

#This compiles the model and uses a logarithmic loss function to evaluate the
#weights, an efficient optimizer for binary classification called adam and is
#asked to be accurate
model.compile(loss='binary_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])

#Puts in the input, then the training output, then the number of iterations and
#then batch_size, which I don't understand
model.fit(X,Y,epochs=1000,batch_size=10)

#This scores the output on how well it has done
scores = model.evaluate(X,Y,verbose=0)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))

'''Resulted in 99.61%'''
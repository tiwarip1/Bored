from keras.models import model_from_json
import numpy as np
import random
import time

tick=time.time()
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

#Loads from a JSON file
json_file=open('model.json','r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

#Load the weights
model.load_weights("model.h5")

model.compile(loss='binary_crossentropy',
                     optimizer='rmsprop',metrics=['accuracy'])

#The model and weights are loaded from the 150 epoch step and then sent for 
#another 150 interations to get better accuracy
model.fit(X,Y,epochs=1000,batch_size=10)

scores = model.evaluate(X,Y,verbose=0)

print("\n%s: %.2f%%" %(model.metrics_names[1],scores[1]*100))

#Creates a JSON file that will save the model itself
model_json = model.to_json()
with open("model.json","w")as json_file:
    json_file.write(model_json)
    
#Save the corresponding weights as a heirarchical data format (HDF5)
model.save_weights("model.h5")
print("This took ",round(time.time()-tick,2)," seconds to run")
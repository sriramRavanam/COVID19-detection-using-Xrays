# -*- coding: utf-8 -*-
"""xrayfinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MDwiPqZMgbtqLGEXOOGhPdVgQrH_-1Vt
"""

import zipfile
#!unrar x "/content/Final_data.rar" "/content/"

!unrar x "/content/drive/MyDrive/Final_data.rar" "/content/"

import tensorflow as tf
import numpy as np
from imutils import paths
import cv2
import random
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt



#to open and load images
pos_im_paths = list(paths.list_images("/content/Final_data/final_Positives"))
neg_im_paths = list(paths.list_images("/content/Final_data/final_Negatives"))

#add labels to data
data = []
labels = []

for imPath in pos_im_paths:
  image = cv2.imread(imPath)
  image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
  image = cv2.resize(image,(224,224))

  data.append(image)
  labels.append(1)

for imPath in neg_im_paths:
  image = cv2.imread(imPath)
  image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
  image = cv2.resize(image,(224,224))

  data.append(image)
  labels.append(0)


#shuffle labels and data together
temp = list(zip(data, labels)) 
random.shuffle(temp) 
data, labels = zip(*temp) 

data = np.array(data) / 255
labels = np.array(labels)


#HYPER Paramaters
INIT_LR = 1e-3
EPOCHS = 12
BS = 155

#some hyperparameters
LR = [1e-3 , 3e-3,3e-4,3e-2]
bs = [155,70]

#data split and data augmentation

(x_train, x_test, y_train, y_test) = train_test_split(data,labels,test_size = 0.20,stratify = labels)

#convert labels into one hot vectors
y_train_Ohot = tf.one_hot(y_train,2)
y_test_Ohot = tf.one_hot(y_test,2)

trainAug = tf.keras.preprocessing.image.ImageDataGenerator(
	rotation_range=15,
	fill_mode="nearest")


#creating model

base = tf.keras.applications.VGG16(weights="imagenet",include_top=False,input_tensor=Input(shape =(224,224,3)))

hmodel = base.output

hmodel = tf.keras.layers.AveragePooling2D(pool_size=(4,4),strides = 2)(hmodel)
hmodel = tf.keras.layers.Flatten(name = "flatten")(hmodel)
hmodel = tf.keras.layers.Dense(64,activation="relu")(hmodel)
hmodel = tf.keras.layers.Dropout(0.2)(hmodel)
hmodel = tf.keras.layers.Dense(16)(hmodel)
hmodel = tf.keras.layers.LeakyReLU()(hmodel)
hmodel = tf.keras.layers.Dense(2,activation = "softmax")(hmodel)

stack = Model(inputs = base.input , outputs = hmodel)


for layer in base.layers:
  layer.trainable = False


optimizer = tf.keras.optimizers.Adam(learning_rate=INIT_LR,decay=INIT_LR / EPOCHS)
stack.compile(loss = "binary_crossentropy",optimizer = optimizer,metrics = ["accuracy"])

H = stack.fit(
	trainAug.flow(x_train, y_train_Ohot), batch_size = BS,
	epochs=EPOCHS)

p,q = stack.evaluate(x_test,y_test_Ohot)

predictions = stack.predict(x_test,batch_size=BS) #h(x)

pred = np.argmax(predictions,axis=1)
ynp = np.array(y_test_Ohot)#y

stack.summary()

#hyperparameter testing, learning rate and batch size against accuracy and loss

class Results:
  def __init__(self,lr,bat,l,a):
    self.l=l
    self.a=a
    self.lr=lr
    self.bat=bat


#refitting the model with new hyperparameters
res = []
for i in LR:
  for j in bs:
    optimizer = tf.keras.optimizers.Adam(learning_rate=i,decay=i / EPOCHS)
    stack.compile(loss = "binary_crossentropy",optimizer = optimizer,metrics = ["accuracy"])
    stack.fit(
	trainAug.flow(x_train, y_train_Ohot), batch_size = j,
	epochs=EPOCHS)
    p,q = stack.evaluate(x_test,y_test_Ohot)
    res.append(Results(i,j,p,q))




#Writing into file

F = open("results.txt","w")

for R in range(len(res)):
  F.write(str(res[R].lr)+"\t"+str(res[R].bat)+"\t"+str(res[R].l)+"\t"+str(res[R].a)+"\n")
F.close()



#read from results.txt and store values in x_float

F = open("results.txt","r")
x = F.readlines()

x_float = []
for i in x:
  x_float.append(list(map(float,i.replace("\n","").split("\t"))))


#store values in lists

losses = []
bat_siz = []
lr_rate = []
accuracy = []

for i in x_float:
  losses.append(i[2])
  bat_siz.append(i[1])
  lr_rate.append(i[0])
  accuracy.append(i[3])


#loss vs batch_size

plt.plot(bat_siz,losses,"go",)
plt.axis([0,160,0,0.2])
plt.xlabel("batch_size")
plt.ylabel("loss")



#loss vs learning_rate

plt.plot(lr_rate,losses,"bo",)
plt.axis([0.00003,0.04,0,0.2])
plt.xlabel("learning_rate")
plt.ylabel("loss")


#accuracy vs batch_size

plt.plot(bat_siz,accuracy,"g^",)
plt.axis([0,160,0,1])
plt.xlabel("batch_size")
plt.ylabel("accuracy")

#accuracy vs learning_rate 

plt.plot(lr_rate,accuracy,"b^",)
plt.axis([0.00003,0.04,0,1])
plt.xlabel("learning_rate")
plt.ylabel("accuracy")


#plot Loss/Accuracy vs Epochs

N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.title("Training Loss and Accuracy on COVID-19 Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
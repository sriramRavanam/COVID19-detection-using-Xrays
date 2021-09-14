# Intro
The pandemic hit us at the end of 2019 and its effects have been devastating.
The virus has affected day to day life, as well as slowed down the global economy.
A couple hundered million cases have been reported and the number is slowly growing.

The covid19 virus mainly attatches itself to the healthy receptor cells in the lungs, through which it enters the body.
The infection may cause lungs to inflammate. Infected patients exhibit distinct radiographical visual characteristics along with fever, fatigue, dry cough,etc. 

The chest x-ray is one of the most effective non invasive methods to detect the virus.

during the summer of 2020, we decided to try to build a model to detect the virus using x-ray images of the patient.
At the time there was a lack of good datasets for chest x-rays for covid infected patients. Hence we had to work with what we found.

Our objective was to develop a model that could be embedded into an __automatic computer aided diagnostic__ system.

# Preprocessing
The dataset contained a few distinct types of x-rays, so our first job was to select all the x-ray images which were PA x-rays (Posterior-Anterior - front view). We collected the names of the pictures corresponding to PA x-rays and stored it in a text file. 
We wrote a batch script to read all images from that text file and copy them into another file.

Now that we had all the infected patients in a folder, we had to get healthy images in another folder. We accomplished this in the same way as before.

We load the images in a colab notebook and *Annotate* the images by assigning the corresponding labels.
Using the train_test_split function from the sklearn api, we split our dataset into a testing set and training set.

Another preprocessing step we perform is data augmentation. We use the keras.preprocessing api to generate augmented data.

# Model
The architecture used in our project is a very simple one.
We utilize the VGG16 model with pretrained weights as our base and we add some neural layers on top of this. These are the layers whose weights we train.
This method is a variation of __Transfer Learning__.
// NEED AN IMAGE HERE

So we mark the layers in the VGG16 model as _not trainable_ and then only train the remaining layers of the model on our data.
We train using the adam optimizer and calculate loss using the binary cross entropy function.

# Testing
We test using the evaluate function which is a part of keras. We test against the testing set of images and see the outcome.

# Learning Rate and Batch size
We used different learning rates and batch sizes to determine the best fit.
We need higher accuracy and low error rate.
// NEED ALL IMAGES RELATED TO THIS HERE.

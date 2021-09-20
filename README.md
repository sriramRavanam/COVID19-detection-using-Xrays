# COVID19-detection-using-Xrays
Covid 19 detection using X-ray images.

<img src="/result_images/xray_infected.jpg" width="200" height="200">


# Objective
Develop a model that can be embedded in an **Automatic Computer Aided Diagnosis** tool.

![ACAD](https://github.com/sriramRavanam/COVID19-detection-using-Xrays/blob/main/result_images/testing.jpg)

# Description
Train a model to distinguish between covid19 infected and healthy _PA chest x-rays_ (Posterior-Anterior).
//NEED IMAGE HERE - maybe one of the infected x-rays or an image of the virus

Uses Transfer Learning to train a quick model to do task effectively.

<img src="/result_images/VGG16.png" width="400" height="200">

# APIs used
1. Tensorflow
    1. Keras - build, train and test model.
2. SKLearn - split dataset and perform evaluation.
3. OpenCV - read and perform certain modifications to images.


# Results
After training, we obtain a model whose summary can be viewed here. 
https://github.com/sriramRavanam/COVID19-detection-using-Xrays/blob/main/model_summary.txt

# Outcomes
* Learnt about the different ways to _pre-process_ the data.
* Understood concepts about _gradient descent_ and _back propagation_.
* Learnt how to _structure_ a deep learning project.
* Learnt the method to _train and evaluate_ a model.

# Reason for selecting project
* It is a mini project for our Data Mining course.
* We wanted to do something relevant to our situation.

## Details. TLDR => we cleaned data, trained model and tested it. We checked the effect of different learning rates and batch sizes. 
The pandemic hit us at the end of 2019 and its effects have been devastating.
The virus has affected day to day life, as well as slowed down the global economy.
A couple hundered million cases have been reported and the number is slowly growing.

The covid19 virus mainly attatches itself to the healthy receptor cells in the lungs, through which it enters the body.
The infection may cause lungs to inflammate. Infected patients exhibit distinct radiographical visual characteristics along with fever, fatigue, dry cough,etc. 

The chest x-ray is one of the most effective non invasive methods to detect the virus.

during the summer of 2020, we decided to try to build a model to detect the virus using x-ray images of the patient.
At the time there was a lack of good datasets for chest x-rays for covid infected patients. Hence we had to work with what we found.

Our objective was to develop a model that could be embedded into an __automatic computer aided diagnostic__ system.

# Procedure
## Preprocessing
The dataset contained a few distinct types of x-rays, so our first job was to select all the x-ray images which were PA x-rays (Posterior-Anterior - front view). We collected the names of the pictures corresponding to PA x-rays and stored it in a text file. 
We wrote a batch script to read all images from that text file and copy them into another file.

Now that we had all the infected patients in a folder, we had to get healthy images in another folder. We accomplished this in the same way as before.

We load the images in a colab notebook and *Annotate* the images by assigning the corresponding labels.
Using the train_test_split function from the sklearn api, we split our dataset into a testing set and training set.

Another preprocessing step we perform is data augmentation. We use the keras.preprocessing api to generate augmented data.

## Model
The architecture used in our project is a very simple one.
We utilize the VGG16 model with pretrained weights as our base and we add some neural layers on top of this. These are the layers whose weights we train.
This method is a variation of __Transfer Learning__.

<img src="/result_images/VGG16 model v2.jpg">

So we mark the layers in the VGG16 model as _not trainable_ and then only train the remaining layers of the model on our data.
We train using the adam optimizer and calculate loss using the binary cross entropy function.

## Testing
We test using the evaluate function which is a part of keras. We test against the testing set of images and see the outcome.

## Learning Rate and Batch size
We used different learning rates and batch sizes to determine the best fit.
We need higher accuracy and low error rate.
<img src="/result_images/loss_vs_lr.jpg">      <img src="/result_images/loss_vs_batsiz.jpg">

<img src="/result_images/acc_vs_lr.jpg">      <img src="/result_images/acc_vs_batsiz.jpg">


Under the guidance of Dr. Vijaya Shetty, NMIT.

Sriram Ravanam, Vishnu LGC.

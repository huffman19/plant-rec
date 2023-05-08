import matplotlib.image as img
import matplotlib.pyplot as pyplot
import numpy as np
import math
from PIL import Image
import time

#global variables
num_filters = 2
filter_span = 3 #results in filter windows of size (3x3)
stride = 1
input_image_depth = 1
epochs = 4

#Reads in the image
def input(imageFile: str):
    return img.imread(imageFile)

#Perform convolution of filter values with imageArray
def forward(imageArray, filters):
    z_Array = np.zeros(((imageArray.shape[0])-(stride*2), (imageArray.shape[1])-(stride*2), input_image_depth, num_filters))
    
    #Fill output z_Array with convolved result of the input image and filters
     
    for i in range(z_Array.shape[0]):
            for j in range(z_Array.shape[1]):
                #dot product of filter and input section
                for k in range(num_filters):
                    z_Array[i,j] = np.sum(imageArray[i*stride:i*stride+filter_span, j*stride: j*stride+filter_span]*filters[:,:,:,k,0]+filters[:,:,:,k,1])
                    
    return z_Array

#will update filter values. TBD...
def backprop():
    return 0

def conv_layer(imageArray):
    #With mini-batch gradient decsent, a batch of inputs will forward pass through the convolutional layers 
    #After this batch forward pass, with backpropogation, the values or weights of the filters will be updated for optimization.
    #The initial filter values are randomized
    #For testing, there is only one input image currently 

    filters = np.random.rand(filter_span, filter_span, input_image_depth, num_filters,2)
    hidden_layer_output = forward(imageArray, filters)

    #update filters with backpropogation
    backprop() 

    return 0

#if __name__ == "__convolutional_layer__":

#to begin, obtain array of the image result of preprocessing
image_array = input('blurGreySunflower.jpg')
#Convolutional layer of CNN extracts features and reduces computation for the fully connected layer
conv_output = conv_layer(image_array)   

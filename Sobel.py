from tkinter import HORIZONTAL
import numpy as np
import scipy as sp;
import matplotlib.pyplot as plt;
from scipy import signal
from matplotlib.animation import FuncAnimation
from PIL import Image
from PIL import ImageFilter;
from PIL import ImageOps;
import cv2


def y_filter(image):
    print(image)

    #kernel to traverse y
    vertical_filter =   [[-1,-2,-1],
                        [0,0,0],
                        [1,2,1]]

    height, width = image.shape 
    

    #CREATING A NEW MATRIX OF SAME SHAPE AS THE ORIGINAL IMAGE, FILLED INSTEAD WITH ONLY 0S
    new_vertical_image = np.zeros_like(image)
    '''
    If this library cannot be used in the official implementation, some alternative ways of doing this have are shown below:

    new_image = [[0 for entry in range(col)] for entry in range(row)]
    new_vertical_image = [[0 for entry in range(col)] for entry in range(row)]
    print(new_image)
    for i in range(height):
        new_image[i] = [0 for element in range(width)]
    '''


    for i in range(3, height - 2):
        for j in range(3, width-2):

            local_pixels = image[i-1:i+2, j-1:j+2] #TODO find a way to remove the third entry
            #apply multiplication of respective indexes
            transformed_pixels = vertical_filter * local_pixels
            #this is normalizing the filter application: mapping to 0 or 1
            vertical_score = (transformed_pixels.sum() + 4)/8
            new_vertical_image[i][j] = vertical_score  #placing the result in the "middle" of the block
    
    return new_vertical_image

''' A version of the x-filter that works with RGB images (but does not work with greyscale) '''
def x_filter_3d(image):
    
    #kernel to traverse x
    horizontal_filter = [[-1,0,1],
                        [-2,0,2],
                        [-1,0,1]]

    height, width, depth = image.shape 
    

    new_horizontal_image = np.zeros_like(image)
 
    for i in range(1, height - 2):
        for j in range(1, width-2):
            local_pixels = image[i-1:i+2, j-1:j+2, 0]
            
            transformed_pixels = horizontal_filter * local_pixels
            horizontal_score = (transformed_pixels.sum() + 4)/8
            new_horizontal_image[i, j] = [horizontal_score] *3
    
    return new_horizontal_image

def x_filter(image):

    #kernel to traverse x
    horizontal_filter = [[-1,0,1],
                        [-2,0,2],
                        [-1,0,1]]    

    height, width = image.shape 
    

    new_image = [[0 for entry in range(col)] for entry in range(row)]

    new_horizontal_image = np.zeros_like(image)
    
 
    for i in range(1, height - 2):
        for j in range(1, width -2):
            local_pixels = image[i-1:i+2, j-1:j+2]
            
            transformed_pixels = horizontal_filter * local_pixels
            #mapping from 0 to 1
            horizontal_score = (transformed_pixels.sum() + 4)/8 #this is mapping the values from 0 to 1,
                                                                #since the maximum possible value is 4 and the
                                                                #minimum is -4.
            new_horizontal_image[i][j] = horizontal_score
    
    return new_horizontal_image



''' A version of the Sobel filter that works with RGB images (but does not work with greyscale) '''
def both_filters_RGB(image):
    
    #kernel to traverse x:
    horizontal_filter = [[-1,0,1],
                        [-2,0,2],
                        [-1,0,1]]

    #kernel to traverse y:
    vertical_filter =   [[-1,-2,-1],
                        [0,0,0],
                        [1,2,1]]

    height, width, depth = image.shape #height = columns, width = rows
    
    new_image = np.zeros_like(image)
    
    #TODO swap col and row later
    for i in range(1, height - 2):
        for j in range(1, width-2):
            local_pixels = image[i-1:i+2, j-1:j+2]
            
            horizontal_transformed_pixels = horizontal_filter * local_pixels
            horizontal_score = (horizontal_transformed_pixels.sum())/4

            vertical_transformed_pixels = vertical_filter * local_pixels
            vertical_score = (vertical_transformed_pixels.sum())/4

            edge_score = (vertical_score**2 + horizontal_score**2)**0.5
            new_image[i][j] = [edge_score]*3 #It is multiplied by 3 due to having three channels
    
    return new_image

''' This is the final version of the filter, which uses both the x filter and the y filter '''
def both_filters_greyscale1(image):

    #kernel to traverse x
    horizontal_filter = [[-1,0,1],
                        [-2,0,2],
                        [-1,0,1]]

    #kernel to traverse y
    vertical_filter =   [[-1,-2,-1],
                        [0,0,0],
                        [1,2,1]]

    height, width = image.shape
    
    new_image = np.zeros_like(image)
    
    for i in range(1, height - 2):
        for j in range(1, width-2):
            local_pixels = image[i-1:i+2, j-1:j+2]
            
            horizontal_transformed_pixels = horizontal_filter * local_pixels
            horizontal_score = (horizontal_transformed_pixels.sum())    #these values are not plot to 0-1 because otherwise 
                                                                        #the result becomes too dim.
        
            vertical_transformed_pixels = vertical_filter * local_pixels 
            vertical_score = (vertical_transformed_pixels.sum())
            
            edge_score = (vertical_score**2 + horizontal_score**2)**0.5
            new_image[i][j] = edge_score 
    
    return new_image


#Preprocessing the image:
original = cv2.imread("actualFlower.jpg")
im_gray = cv2.imread("actualFlower.jpg", cv2.IMREAD_GRAYSCALE)
im_gray = cv2.GaussianBlur(im_gray, (5,5), cv2.BORDER_DEFAULT)



sobel = both_filters_greyscale1(im_gray)

#final_img = x_filter(im_gray)

#Save the image to visualize it:
cv2.imwrite("./imageOutputs/finalImage.jpg", sobel)


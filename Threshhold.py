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



"""This replicates the binary thresholding from cv2"""
def threshold(image, threshValue):#image is in greyscale
    output = np.zeros_like(image)
    rows, columns =  output.shape

    for row in range(0, rows-1):
        for col in range(0, columns-1):
            if image[row][col] >= threshValue:
                output[row][col] = 255
                
            else:
                output[row][col] = 0

    return output

#NOTE: below is a function that I wrote to try to see if I could decrease the size of the shapes in the background. I don't think this will be useful.
def nonBinaryThreshold(image, threshValue1, threshValue2):#image is in greyscale
    output = np.zeros_like(image)
    rows, columns =  output.shape

    for row in range(0, rows-1):
        for col in range(0, columns-1):
            if image[row][col] >= threshValue1:
                output[row][col] = 255
            elif image[row][col] < threshValue1 and image[row][col] >= threshValue2:
                output[row][col] = 127
            else:
                output[row][col] = 0

    return output


"""This replicates the thresh to zero implementation of cv2"""
def threshToZero(image, thresh): 
    output = np.zeros_like(image)
    rows, columns =  output.shape

    for row in range(0, rows-1):
        for col in range(0, columns-1):
            if image[row][col] >= thresh:
               output[row][col] = image[row][col]
            
            if image[row][col] < thresh:
                output[row][col] = 0

    return output

#Below: some preprocessing
original = cv2.imread("actualFlower.jpg")
im_gray = cv2.imread("actualFlower.jpg", cv2.IMREAD_GRAYSCALE)
im_gray = cv2.GaussianBlur(im_gray, (5,5), cv2.BORDER_DEFAULT)

#Below: testing the functions I wrote:
out_img = threshToZero(im_gray, 127) # choosing a median value
#out_img = nonBinaryThreshold(im_gray, 170, 85)
#out_img = nonBinaryThreshold(im_gray, 150, 100)


"""Below: testing the outputs of some thresholding cv2 functions, to see if they match with ours:"""
#ret, thresh = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)
#ret, thresh = cv2.threshold(im_gray, 127, 255, cv2.THRESH_TOZERO)
#th3 = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
#ret, thresh = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)



cv2.imwrite("./imageOutputs/adaptive.jpg", out_img)
plt.show()
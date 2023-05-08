# -*- coding: utf-8 -*-
"""canny_joseph.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C-5kHEZVNqwUH_Ja9l3yxSmsAGpTHrdB
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/VIP\ APPS\ -\ Plant\ \(SP22\)/Canny Images

#load image
rawImage = plt.imread('iris.jpg')
plt.imshow(rawImage)

#greyscale code - Joseph Huang 1/20/23
row = len(rawImage)
col = len(rawImage[1])

redarray = np.zeros((row, col), np.dtype(np.uint8))  
greenarray = np.zeros((row, col), np.dtype(np.uint8))
bluearray = np.zeros((row, col), np.dtype(np.uint8))

for i in range(row):
    for j in range(col):        
        redarray[i][j] = rawImage[i][j][0]   
        greenarray[i][j] = rawImage[i][j][1]
        bluearray[i][j] = rawImage[i][j][2] 

grey = np.zeros((row, col), np.dtype(np.uint8)) 

#BT.709 Equation
grey = (0.183 * redarray) + (0.614 * greenarray) + (0.062 * bluearray)

plt.imshow(grey, cmap='gray')

def contrastValues(channel):
    
    # kwl 1/30/23
    # Function for determining "contrast" of image (ratio of highlights and shadows to midtones)
    
    highlights = (channel > 200).sum() # Counting number of pixels above 200 ("highlights")
    shadows = (channel < 100).sum() # Counting pixels below 100 ("shadows")
    midtones = (channel < 200).sum() - shadows # Counting values between
    
    highToMid = highlights / midtones # Ratio of highlights to midtones
    lowToMid = shadows / midtones # Ratio of shadows to midtones
    if highlights < shadows:
        extremes = highlights / shadows # Ratio of highlights to shadows; always should be <= 1
    else:
        extremes = shadows / highlights
        
    print(f"High to mid: {highToMid}")
    print(f"Shad to mid: {lowToMid}")
    print(f"High/Shad ratio: {extremes}")
    
    contrastIndex = highToMid * lowToMid * extremes # Unitless index of "how contrasting" the channel is
    
    print(contrastIndex)
    
    return(contrastIndex)


#Kaleb Lee 1/30/2023 - Test of picking color channel
redC = contrastValues(redarray)
greenC = contrastValues(greenarray)
blueC = contrastValues(bluearray)

# By default, we will simply use the red channel
if (blueC > greenC) and (blueC > greenC):
    channelIn = bluearray
elif (greenC > blueC) and (greenC > redC):
    channelIn = greenarray
else:
    channelIn = redarray

#gaussian filter code - Joseph Huang 1/20/23

gaussianWindow = (np.array([[1,2,1],[2,4,2],[1,2,1]]))/16
#gaussianWindow = (np.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]]))/273
#gaussianWindow = (np.array([[0,0,1,2,1,0,0],[0,3,13,22,13,3,0],[1,13,59,97,59,13,1],[2,22,97,159,97,22,2],[1,13,59,97,59,13,1],[0,3,13,22,13,3,0],[0,0,1,2,1,0,0]]))/1003
gaussian = signal.convolve2d(channelIn, gaussianWindow)  
plt.imshow(gaussian, cmap='gray')

#gradient calc. (Basically Sobel) - Joseph Huang 1/21/23

#Set dx and dy kernals 
dx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]]).astype(np.float64) 
dy = np.array([[-1,-2,-1],[0,0,0],[1,2,1]]).astype(np.float64)
 
gx = signal.convolve2d(gaussian,dx)  
gy = signal.convolve2d(gaussian,dy) 
sobel = np.sqrt(gx**2 + gy**2)
theta = np.arctan2(gy, gx)

plt.imshow(sobel,cmap='gray')

#non-maximum supression - Joseph Huang 1/23/23

#get shape of the image
rows, cols = sobel.shape

#start with array of zeros
thinned = np.zeros((rows,cols))

#theta is based on direction of gradient calcultion in sobel 
direction = theta * 180 / np.pi  #NOTE to self: direction is a numpy ndarray

#reference "https://www.statology.org/numpy-replace/" for this function
direction[direction < 0] += 180
direction[direction > 180] -= 180

#reference used to get hint on directions approach, noted in confluence
for i in range(rows - 1):
  for j in range(cols - 1):
   
    #NOTE to self: (0,0) is at top left corner of image. Make sure to check i and j additions for each case
    #direction is E and W
    #direction is between 0 and 22.5 because once it goes above 22.5, it would be facing the NE pixel or SW pixel.
    if (0 <= direction[i,j] <= 22.5):
      temp1 = sobel[i, j + 1]
      temp2 = sobel[i, j - 1]
                
    #direction is NE and SW
    #direction is between 22.5 and 67.5 because it would be facing the N pixel
    elif (22.5 < direction[i,j] <= 67.5):
      temp1 = sobel[i + 1, j - 1]
      temp2 = sobel[i - 1, j + 1]
                
    #direction is N and S
    #past 112.5 and it would be NW and SE
    elif (67.5 < direction[i,j] <= 112.5):
      temp1 = sobel[i + 1, j]
      temp2 = sobel[i - 1, j]

    #direction is NW and SE
    #past 157.5 would make direction E and W again
    elif (112.5 < direction[i,j] <= 157.5):
      temp1 = sobel[i - 1, j - 1]
      temp2 = sobel[i + 1, j + 1]

    #E and W again, values are restricted to be between 0 and 180 above
    elif (157.5 < direction[i,j] <= 180):
      temp1 = sobel[i, j + 1]
      temp2 = sobel[i, j - 1]

    #keep most intense pixel
    #If the sobel pixel is more intense the two around it, then keep the pixel
    #else make it 0
    if (sobel[i, j] >= temp1) and (sobel[i, j] >= temp2):
      thinned[i, j] = sobel[i, j]
    else:
      thinned[i, j] = 0

plt.imshow(thinned,cmap='gray')

#Double Thresholding - Joseph Huang 1/24/23

upperThresh = 230
lowerThresh = 100

row, col = thinned.shape
doubleThresh = np.zeros((row,col))

#find location of pixel that are stronger than the upper threshold 
strong_x, strong_y = np.where(thinned > upperThresh)

#find location of pixel that is between lower and uppper threshold
weak_x, weak_y = np.where((thinned <= upperThresh) & (thinned >= lowerThresh))
    
#set pixels which were above the upper threshold to 255
doubleThresh[strong_x, strong_y] = 255

#set pixels which are between the upper and lower threshold to 25 (indicating weak)
doubleThresh[weak_x, weak_y] = 25

plt.imshow(doubleThresh,cmap='gray')

#hysteresis thesholding - Joseph Huang 1/28/23
r, c = doubleThresh.shape  
for i in range(r - 1):
  for j in range(c - 1):
    if (doubleThresh[i , j] == 25):
      if (doubleThresh[i + 1, j - 1] == 255):
        doubleThresh[i, j] = 255
      elif (doubleThresh[i + 1, j] == 255):
        doubleThresh[i, j] = 255
      elif (doubleThresh[i + 1, j + 1] == 255):
        doubleThresh[i, j] = 255
      elif (doubleThresh[i, j - 1] == 255): 
        doubleThresh[i, j] = 255
      elif (doubleThresh[i, j + 1] == 255):
        doubleThresh[i, j] = 255
      elif (doubleThresh[i - 1, j - 1] == 255):
        doubleThresh[i, j] = 255
      elif (doubleThresh[i - 1, j] == 255): 
        doubleThresh[i, j] = 255
      elif (doubleThresh[i - 1, j + 1] == 255):
        doubleThresh[i, j] = 255
      else:
        doubleThresh[i, j] = 0

plt.imshow(doubleThresh,cmap='gray')
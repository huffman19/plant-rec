"""
Roberts Operator - First Attempt at choosing color channel | kwl S23 | 1/30/23
[ Based on Sobel operator code from F22 ]

> Note: This code is purely to create + test algorithm for choosing color channels.
        The Roberts operator will likely not be part of our final pipeline.
"""

import numpy as np
import cv2
import os
os.chdir('C:/Users/blu2s/OneDrive/Documents/VIP APPS/RobertEdgeDetection')

def roberts(image):
    print(image)
    
    # x- and y-masks
    Mx = [
        [1, 0],
        [0, -1]
        ]
    
    My = [
        [0, 1],
        [-1, 0]
        ]
    
    # Measuring image + creating new array
    imHeight, imWidth = image.shape
    newImage = np.zeros_like(image)
    
    # Iterating through image
    for i in range (1,imHeight - 1):
        for j in range (1,imWidth- 1):
            
            localWindow = image[i-1:i+1,j-1:j+1]
            
#            print(localWindow)
            
            # Gradient approximations
            GxArray = Mx * localWindow
            Gx = (GxArray.sum())
            GyArray = My * localWindow
            Gy = (GyArray.sum())
            
            # Calculating magnitude of vector
            vectorMag = ( Gx ** 2 + Gy ** 2) ** 0.5
            
            # First part of double thresholding
            if vectorMag >= 100:
                vectorMag = 255
            elif vectorMag >= 50:
                vectorMag = 100
            else:
                vectorMag = 0
            
            # Placing pixel in output image
            newImage[i][j] = vectorMag
            
    newImageOut = np.zeros_like(image)
    
    # Double thresholding for filtered image
    for i in range (1,imHeight - 1):
        for j in range (1, imHeight - 1):
            if newImage[i,j] == 255:
                newImageOut[i,j] = 255
            elif newImage[i,j] == 100:
                if ((newImage[i,j+1] == 255)
                    or (newImage[i,j-1] == 255)
                    or (newImage[i+1,j] == 255)
                    or (newImage[i-1,j] == 255)):
                    newImageOut[i,j] = 255
                else:
                    newImageOut[i,j] = 0
            
#    print(newImageOut)
    
    return newImage

def contrastValues(channel):
    
    # kwl 1/30/23
    # Function for determining "contrast" of image (ratio of highlights and shadows to midtones)
    # Ideally, plotted histogram should have a "bowl" shape - high extremes and low "dip" in the middle
    # matplotlib is apparently broken on this version of Spyder/Conda; will try plotting these later
    
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

imageIn = cv2.imread("bello.jpg")

# Splitting image into red, green, blue channels
imageR = imageIn[:,:,2]
imageG = imageIn[:,:,1]
imageB = imageIn[:,:,0]

redC = contrastValues(imageR)
greenC = contrastValues(imageG)
blueC = contrastValues(imageB)

# By default, we will simply use the red channel
if (blueC > greenC) and (blueC > greenC):
    channelIn = imageB
    print("\nUsed Blue\n")
elif (greenC > blueC) and (greenC > redC):
    channelIn = imageG
    print("\nUsed Green\n")
else:
    channelIn = imageR
    print("\nUsed Red\n")

#print(channelIn)

imageOut = roberts(channelIn)

cv2.imwrite("./robertOutputs/TheImportantOutput.jpg",imageOut)
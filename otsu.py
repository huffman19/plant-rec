"""
Otsu's Method - Attempt 1 | kwl S23 | 2/2/23
"""

import numpy as np
import cv2
import os
os.chdir('C:/Users/blu2s/OneDrive/Documents/VIP APPS/RobertEdgeDetection')

def otsu_threshold(image):
    
    # Calculating best threshold value using Otsu's
    
    # Initializing values as below 0; variance is a scalar and will not be negative
    # So if the value is below 0 we know we have not assigned a calculated value yet
    leastVar = -1
    leastVarThres = -1
    
    # Iterating through every value from 0 to 255 to determine which has least variance
    for threshold in range(0,255):
        
        # Determining "background" and "foreground" pixel values
        # Background pixels are all those below the threshold
        # Foreground are all above threshold
        bgpix = image[image <= threshold]
        fgpix = image[image >= threshold]
        
        # Pixel weight: % of pixels in image that are foreground/background pixels
        bgweight = len(bgpix) / len(image)
        # Using numpy var function as a quick way to calculate variance
        bgvar = np.var(bgpix)
        
        fgweight = len(fgpix) / len(image)
        fgvar = np.var(fgpix)
        
        classVar = (bgweight * bgvar) + (fgweight * fgvar)
        
        # Determining whether the new value just calculated is less than the previous least variance value
        if (classVar < leastVar) or (leastVar < 0):
            leastVar = classVar
            leastVarThres = threshold
        
        print(f"Current:\nThreshold: {leastVarThres}\nNow: {classVar}\nLowest: {leastVar}\n")
        
    return(leastVarThres)

def finalThreshold(image, thresValue):
    
    # Performing binary thresholding using value attained through Otsu's method
    
    imHeight, imWidth = image.shape
    newImage = np.zeros_like(image)
    
    # Iterating through image
    for i in range (1,imHeight - 1):
        for j in range (1,imWidth- 1):
            if image[i][j] > thresValue:
                newImage[i][j] = 1
                
    return(newImage)
     
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
           
imageIn = cv2.imread("bellf.jpg")

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

threshold = otsu_threshold(channelIn)

imageMask = finalThreshold(channelIn, threshold)

maskB = imageIn[:,:,0] * imageMask
maskG = imageIn[:,:,1] * imageMask
maskR = imageIn[:,:,2] * imageMask

imageOut = np.dstack((maskB,maskG,maskR))

cv2.imwrite("./robertOutputs/dandyOtsu.jpg",imageOut)
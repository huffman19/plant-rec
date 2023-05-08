# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import matplotlib.image as img
import matplotlib.pyplot as pyplot
import numpy as np
import math
from PIL import Image
import time

# Function inputs:
# imageFile: Name of Imagefile to be greyscaled
#
# output: 2D array
# Purpose: Convert a color image to black & white
# 9/18/2022 (ah)
def greyScale(imageFile:str):
    # initialize 3D array representation of Image
    # initialize numpy array of zeros for output
    image = img.imread(imageFile)
    arr = np.zeros((image.shape[0],image.shape[1]))

    # Sum of RGB values according to BT.709 at each pixel
    # Y = 0.2126R + 0.7152G + 0.0722B
    arr = image[:,:,0] * 0.2126 + image[:,:,1] *  0.7152 + image[:,:,2] * 0.0722
    
    return arr

# Function inputs:
# greyarr: a 2D numpy array representing the unscaled version of the image in greyscale
#
#output: 2D array that has been scaled down by 1/4
#Purpose: Covert a larger greyscale image to one that is 1/4 of the size by averaging groups of 4 cells
#9/22/2022 (nb)
def ImageRescale(greyarr):
    #find length and width of large grayscale array
    width = len(greyarr)
    height = len(greyarr[0])
    newarr = np.zeros((width // 2, height // 2)) #initialize small image array of zeros
    for i in range(0, width,2):
        for j in range(0, height,2):
            #average group of four pixels into one and send to small image
            newcell = (greyarr[i,j] + greyarr[i + 1,j] + greyarr[i,j + 1] + greyarr[i + 1,j + 1]) / 4
            newarr[i // 2, j // 2] = newcell
    return(newarr)

# Function inputs:
# imageArr: 2D np.array of an greyScaled image
# radius: radius of kernal
#
# output: 2D array
# Purpose: Blur an image using Gaussian distribution


# 9/18/2022 (ah)
def gaussianBlur(imageArr: np.array, radius: int):
    sigma = max(float(radius/2), 1)
    # Computes Kernal size from radius
    # EX: radius = 1 -> kernalSize = 3
    # 3x3 Kernal
    kernalSize = (2 * radius) + 1
    outputArr = np.zeros(imageArr.shape)
    #Initialize kernal
    kernal = np.zeros((kernalSize, kernalSize))
    sum = 0
    
    # Iterate through each element in kernal to determine value
    # Uses 2d gaussian function, center position is 0
    # x and y range from -radius to radius 
    # 'value' is the output from gaussian function at point (x,y)
    for x in range(-radius, radius+1):
        for y in range(-radius, radius+1):
            expNum = float(-(x*x + y*y))
            expDenom = (2 * sigma * sigma)
            
            expResult = math.exp(expNum / expDenom)
            value = (expResult / (2 * math.pi * sigma * sigma))
            kernal[x + radius][y + radius] = value
            sum += value
    
    #Normalized the kernal
    for x in range(kernalSize):
        for y in range(kernalSize):
            kernal[x][y] /= sum
            
    #TODO: blur edge pixels
    #This is where the new value for each pixel is calculated
    #Iterates over every pixel that allows for operation
    for x in range(radius, imageArr.shape[0] - radius):
        for y in range(radius, imageArr.shape[1] - radius):
            newValue = 0
            
            
            for kernalx in range(-radius, radius+1):
                for kernaly in range(-radius, radius+1):
                    kernalValue = kernal[kernalx + radius][kernaly + radius]
                    newValue += float(imageArr[x+kernalx][y+kernaly] * kernalValue)
            outputArr[x,y] = newValue
    
    return outputArr

    
if __name__ == "__main__":
 #   resizeImage("sunflower.jpg", 480, 480)
    greystart = time.time()
    imageArray = greyScale("sunflower.jpg")
    pyplot.imshow(imageArray, cmap ="gray")
    pyplot.show()
    rescaletime = time.time()
    rescaleimg = ImageRescale(imageArray)
    rescaleend = time.time()
    print(rescaleend - rescaletime)
    pyplot.imshow(rescaleimg, cmap = "gray")
    pyplot.show()
    grey = Image.fromarray(np.uint8(imageArray) , 'L')
    
    im1 = grey.save("greySunflower.jpg")
    blurstart = time.time()
    blurImageArray = gaussianBlur(imageArray,3)
    blur = Image.fromarray(np.uint8(blurImageArray) , 'L')
    im1 = blur.save("blurGreySunflower.jpg")
    print(blurstart - greystart)
    print(time.time() - blurstart)

        


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

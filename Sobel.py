import numpy as np
import math
import scipy
import scipy.signal
import os
import matplotlib.image as img
from matplotlib import pyplot as plt
from PIL import Image
#from Threshhold import *

def greyscale(image:np.ndarray):
    # initialize 3D array representation of Image
    # initialize numpy array of zeros for output
    arr = np.zeros((image.shape[0],image.shape[1]))
    # Sum of RGB values according to BT.709 at each pixel
    # Y = 0.2126R + 0.7152G + 0.0722B
    
    arr = image[:,:,0] * 0.2126 + image[:,:,1] *  0.7152 + image[:,:,2] * 0.0722
    return arr

#Bruna's function
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

def prewitt(image):

    #kernel to traverse x
    horizontal_filter = [[-1,0,1],
                        [-1,0,1],
                        [-1,0,1]]

    #kernel to traverse y
    vertical_filter =   [[-1,-1,-1],
                        [0,0,0],
                        [1,1,1]]

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

# 9/18/2022 (ah)
def gaussianBlur(imageArr: np.array, radius: int):
    sigma = 2#max(float(radius/2), 1)
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
    outputArr = scipy.signal.convolve(kernal, imageArr)
    
    
    return outputArr

def preprocess(image:np.ndarray, radius: int, thres: int):
    grey = greyscale(image)
    blur = gaussianBlur(grey, radius)
    sobel = both_filters_greyscale1(blur)
    thres = nonBinaryThreshold(sobel, 150, 50)
    # thres = threshold(sobel, thres)
    return thres

def convert_to_sobel(dirPath:str, destDir:str):
    
    for filename in os.listdir(dirPath):
        if filename.lower().endswith(".jpg"): 
            filepath = os.path.join(dirPath, filename)
            print('Converting %s...' % filepath)
            image = img.imread(filepath)
            processedImage = preprocess(image, 5, 40)
            im = Image.fromarray(processedImage)
            destPath = os.path.join(destDir, "sobel_"+filename)
            destPath.replace(".jpg", "jpeg")
            # im.save(destPath, format="JPEG")
            plt.imsave(destPath, processedImage, cmap="gray")
            
            # subprocess.run(["magick", "%s" % filename, "%s" % (filename[0:-5] + '.jpg')])
            continue
    
def get_image(filename: str):
    image = img.imread(filename)
    array = np.asarray(image)
    return array

def save_grey_image(filename: str, image: np.ndarray):
    im = Image.fromarray(image)
    im = im.convert("L")
    im.save(filename)
    
def save_color_image(filename: str, image: np.ndarray):
    im = Image.fromarray(image, mode="RGB")
    im.save(filename)

def process_all_colors(image):
    red = image[:,:,0]
    blue = image[:,:,1]
    green = image[:,:,2]
    
def get_y_hist(image: np.ndarray):
    hist = np.zeros(image.shape[0])
    for i in range(image.shape[0]):
        hist[i] = np.sum(image[i])
    return hist

def get_x_hist(image: np.ndarray):
    image = np.transpose(image)
    hist = np.zeros(image.shape[0])
    for i in range(image.shape[0]):
        hist[i] = np.sum(image[i])
    return hist

def threshold_seg(image: np.ndarray):
    mean = np.mean(image)
    img_list = image.reshape(image.shape[0]*image.shape[1])
    for i in range(len(img_list)):
        if img_list[i] > mean*1.25:
            img_list[i] = 255
        # elif img_list[i] > mean*.75:
        #     img_list[i] = mean*.5
        else:
            img_list[i] = 0
    result = img_list.reshape((image.shape[0],image.shape[1]))
    return result
        
# def mask_color(image: np.ndarray, mask: np.ndarray):
#     result = np.zeros(image.shape)
#     for i in range(image.shape[2]):
#         channel = image[:,:,i]
#         result[:,:,i] = np.multiply(mask,channel)
#     return result

def mask(image: np.ndarray, mask: np.ndarray):
    result = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i][j]:
                if len(image.shape) > 2:
                    for k in range(image.shape[2]):
                        result[i][j][k] = image[i][j][k]
                else:
                    result[i][j] = image[i][j]
    return result      

# def grey_to_color(image: np.ndarray):
#     color = np.zeros((image[0], image[1], 3))
#     for i in range(3):
#         color[:,:,i] = image
#     return color
if __name__ == "__main__":
    image = get_image("sample_images\\sun.jpg")
    grey = greyscale(image)
    thres = threshold_seg(grey)
    grey = greyscale(image)
    mask_img = mask(grey, thres)

    save_grey_image("mask_images\\sun_mask.jpg", mask_img)

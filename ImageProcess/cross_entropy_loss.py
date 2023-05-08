import matplotlib.image as img
import matplotlib.pyplot as pyplot
import numpy as np
import math
from PIL import Image
import time

#The cross entropy loss function is used in the process of back propogation to understand how well the model fits the data
def cross_entropy_loss(soft_max_results, classes, observed_value, M):
    cross_entropy_loss = 0
    #the cross entropy is calculated by summing across all possible classifications
    #the product of a binary indication of if that classification is the observed class and the natural log of the result of the soft max function for that class
    for i in range(0, M):
        cross_entropy_loss += (classes[i] == observed_value)*(np.log(soft_max_results[i][1]))
    return cross_entropy_loss

#Defininf some variables for testing purposes

#number of classes, M
M = 3
classes = ['A', 'B', 'C']
soft_max_results = [['A', 0.1],['B', 0.2],['C', 0.7]]
observed_value = 'C'

print(cross_entropy_loss(soft_max_results, classes, observed_value, M))
import numpy as np
from Sobel import get_image
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IoU import get_iou, get_iou_dict
import random

class Anchor():
    def __init__(self, width, height, x_center, y_center) -> None:
        self.w = width
        self.h = height
        self.x = x_center
        self.y = y_center
        
    def get_top_left(self):
        return (self.x - self.w // 2, self.y - self.h // 2)
    
    def get_bottom_right(self):
        return (self.x + self.w // 2, self.y + self.h // 2)
        

def get_anchor_centers(image: np.ndarray, grid_size=40):
    '''
    Gets the anchor centers to generate region proposals
    '''
    step = image.shape[0] // grid_size
    x_ctrs = np.arange(step, image.shape[0], step)
    y_ctrs = np.arange(step, image.shape[1], step)
    ctrs = np.zeros((len(x_ctrs) * len(y_ctrs), 2))
    idx = 0
    for x in x_ctrs:
        for y in y_ctrs:
            ctrs[idx][0] = x - (step // 2)
            ctrs[idx][1] = y - (step // 2)
            idx += 1        
    
    return ctrs

def get_anchors(scales: list[float], ratios: list[float], x_center: int, y_center: int, base_size: int = 32):
    '''
    Returns a list of anchor boxes around the same (x,y) center
    anchor: (width, height, x_center, y_center)
    '''
    anchor = np.array([base_size, base_size, 0, 0])
    dims = ratio_enum(anchor, ratios)
    arr = []
    for dim in dims:
        arr.append(scale_enum(dim, scales)) 
    arr = np.vstack(arr)
    arr[:,2] = x_center
    arr[:,3] = y_center
    
                
    return arr

def ratio_enum(anchor: np.array, ratios):
    '''
    Enumerate a set of anchors for each ratios.
    '''
    w, h, x, y = anchor
    size = w * h
    size_ratios = size / ratios
    ws = np.round(np.sqrt(size_ratios))
    hs = np.round(ws * ratios)
    dims = np.zeros((len(ratios), 4))
    dims[:,0] = ws
    dims[:,1] = hs
    return dims

def scale_enum(anchor, scales):
    """
    Enumerate a set of anchors for each scale.
    """

    w, h, x, y = anchor
    ws = w * scales
    hs = h * scales
    dims = np.zeros((len(scales), 4))
    dims[:,0] = ws
    dims[:,1] = hs
    return dims

def add_boxes_to_image(image, anchors):
    fig, ax = plt.subplots()
    ax.imshow(image)
    for i in range(len(anchors)):
        coord = (anchors[i][2] - anchors[i][0]//2,anchors[i][3] - anchors[i][1]//2)
        rect = patches.Rectangle(coord, anchors[i][0], anchors[i][1], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    rect = patches.Rectangle((70,41), 120, 155, linewidth=2, edgecolor='b', facecolor='none')
    ax.add_patch(rect)
    
    plt.show()
    
def add_dots(image, centers):
    fig, ax = plt.subplots()
    ax.imshow(image)
    for x, y in centers:
        circle = patches.Circle((x,y), 1, facecolor='red')
        ax.add_patch(circle)
    plt.show()

def temp(image, anchors, ground_truth, i):
    fig, ax = plt.subplots()
    ax.imshow(image)
    coord = (anchors[i][2] - anchors[i][0]//2,anchors[i][3] - anchors[i][1]//2)
    rect = patches.Rectangle(coord, anchors[i][0], anchors[i][1], linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    coord = (ground_truth[2] - ground_truth[0]//2, ground_truth[3] - ground_truth[1]//2)
    rect = patches.Rectangle(coord, ground_truth[0], ground_truth[1], linewidth=2, edgecolor='b', facecolor='none')
    ax.add_patch(rect)
    
    plt.show()
    
def get_all_anchors(centers, scales, ratios, image_dim, base_size=45):
    all_anchors = []
    for x, y in centers:
        anchors = np.ndarray.tolist(get_anchors(scales, ratios, x, y, 32))
        copy = anchors.copy()
        for i in range(len(anchors)):
            w, h, x_c, y_c = anchors[i]
            left = x_c - w//2
            right = x_c + w//2
            up = y_c - h//2
            down = y_c + h//2
            if left < 0 or right > image_dim[0] or up < 0 or down > image_dim[1]:
                copy.remove(anchors[i])
        all_anchors.extend(copy)
    return all_anchors

def get_positive_boxes(anchors, ground_truth):
    pos_anchors = []
    neg_anchors = []
    highest = ((0,0,0,0), 0)
    for anchor in anchors:
        iou = get_iou(anchor, ground_truth)
        if iou > 0.7:
            pos_anchors.append((anchor, iou))
        if iou < 0.3:
            neg_anchors.append((anchor, iou))
        if iou > highest[1]:
            highest = (anchor, iou)
    if len(pos_anchors) == 0:
        pos_anchors.append(highest)
    return pos_anchors, neg_anchors
                
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        arrLeft = arr[:mid].copy()
        arrRight = arr[mid:].copy()

        # Sort the two halves
        arrLeft = mergeSort(arrLeft)
        arrRight = mergeSort(arrRight)
        
        # Initial values for pointers that we use to keep track of where we are in each array
        i = j = k = 0
 
        # Until we reach the end of either start or end, pick larger among
        # elements start and end and place them in the correct position in the sorted array
        while i < len(arrLeft) and j < len(arrRight):
            if arrLeft[i][1] > arrRight[j][1]:
                arr[k] = arrLeft[i]
                i += 1
            else:
                arr[k] = arrRight[j]
                j += 1
            k += 1
 
        # When all elements are traversed in either arr1 or arr2,
        # pick up the remaining elements and put in sorted array
        while i < len(arrLeft):
            arr[k] = arrLeft[i]
            i += 1
            k += 1

        while j < len(arrRight):
            arr[k] = arrRight[j]
            j += 1
            k += 1
    return arr

def non_max_threshold(anchors: np.array, threshold: float=0.5):
    '''
    input: anchors -> list((anchor, iou))
    output: non_max -> list((anchor, iou))
    
    computes non-maximum thresholding on all anchors in anchors
    '''
    assert threshold < 1.0 and threshold > 0.0
    final_anchors = []
    anchors = mergeSort(anchors)
    while np.any(anchors):
        best = anchors[0]
        temp_anchors = anchors[1:]
        to_delete = []
        to_delete.append(0)
        for i in range(len(temp_anchors)):
            iou = get_iou(best[0], anchors[i][0])
            if iou > threshold:
                to_delete.append(i+1)
        final_anchors.append(best)
        anchors = np.delete(anchors, to_delete, 0)
        
    return final_anchors

def get_sample_neg(anchors, num_anchors):
    l = len(anchors)
    interval = l // num_anchors
    samples = []
    for i in range(num_anchors):
        idx = random.randint(i*interval, (i+1)*interval - 1)
        samples.append(anchors[idx])
    return samples

def iou_test():
    box1 = {}
    box1["x1"] = 70
    box1["x2"] = 190
    box1["y1"] = 41
    box1["y2"] = 196
    box2 = {}
    box2["x1"] = 233
    box2["x2"] = 255
    box2["y1"] = 206
    box2["y2"] = 255
    #print(get_iou(anchors[idx], ground_truth))
    print(get_iou_dict(box1, box2))


if __name__ == "__main__":    
    image = get_image("sample_images/dandi_test.jpg")
    ctrs = get_anchor_centers(image, 20)
    scales = np.array([1, 2, 4])
    ratios = np.array([0.5, 1, 2])
    anchors = np.ndarray.tolist(get_anchors(scales, ratios, 128, 128, 32))
    # image = Image.open("sample_images/dandi_test.jpg")
    # add_boxes_to_image(image, anchors)
    # add_dots(image, ctrs)
    idx = 5
    # bounding box for dandi_test.jpg
    ground_truth = (120, 155, 130, 118)
    
    #temp(image, anchors, idx)
    all_anchors = get_all_anchors(ctrs, scales, ratios, image.shape, 45)
    pos_anchors, neg_anchors = get_positive_boxes(all_anchors, ground_truth)
    samples = np.array(get_sample_neg(neg_anchors, 20))
    pos_anchors = np.array(pos_anchors)
    add_boxes_to_image(image, samples[:,0])
    add_boxes_to_image(image, pos_anchors[:,0])
    
    thres_anchors = np.array(non_max_threshold(pos_anchors, 0.5))
    add_boxes_to_image(image, thres_anchors[:,0])
    #temp(image, anchors, ground_truth, idx)
    

def get_iou_dict(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    
    bb1 & bb2 : {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is top left corner,
        the (x2, y2) position is bottom right corner

    Returns float between [0,1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # get intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    #if no intersection, return 0
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # get intersection area
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both boxes
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    #get iou by computing intersection of union area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    
    bb1 & bb2 : [w, h, x_center, y_center]
        w: width
        h: height

    Returns float between [0,1]
    """
    
    bb1_x1 = bb1[2] - bb1[0]//2
    bb1_x2 = bb1[2] + bb1[0]//2
    bb1_y1 = bb1[3] - bb1[1]//2
    bb1_y2 = bb1[3] + bb1[1]//2
    
    bb2_x1 = bb2[2] - bb2[0]//2
    bb2_x2 = bb2[2] + bb2[0]//2
    bb2_y1 = bb2[3] - bb2[1]//2
    bb2_y2 = bb2[3] + bb2[1]//2

    # get intersection rectangle
    x_left = max(bb1_x1, bb2_x1)
    y_top = max(bb1_y1, bb2_y1)
    x_right = min(bb1_x2, bb2_x2)
    y_bottom = min(bb1_y2, bb2_y2)

    #if no intersection, return 0
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # get intersection area
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both boxes
    bb1_area = (bb1_x2 - bb1_x1) * (bb1_y2 - bb1_y1)
    bb2_area = (bb2_x2 - bb2_x1) * (bb2_y2 - bb2_y1)

    #get iou by computing intersection of union area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou
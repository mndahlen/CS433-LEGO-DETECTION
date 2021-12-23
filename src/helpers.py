"""
Various helper functions used in the project. 
"""

import numpy as np
import cv2

def flip_horizontal(image):
    return np.flip(image, axis=1)

def add_noise(image, mean, sigma):
    gauss = np.abs(np.random.normal(mean,sigma,image.shape))
    noisy = np.uint8(image + gauss)
    return noisy

def blur(image, kernel_size = (5,5)):
    return cv2.blur(image, kernel_size)

def change_brigthness(image, factor):
    image = image*factor
    image[image > 255] = 255
    return np.uint8(image*factor)

def motion_blur(image, orientation, factor = 30):
    kernel_size = factor
    kernel_v = np.zeros((kernel_size, kernel_size))

    if orientation == "horizontal":
        kernel_h = np.copy(kernel_v)
        kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
        kernel_h /= kernel_size
        mb = cv2.filter2D(image, -1, kernel_h)
    elif orientation == "vertical":
        kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
        kernel_v /= kernel_size
        mb = cv2.filter2D(image, -1, kernel_v)
    else:
        print("Error! Must select blur orientation: \"vertical\" or \"horizontal\".")
        exit(1)
    return mb

def change_colour(img, colour):
    # Change colour of whole picture. Using HSV to only change the colour
    img_hsv = img.copy()
    colour_add = np.ones(np.shape(img))
    colour_add[:,:,:] = colour
    img_hsv[img_hsv > 0] = img_hsv[img_hsv > 0] + colour_add[img_hsv > 0]
    return img_hsv

def image_to_black_and_white(img):
    image = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    return image

def rotate(img, degree):
    (h, w) = img.shape[:2]
    (cX, cY) = (w//2, h//2)
    M = cv2.getRotationMatrix2D((cX, cY), degree, 1.0)
    return cv2.warpAffine(img, M, (w, h))

def num_to_namestring(num):
    if num < 10:
        return "000{}".format(num)
    
    if num < 100:
        return "00{}".format(num)
    
    if num < 1000:
        return "0{}".format(num)
    
    if num < 10000:
        return "{}".format(num)

def get_bbox(im):
    # Get bbox of image (We expect everything but lego to be black, i.e 0 intensity)
    im_1_channel = np.sum(im,2)
    im_find_x = np.sum(im_1_channel,0)
    im_find_y = np.sum(im_1_channel,1)

    x_low = 0
    x_high = im.shape[1]
    y_low = 0
    y_high = im.shape[0]

    idx = 0
    low_found = False
    for i in im_find_x:
        if not low_found:
            if i != 0:
                low_found = True
                x_low = idx
        else:
            if i == 0:
                x_high = idx
                break
        idx += 1

    idx = 0
    low_found = False
    for i in im_find_y:
        if not low_found:
            if i != 0:
                low_found = True
                y_low = idx
        else:
            if i == 0:
                y_high = idx
                break
        idx += 1

    return (x_low,y_low,x_high,y_high)

def get_bbox_center(bbox):
    # Expects bbox in format (x_low,y_low,x_high,y_high)   
    x_mid = (bbox[2] + bbox[0])/2
    y_mid = (bbox[3] + bbox[1])/2
    return (x_mid, y_mid)

def get_bbox_height_width(bbox):
    # Expects bbox in format (x_low,y_low,x_high,y_high)   
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return (height, width)


import numpy as np
import pandas as pd
import cv2
import os

# TODO Augmentations
# Motion blur
# Lens effects
# Research camera effects
# Change color
# Add shadow

def flip_horizontal(image):
    return np.flip(image, axis=1)

def add_noise(image, mean, sigma):
    gauss = np.abs(np.random.normal(mean,sigma,image.shape))
    noisy = np.uint8(image + gauss)
    return noisy

def gaussian_blur(image, kernel_size = (5,5), sigma=0):
    blur = cv2.GaussianBlur(image,kernel_size,sigma)
    return blur

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
        mb = cv2.filter2D(img, -1, kernel_h)
    elif orientation == "vertical":
        kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
        kernel_v /= kernel_size
        mb = cv2.filter2D(img, -1, kernel_v)
    else:
        print("Error! Must select blur orientation: \"vertical\" or \"horizontal\".")
        exit(1)
    return mb

# Change colour of whole picture. USing HSV to only change the colour
# Don't know how good it is, gets rather blurry around the edges
# For some reason it can't change back??
def change_colour(img, colour_add):
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    #print(img[100])
    img_hsv = img.copy()
    for row in range(img_hsv.shape[0]):
        for col in range(img_hsv.shape[1]):
            if (img_hsv[row][col].any() > 0):
                img_hsv[row][col] = (img_hsv[row][col] + colour_add)
               
    #print(img_hsv[100])
    #cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR_FULL, dst=img_hsv)
    return img_hsv

IMGDIR = "data/kaggle/3003"
img = cv2.imread(os.path.join(IMGDIR,"0001" + ".png"))
img_flipped = flip_horizontal(img)
img_noise = add_noise(img, 0, 30)
img_blur = gaussian_blur(img)
img_brighter = change_brigthness(img, 1.2)
img_colour = change_colour(img, [200, 50, 0])
img_mb = motion_blur(img, "vertical")

cv2.imshow("image",img_mb)
cv2.waitKey(0)
cv2.destroyAllWindows() 
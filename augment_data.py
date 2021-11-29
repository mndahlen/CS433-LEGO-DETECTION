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
    gauss = np.abs(np.random.normal(mean,sigma,img.shape))
    noisy = np.uint8(image + gauss)

    return noisy

def gaussian_blur(image, kernel_size = (5,5), sigma=0):
    blur = cv2.GaussianBlur(img,kernel_size,sigma)
    return blur

def change_brigthness(img, factor):
    img = img*factor
    img[img > 255] = 255
    return np.uint8(img*factor)


IMGDIR = "data/kaggle/3003"
img = cv2.imread(os.path.join(IMGDIR,"0001" + ".png"))
img_flipped = flip_horizontal(img)
img_noise = add_noise(img, 0, 30)
img_blur = gaussian_blur(img)
img_brighter = change_brigthness(img, 1.2)

img_combo = change_brigthness(gaussian_blur(add_noise(img, 0, 30)),0.8)
cv2.imshow("test",img_noise)
cv2.waitKey(0) 

#closing all open windows 
cv2.destroyAllWindows() 
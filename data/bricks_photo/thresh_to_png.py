import cv2
import numpy as np
import os

"""
This is a utility function to load a JPEG image, thresh pixel values to 0 and then convert to PNG. 
JPEG tends to make black pixels non black.
"""

T = 20

classes = ["2540","3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]
DATADIR = "data/raw_bricks"

if 0: # Don't run this is the bricks are no longer jpeg!
    for class_ in classes:
        class_idx = 0
        for filename in os.listdir(class_):
            if filename.endswith(".jpg"):
                class_idx += 1
                print(filename)

                im = cv2.imread(os.path.join(class_,filename))
                im[im < T] = 0                
                filename_png = class_ + "_" + str(class_idx) + ".png"
                cv2.imwrite(os.path.join(class_,filename_png),im)
else:
    print("please activate me if you really want to use me!")

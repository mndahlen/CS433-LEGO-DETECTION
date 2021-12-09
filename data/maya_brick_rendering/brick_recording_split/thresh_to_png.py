import cv2
import numpy as np
import os

T = 40

classes = ["2540","3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]

if 1: # Don't run this is the names are no longer weird!
    for class_ in classes:
        class_idx = 0
        for filename in os.listdir(class_):#os.path.join(DATADIR,class_)):
            if filename.endswith(".png"):
                class_idx += 1
                print(filename)

                im = cv2.imread(os.path.join(class_,filename))
                im[im < T] = 0                
                cv2.imwrite(os.path.join(class_,filename),im)
else:
    print("please activate me if you really want to use me!")
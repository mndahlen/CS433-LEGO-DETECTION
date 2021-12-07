import os
import cv2

if 0: # Don't runt this is the names are no longer weird!
    for filename in os.listdir("3022"):
        if filename.endswith(".png"):
            goodname = filename[-8:]
            os.rename("3022/" + filename,"3022/" +  goodname)
            continue
        else:
            continue

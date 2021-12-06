import cv2
import numpy as np
import pandas as pd
import os
import random

DATADIR = "data_generation"
BACKGROUNDIR = "backgrounds"
 

def num_to_namestring(num):
    if num < 10:
        return "000{}".format(num)
    
    if num < 100:
        return "00{}".format(num)
    
    if num < 1000:
        return "0{}".format(num)
    
    if num < 10000:
        return "{}".format(num)

background = cv2.imread(os.path.join(DATADIR,BACKGROUNDIR,"lena.png"))

composition = {"3003":5,"3004":1,"3022":0,"3023":1} # currently 0 for 3022 cuz filenames bad
max_index = 400

bboxes = pd.read_csv("data_generation/test/kaggle_bbox.csv")

lego_scale_factor = 0.2

for label in composition:
    for i in range(1,composition[label] + 1):
        rnd_index = random.randint(1, max_index)
        filename = num_to_namestring(rnd_index) + ".png"
        path = os.path.join(DATADIR,"kaggle",label,filename)
        bbox = bboxes.loc[(bboxes['filename'] == filename) & (bboxes['label'] == int(label))]
        img = cv2.imread(path)
        x_low = int(bbox["x_low"]*lego_scale_factor)
        y_low = int(bbox["y_low"]*lego_scale_factor)
        x_high = int(bbox["x_high"]*lego_scale_factor)
        y_high = int(bbox["y_high"]*lego_scale_factor)
        cv2.imshow("test",img)
        cv2.waitKey(0) 
cv2.destroyAllWindows() 



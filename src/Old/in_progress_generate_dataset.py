import cv2
import numpy as np
import pandas as pd
import os
import random
import csv

# Custom modules
import helpers as helper

# Directories
DATADIR_KAGGLE = "data/kaggle" 
BACKGROUNDIR = "backgrounds"
DIRS_KAGGLE = ["3003","3004","3022","3023"]
DATADIR_RAW = "data/raw_bricks"
DIRS_RAW = ["2540", "3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]
BACKDIR = "data/backgrounds"
WRITEDIR = "data/syntetic_dataset/images"
LABELCSV = "data/syntetic_dataset/labels/labels.csv"
FORMAT = ".jpeg"

# Size of images in the dataset
WIDTH = 600
HIGTH = 400

# Specifications for the dataset
NUM_IMAGES = 1000
MIN_PER_IMAGE = 0
MAX_PER_IMAGE = 50
BRICK_DISTRIBUTION = {"2540": 0, "3001":0, "3003":10, "3004":10, "3020":0, "3021":0, "3022":10, "3023":10, "3039":0, "3660":0}

# Ratio between kaggle and real
KAGGLE_RATIO = 10

# Path to bounding boxes
BBOX = pd.read_csv("data/test/kaggle_bbox.csv")

def write_to_file(image, filename):
    cv2.imwrite(os.path.join(WRITEDIR,filename), image)


    



images = ["3003", "3004", "3022", "3023"]
backgrounds = os.listdir(BACKDIR)
build_dataset(backgrounds, images, 1000)

#cv2.imshow("result", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows() 


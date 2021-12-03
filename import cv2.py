import cv2
import numpy as np
import pandas as pd
import os
import random
import generate_synthetic
import csv
## Program for generating dataset

# Directions for getting data
DATADIR = "data/kaggle" 
DIRS = ["3003","3004","3022","3023"]

WRITEDIR = "data/syntetic_dataset/images"
LABELCSV = "data/syntetic_dataset/labels/labels.csv"
FORMAT = ".jpeg"

def write_to_file(image, name, label_boxes):

    # Save the image to the correct place
    filename = name + FORMAT
    cv2.imwrite(os.path.join(WRITEDIR,filename), image)

    # Add in csv all labels and boxes in this image
    with open(LABELCSV, 'w', newline=' ') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')

        for box in label_boxes:
            writer.writerow(box)

def 
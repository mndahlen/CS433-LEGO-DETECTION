import cv2
import numpy as np
import pandas as pd
import os
import random
from generate_synthetic import num_to_namestring
import csv
import augment_data
## Program for generating dataset

# Directions for getting data
DATADIR = "data/kaggle" 
DIRS = ["3003","3004","3022","3023"]

WRITEDIR = "data/syntetic_dataset/images"
LABELCSV = "data/syntetic_dataset/labels/labels.csv"
FORMAT = ".jpeg"

# Size of images in the dataset
WIDTH = 600
HIGTH = 400

# Specifications for the dataset
MIN_PER_IMAGE = 0
MAX_PER_IMAGE = 10

# Path to bouding boxes
bboxes = pd.read_csv("data/test/kaggle_bbox.csv")


def write_to_file(image, name, label_boxes):

    # Save the image to the correct place
    filename = name + FORMAT
    cv2.imwrite(os.path.join(WRITEDIR,filename), image)

    # Add in csv all labels and boxes in this image
    with open(LABELCSV, 'w', newline=' ') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')

        for box in label_boxes:
            writer.writerow(box)

# Function for generation one image
def generate_image_from_list(background, images, colour="grey"):

    # Size of background
    back_width = background.shape[1]
    back_height = background.shape[0]
    max_index = 400

    # Percentage overlap in x- resp y- directions
    max_overlap = 0
    boxes = []
    for image in images:
            lego_scale_factor = random.uniform(0.2, 0.5)

            # Find random image of the specific piece
            rnd_index = random.randint(1, max_index)
            filename = num_to_namestring(rnd_index) + ".png"

            path = os.path.join(DATADIR,image,filename)

            bbox = bboxes.loc[(bboxes['filename'] == filename) & (bboxes['label'] == int(image))]
            img = cv2.imread(path)

            # Scale image
            width = int(img.shape[1] *lego_scale_factor)
            height = int(img.shape[0] *lego_scale_factor)
            dim = (width, height)

            # Augment lego piece
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            # Select colour from input. Either noo change, random colour or choose a colour
            if (colour == "random"):
                img = augment_data.change_colour(img, np.random.randint(0, 255, size=3))
            elif (colour == "grey"):
                print("grey")
            else:
                img = augment_data.change_colour(img, colour)


            #img = augment_data.add_noise(img, 0, 30)
            # Scale bounding boxes
            x_low = int(bbox["x_low"]*lego_scale_factor)
            y_low = int(bbox["y_low"]*lego_scale_factor)
            x_high = int(bbox["x_high"]*lego_scale_factor)
            y_high = int(bbox["y_high"]*lego_scale_factor)

            #boxes.append([label, x_low, y_low, x_high, y_high])
            # Make sure the whole box is within background (could change later if we want half pieces)
            # Note: offset for bounding box
            offset_x = np.random.randint(0, back_width - x_high)
            offset_y = np.random.randint(0, back_height - y_high)
            
            # Check that the offset is within boundaries
            overlap = False
            while(overlap):
                overlap = False
                for box in boxes:
                    box_offset_x = (box[3] + box[1])/2
                    box_offset_y = (box[4] + box[2])/2
                    box_size_x = box[3] - box[1]
                    box_size_y = box[4] - box[2]
                    size_x = x_high - x_low
                    size_y = y_high - y_low
                    if (((size_x + box_size_x)/2 - np.abs(box_offset_x - offset_x)) > max_overlap*min(size_x/2, box_size_x/2)):
                        overlap = True
                    elif (((size_y + box_size_y)/2 - np.abs(box_offset_y - offset_y)) > max_overlap*min(size_y/2, box_size_y/2)):
                        overlap = True
                if overlap == True:
                    offset_x = np.random.randint(0, back_width - x_high)
                    offset_y = np.random.randint(0, back_height - y_high)

            for col in range(offset_x, offset_x + x_high - x_low):
                for row in range(offset_y, offset_y + y_high - y_low):
                    # Remap to coordinates for a lego piece
                    img_col = col - offset_x + x_low
                    img_row = row - offset_y + y_low
                    if (img[img_row][img_col].any() > 0):        
                        background[row][col] = img[img_row][img_col]

            # Set the bounding box correctly in the background
            x_high = x_high + offset_x - x_low
            y_high = y_high + offset_y - y_low
            x_low = offset_x 
            y_low = offset_y
            boxes.append([image, x_low, y_low, x_high, y_high])
    return background, boxes


# List of backgrounds as strings
# List of images as strings
def build_dataset(backgrounds, back_format, images, img_format, size):

    # For each image we want to construct
    for i in range(size):
        
        # Pick a random background
        back = random.choice(backgrounds)

        # Select pieces at random for this image
        num_of_elements = random.randint(MIN_PER_IMAGE, MAX_PER_IMAGE)
        elements = random.choices(images, num_of_elements)



import cv2
import numpy as np
import pandas as pd
import os
import random
from generate_synthetic import BACKGROUNDIR, num_to_namestring
import csv
import augment_data
from generate_bbox_csv import get_bbox
## Program for generating dataset

# Directions for getting data
DATADIR_KAGGLE = "data/kaggle" 
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
MIN_PER_IMAGE = 0
MAX_PER_IMAGE = 50

# Ratio between kaggle and real
KAGGLE_RATIO = 10

# Path to bouding boxes
bboxes = pd.read_csv("data/test/kaggle_bbox.csv")


def write_to_file(image, filename):
    cv2.imwrite(os.path.join(WRITEDIR,filename), image)



# Function for generation one image
def generate_image_from_list(background_name, images, colour="grey", kaggle_ratio=KAGGLE_RATIO, bbx_gen="preprocess", noise_mean=0, noise_std=0, motion_blur_factor=0, motion_blur_dir="horizontal"):
    background = cv2.imread(os.path.join(BACKDIR,background_name))
    background = cv2.resize(background, (WIDTH, HIGTH), interpolation=cv2.INTER_AREA)
    back_width = WIDTH
    back_height = HIGTH
    max_index = 400

    # Percentage overlap in x- resp y- directions
    max_overlap = 0
    boxes = []
    for image in images:
            # Find random image of the specific piece
            take_kaggle = random.randint(0, kaggle_ratio)
     
            if(take_kaggle == 0):
                # Pick raw image
                colour = "grey"
                filename = random.choice(os.listdir(os.path.join(DATADIR_RAW,image)))
                # Unnice solution, will solve this better later
                while (filename == 'uncut'):
                    filename = random.choice(os.listdir(os.path.join(DATADIR_RAW,image)))
                
                path = os.path.join(DATADIR_RAW,image,filename)
            else:
                rnd_index = random.randint(1, max_index)
                filename = num_to_namestring(rnd_index) + ".png"
                path = os.path.join(DATADIR_KAGGLE,image,filename)

            img = cv2.imread(path)

            # Scale image. Want random between maybe 1/20 and 1/5 of image size? 
            lego_height = random.randint(int(HIGTH/15), int(HIGTH/5))
            lego_scale_factor = lego_height/img.shape[0]
            lego_width = int(lego_scale_factor*img.shape[1])

            dim = (lego_width, lego_height)

            # Augment lego piece
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            
            # Use preporcessed bounding boxes. Should be fastest, but we can not get arbitrary rotation
            if (bbx_gen=="preprocess"):
                bbox = bboxes.loc[(bboxes['filename'] == filename) & (bboxes['label'] == int(image))] 
                # Scale bounding boxes
                x_low = int(bbox["x_low"]*lego_scale_factor)
                y_low = int(bbox["y_low"]*lego_scale_factor)
                x_high = int(bbox["x_high"]*lego_scale_factor)
                y_high = int(bbox["y_high"]*lego_scale_factor)

            elif (bbx_gen=="rotate_image"):
                # Add choice for rotation
                degree = random.randint(0, 360)
                img = augment_data.rotate(img, degree)
                # Call bbox generation for getting the new bounding box for this rotation
                x_low, y_low, x_high, y_high = generate_bbox_csv.get_bbox(img)
            
            # Select colour from input. Either noo change, random colour or choose a colour
            if (colour == "random"):
                img = augment_data.change_colour(img, np.random.randint(0, 255, size=3))
            elif (colour == "grey"):
                print("grey")
            else:
                img = augment_data.change_colour(img, colour)


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
    
    # Always blur a little to remove lines between background and lego pieces
    background = augment_data.blur(background)

    # Add desired noise and motion blur
    background = augment_data.add_noise(background, noise_mean, noise_std)
    background = augment_data.motion_blur(background, motion_blur_dir, motion_blur_factor)

    return background, boxes


# List of backgrounds as strings
# List of images as strings
def build_dataset(backgrounds, images, size):
    label_boxes = pd.DataFrame(columns=["Image name", "Label", "X-low", "Y-low", "X-high", "Y-high"])
    for i in range(size):
        background = random.choice(backgrounds)
        num_of_elements = random.randint(MIN_PER_IMAGE, MAX_PER_IMAGE)
        elements = random.choices(images, k=num_of_elements)

            # Some randnoise_
        noise_mean = random.randint(-3, 3)
        noise_std = random.randint(0, 10)
        image, boxes = generate_image_from_list(background, elements, colour="grey")
        filename = str(i) + FORMAT
        write_to_file(image, filename)
        for box in boxes:
            label_boxes = label_boxes.append({"Image name":filename,"Label":box[0],
                                            "X-low":box[1],"Y-low":box[2],
                                            "X-high":box[3],"Y-high":box[4]}, ignore_index=True)

        if (i % 100 == 0):
            print("Image number: " + str(i) + " finished")
    label_boxes.to_csv(LABELCSV, index=False)
    



images = ["3003", "3004", "3022", "3023"]
backgrounds = os.listdir(BACKDIR)
build_dataset(backgrounds, images, 10)

#cv2.imshow("result", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows() 


#from _typeshed import NoneType

import cv2
import numpy as np
import pandas as pd
import os
import random
import csv
#import augment_data as augment_data
#import generate_brick_bbox as generate_brick_bbox
## Program for generating dataset

# Custom modules
import helpers as helper

# Directories
DATADIR_KAGGLE = "data/bricks_3D" 
BACKGROUNDIR = "data/backgrounds"
BACKGREYDIR = "data/greyish_background"
DIRS_KAGGLE = ["3003","3004","3022","3023"]
DATADIR_RAW = "data/bricks_photo"
DIRS_RAW = ["2540", "3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]
BACKDIR = "data/backgrounds"
WRITEDIR = "data/syntetic_data_v2/images"
LABELCSV = "data/syntetic_data_v2/labels/labels.csv"
FORMAT = ".jpeg"

# Size of images in the dataset
WIDTH = 600
HIGTH = 400

# Specifications for the dataset
MIN_PER_IMAGE = 1
MAX_PER_IMAGE = 50

# Ratio between kaggle and real
KAGGLE_RATIO = 10

# Path to bounding boxes
bbox = pd.read_csv("data/test/kaggle_bbox.csv")


def write_to_file(image, idx, boxes, label_boxes):
    filename = str(idx) + FORMAT
    cv2.imwrite(os.path.join(WRITEDIR,filename), image)
    for box in boxes:
        label_boxes = label_boxes.append({"Image name":filename,"Label":box[0],
                                        "X-low":box[1],"Y-low":box[2],
                                        "X-high":box[3],"Y-high":box[4]}, ignore_index=True)
    return label_boxes

# Function for generation one image
def generate_image_from_list(background, images, colour="grey", kaggle_ratio=KAGGLE_RATIO, bbx_gen="preprocess", noise_mean=0, noise_std=0, motion_blur_factor=1, motion_blur_dir="horizontal"):
    # Crop background to generate unique backgrounds for each image (to augment background)
    # Nvm this for now, think about it as a possible augmentation
    if False:
    #if (background.shape[0] > HIGTH and background.shape[1] > WIDTH):
        back_low_x = random.randint(0, background.shape[0] - HIGTH - 1)
        back_high_x = random.randint(back_low_x + HIGTH, background.shape[0]- 1)
        back_low_y = random.randint(0, background.shape[1] - WIDTH- 1)
        back_high_y = random.randint(back_low_y + WIDTH, background.shape[1]- 1)
        background = background[back_low_x:back_high_x][back_low_y:back_high_y] 
        print(back_low_x, back_low_y, back_high_x, back_high_y)
        print(background.shape)
    background = cv2.resize(background, (WIDTH,HIGTH), interpolation=cv2.INTER_AREA)
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
                #rnd_index = random.randint(1, max_index)
                #filename = helper.num_to_namestring(rnd_index) + ".png"
                #Pick random element from corresponding kaggle directory
                filename = random.choice(os.listdir(os.path.join(DATADIR_KAGGLE,image)))
                path = os.path.join(DATADIR_KAGGLE,image,filename)

            img = cv2.imread(path)
            if (type(img) == None):
                print(filename)
                print(image)
            # Scale image. Want random between maybe 1/20 and 1/5 of image size? 
            lego_height = random.randint(int(HIGTH/15), int(HIGTH/3))
            lego_scale_factor = lego_height/img.shape[0]
            lego_width = int(lego_scale_factor*img.shape[1])

            dim = (lego_width, lego_height)

            # Augment lego piece
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            
            # Use preporcessed bounding boxes. Should be fastest, but we can not get arbitrary rotation
            if (bbx_gen=="preprocess"):
                bbox = bbox.loc[(bbox['filename'] == filename) & (bbox['label'] == int(image))] 
                # Scale bounding boxes
                x_low = int(bbox["x_low"]*lego_scale_factor)
                y_low = int(bbox["y_low"]*lego_scale_factor)
                x_high = int(bbox["x_high"]*lego_scale_factor)
                y_high = int(bbox["y_high"]*lego_scale_factor)

            elif (bbx_gen=="rotate_image"):
                # Add choice for rotation
                degree = random.randint(0, 360)
                img = helper.rotate(img, degree)
                # Call bbox generation for getting the new bounding box for this rotation
                x_low, y_low, x_high, y_high = helper.get_bbox(img)
            elif (bbx_gen=="generic"):
                x_low, y_low, x_high, y_high = helper.get_bbox(img)
                
            # Select colour from input. Either noo change, random colour or choose a colour
            if (colour == "random"):
                img = helper.change_colour(img, np.random.randint(0, 255, size=3))
            elif (colour != "grey"):
                img = helper.change_colour(img, colour)

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
def build_random_dataset(backgrounds, backdir, images, size_random, label_boxes, idx=0, kaggle_ratio=10, noise=True, blur=True, motion=True, colour="random"):
     # Random images
    for i in range(size_random):
        background = random.choice(backgrounds)
        num_of_elements = random.randint(MIN_PER_IMAGE, MAX_PER_IMAGE)
        elements = random.choices(images, k=num_of_elements)

            # Some randnoise_
        noise_mean = random.randint(-2, 2)
        noise_std = random.randint(0, 5)
        motion_blur_dir = random.choice(["horizontal", "vertical"])
        motion_blur_factor = random.randint(6, 15)
        background = cv2.imread(os.path.join(backdir,background))
        image, boxes = generate_image_from_list(background, elements, colour=colour, kaggle_ratio=kaggle_ratio, bbx_gen="generic")
        # Add augmentation to image afterwards (like blur, noise etc)

        if blur:
            image = helper.blur(image, kernel_size=(5, 5))

        # Add desired noise and motion blur
        if noise:
            image = helper.add_noise(image, noise_mean, noise_std)
        if motion:
            image = helper.motion_blur(image, motion_blur_dir, motion_blur_factor)

        # Write image to file and add bounding boxes to the list
        label_boxes = write_to_file(image, idx, boxes, label_boxes)

        if (idx % 100 == 0):
            print("Image number: " + str(idx) + " finished")

        # Always increment index to get unique images
        idx += 1
    label_boxes.to_csv(LABELCSV, index=False)

    # To make more datasets we must return index
    return idx, label_boxes

# Just images of pieces on black background
def build_simple_dataset(images, size_simple, label_boxes, min_pieces=1, max_pieces=1, mix_pieces=False, idx=0, kaggle_ratio=10):
    piece_idx = 0
    background = np.zeros((WIDTH, HIGTH, 3), dtype = "uint8")
    for i in range(size_simple):
        num_of_pieces = random.randint(min_pieces, max_pieces)
        if (mix_pieces):
            elements = random.choices(images, k=num_of_pieces)
        else:
            elements = [images[piece_idx]]*num_of_pieces
            piece_idx = (piece_idx + 1)%len(images)
        # Generate images
        
        image, boxes = generate_image_from_list(background, elements, colour="grey", kaggle_ratio=kaggle_ratio, bbx_gen="rotate_image")

         # Write image to file and add bounding boxes to the list
        label_boxes = write_to_file(image, idx, boxes, label_boxes)

        if (i % 100 == 0):
            print("Simple image number: " + str(idx) + " finished")


        idx = idx + 1
    return idx, label_boxes


# Set up start conditions for generating dataset
idx = 0
label_boxes = pd.DataFrame(columns=["Image name", "Label", "X-low", "Y-low", "X-high", "Y-high"])
images = ["2540", "3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]
backgrounds = os.listdir(BACKDIR)
backgrounds_grey = os.listdir(BACKGREYDIR)

# Ten calls, so mult with that
size_per_call = 1000
# Call different functions for different type of images

# Images with black background and no blur or noise
idx, label_boxes = build_simple_dataset(images, size_per_call, label_boxes, idx=idx, min_pieces=10, max_pieces=10, kaggle_ratio=5)

# No noise or blurring
idx, label_boxes = build_random_dataset(backgrounds, BACKDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=False, blur=False, motion=False, colour="random")

# Only blur (to smooth edges but still have good quality images)
idx, label_boxes = build_random_dataset(backgrounds, BACKDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=False, blur=True, motion=False, colour="random")

# Motion blur instead
idx, label_boxes = build_random_dataset(backgrounds, BACKDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=False, blur=False, motion=True, colour="random")

# Images with random background and everything
idx, label_boxes = build_random_dataset(backgrounds, BACKDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5)

# Images with random background and everything, but no random colour
idx, label_boxes = build_random_dataset(backgrounds, BACKDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, colour="grey")


# Images with quite simple background and no noise or motion blur (or colour for kaggle)
idx, label_boxes = build_random_dataset(backgrounds_grey, BACKGREYDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=False, blur=False, motion=False, colour="grey")

# Images with quite simple background and no noise or motion blur, but now random colour
idx, label_boxes = build_random_dataset(backgrounds_grey, BACKGREYDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=False, blur=True, motion=False, colour="random")

# Images with quite simple background and noise, but now random colour
idx, label_boxes = build_random_dataset(backgrounds_grey, BACKGREYDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=True, blur=True, motion=False, colour="random")

idx, label_boxes = build_random_dataset(backgrounds_grey, BACKGREYDIR, images, size_per_call, label_boxes, idx=idx, kaggle_ratio=5, noise=True, blur=True, motion=True, colour="random")


# Finally write to csv file
label_boxes.to_csv(LABELCSV, index=False)

#cv2.imshow("result", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows() 


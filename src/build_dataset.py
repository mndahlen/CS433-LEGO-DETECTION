"""
Module with primary functions for building dataset:
    - build_dataset(): Iterates over chosen dataset size, generating dataset images (Backgrounds with brick cutouts).
    - generate_image_from_list():  Takes ONE background image and places brick cutouts on it.
    - write_to_file(): Saves image.
"""

import cv2
import pandas as pd
import numpy as np
import os
import random
from BrickPlacer import RandomBrickPlacer, UniformBrickPlacer
import helpers as helper

def generate_image_from_list(background, back_width, back_height, images, raw_piece_dir, synt_piece_dir, synt_ratio, colour="grey", rotation=0, placement_style="uniform"):
    # Fit to desired input size 
    background = cv2.resize(background, (back_width, back_height), interpolation=cv2.INTER_AREA)

    boxes = []

    # For uniform distribution of bricks
    if placement_style == "uniform":
        brick_place = UniformBrickPlacer(back_width, back_height, 5,5)
    elif placement_style == "random":
        brick_place = RandomBrickPlacer(back_width, back_height)

    for image in images:
            # Find random image of the specific piece
            take_synt = random.randint(0, synt_ratio)
     
            if(take_synt == 0):
                # Pick raw image. Alwas choose the colour of this image
                colour = "grey"
                filename = random.choice(os.listdir(os.path.join(raw_piece_dir,image)))
                # Make sure we dont get any other files in the directory
                while (not filename.endswith('.png')):
                    filename = random.choice(os.listdir(os.path.join(raw_piece_dir,image)))
                path = os.path.join(raw_piece_dir,image,filename)
            else:
                # Pick random element from corresponding synthetic image directory
                filename = random.choice(os.listdir(os.path.join(synt_piece_dir,image)))
                while (not filename.endswith('.png')):
                    filename = random.choice(os.listdir(os.path.join(synt_piece_dir,image)))   
                path = os.path.join(synt_piece_dir,image,filename)

            img = cv2.imread(path)
            # Augment pieces by rotation them. Either random or chosen rotation
            # (default zero)
            if (rotation=='random'):
                degree = random.randint(0, 360)
                img = helper.rotate(img, degree)
            else:
                img = helper.rotate(img, rotation)

            # Generate the bounding box for the piece in question
            x_low, y_low, x_high, y_high = helper.get_bbox(img)

            # Select colour from input. Either no change, random colour or choose a colour
            if (colour == "random"):
                img = helper.change_colour(img, np.random.randint(0, 255, size=3))
            elif (colour != "grey"):
                img = helper.change_colour(img, colour)

            # Crop image to only include the lego piece
            img = img[y_low:(y_high+1), x_low:(x_high+1)]

            # Scale image. Want random between maybe 1/10 and 1/5 of image size?
            min_im_size = min(back_width, back_height)
            des_lego_size = random.randint(int(min_im_size/10), int(min_im_size/5))

            # The largest dim of the lego brick should have this size
            lego_scale_factor = des_lego_size/max(img.shape[0], img.shape[1])
            im_height = int(img.shape[0]*lego_scale_factor)
            im_width = int(lego_scale_factor*img.shape[1])
            dim = (im_width, im_height)
            
            if (dim[0] == 0 or dim[1] == 0):
                print("WARNING: File {} with dimension {} is invalid: Skipping!".format(filename,dim))
                continue

            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            # Remap the bounding box to now include all of the image (since image is resized to only include piece)
            x_low =0
            x_high = img.shape[1]
            y_low = 0
            y_high = img.shape[0]

            # Call the brick placer to get a place for this brick
            (offset_x, offset_y) = brick_place.get_brick_placement(x_high, y_high)

            for col in range(offset_x, offset_x + x_high ):
                for row in range(offset_y, offset_y + y_high):
                    # Remap to coordinates for a lego piece
                    img_col = col - offset_x
                    img_row = row - offset_y 

                    if (img[img_row][img_col].max() > 0):       
                        if col < 600 and row < 400:
                            background[row][col] = img[img_row][img_col]

            # Set the bounding box correctly in the background
            x_high = x_high + offset_x - x_low
            y_high = y_high + offset_y - y_low
            x_low = offset_x 
            y_low = offset_y
            boxes.append([image, x_low, y_low, x_high, y_high])

    return background, boxes

def write_to_file(image, write_dir, idx, boxes, label_boxes):
    filename = str(idx) + '.jpeg'       # Set filename to index
    cv2.imwrite(os.path.join(write_dir,'images', filename), image)        # Write to desired directory
    for box in boxes:       # Append all bounding boxes to pandas dataframe to write it to csv
        label_boxes = label_boxes.append({"Image name":filename,"Label":box[0],
                                        "X-low":box[1],"Y-low":box[2],
                                        "X-high":box[3],"Y-high":box[4]}, ignore_index=True)
    return label_boxes          # The label-boxes will go on through the entire dataset

def build_dataset(backdir, images, synt_image_dir, raw_image_dir, size, write_dir, idx=0, 
                    synt_ratio=10, back_width=600, back_height=400, colour="grey", rotation=0,placement_style="uniform"):
    """
    List of backgrounds as strings
    List of images as strings
    """

    # List all images in backgrounds directory
    backgrounds = [back for back in os.listdir(backdir) if (back.endswith('.png') or back.endswith('jpeg') or back.endswith('jpg')) ]
    
    # Create dataframe for all bounding boxes
    label_boxes = pd.DataFrame(columns=["Image name", "Label", "X-low", "Y-low", "X-high", "Y-high"])
    
    # Make random images in all of the size
    for i in range(size):

        # Pick one background for this image
        background = random.choice(backgrounds)
        background = cv2.imread(os.path.join(backdir,background))

        # Generate one image
        image, boxes = generate_image_from_list(background, back_width, back_height, 
                                                images, raw_image_dir, synt_image_dir, synt_ratio, 
                                                colour, rotation,placement_style)

        # Write image to file and add bounding boxes to the list
        label_boxes = write_to_file(image, write_dir, idx, boxes, label_boxes)

        if (idx % 1 == 0):
            print("Image number: " + str(idx) + " finished")

        # Always increment index to get unique images
        idx += 1
    label_boxes.to_csv(os.path.join(write_dir, 'labels/labels.csv'), index=False)

    # To make more datasets we must return index
    return idx
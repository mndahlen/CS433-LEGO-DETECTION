# Function for generation one image
# Input: One background as openCV image (3 dim np array)
#        List of strings for piece names, example ['3003', '3004',]
#        width and height of desired output image (resizing background to this)
#        ratio of syntetic vs raw images
#        directories for synthetic and real images of bricks (should contain folders with same names as the piece names)

import cv2
import numpy as np
import os
import random
from UniformBrickPlacer import UniformBrickPlacer
import helpers as helper

def generate_image_from_list(background, back_width, back_height, images, raw_piece_dir, synt_piece_dir, synt_ratio, colour="grey", rotation=0):

    # Start by resizing background to fit desired output
    background = cv2.resize(background, (back_width, back_height), interpolation=cv2.INTER_AREA)

    boxes = []

    # Create a brickplacer for uniform distribution of bricks
    brick_place = UniformBrickPlacer(back_width, back_height, 5,5)

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
                #Pick random element from corresponding syntetic image directory
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
            
            # We can't have images with too small, because can resize. So check that they have dimension
            # Otherwise, just go with a new image
            # Also print the file to show where the problem is
            if (dim[0] == 0 or dim[1] == 0):
                print(filename)
                print(dim)
                continue

            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

            # Remap the bounding box to now include all of the image (since image is resized to only include piece)
            x_low =0
            x_high = img.shape[1]
            y_low = 0
            y_high = img.shape[0]

            # Call the brick placer to get a place for this brick
            (offset_x, offset_y) = brick_place.get_brick_placement(x_high, y_high)

            # Overwrite coordinates in background where the lego piece should be
            for col in range(offset_x, offset_x + x_high ):
                for row in range(offset_y, offset_y + y_high):
                    # Remap to coordinates for a lego piece
                    img_col = col - offset_x
                    img_row = row - offset_y 
                    if (img[img_row][img_col].max() > 0):       
                        background[row][col] = img[img_row][img_col]

            # Set the bounding box correctly in the background
            x_high = x_high + offset_x - x_low
            y_high = y_high + offset_y - y_low
            x_low = offset_x 
            y_low = offset_y
            boxes.append([image, x_low, y_low, x_high, y_high])
    return background, boxes
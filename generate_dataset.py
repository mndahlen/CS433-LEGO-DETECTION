import cv2
import numpy as np
import pandas as pd
import os
import random
from generate_synthetic import BACKGROUNDIR, num_to_namestring
import csv
import augment_data
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

    # Save the image to the correct place
    cv2.imwrite(os.path.join(WRITEDIR,filename), image)

    # Add in csv all labels and boxes in this image
   # with open(LABELCSV, 'w', newline='\n') as csvfile:
    #    writer = csv.writer(csvfile, delimiter=' ')

    #    for box in label_boxes:
    #        writer.writerow([filename, box])

# Function for generation one image
def generate_image_from_list(background_name, images, colour="grey"):

    # Fetch background
    background = cv2.imread(os.path.join(BACKDIR,background_name))
    # Resize background to 600*400
    background = cv2.resize(background, (WIDTH, HIGTH), interpolation=cv2.INTER_AREA)
    back_width = background.shape[1]
    back_height = background.shape[0]
    max_index = 400

    # Percentage overlap in x- resp y- directions
    max_overlap = 0
    boxes = []
    for image in images:
            #lego_scale_factor = random.uniform(0.2, 0.5)

            # Find random image of the specific piece
            take_kaggle = random.randint(0, KAGGLE_RATIO)
     
     
            if(take_kaggle == 0):
                # Pick raw image
                filename = random.choice(os.listdir(os.path.join(DATADIR_RAW,image)))
                # Unnice solution, will solve this better later
                while (filename == 'uncut'):
                    filename = random.choice(os.listdir(os.path.join(DATADIR_RAW,image)))
                
                path = os.path.join(DATADIR_RAW,image,filename)
            else:
                # Set colour for thses
                colour = "random"
                rnd_index = random.randint(1, max_index)

                # Strange name in these
                if(image == "3022"):
                    filename = "201706161906-" + num_to_namestring(rnd_index) + ".png"
                else:
                    filename = num_to_namestring(rnd_index) + ".png"

                path = os.path.join(DATADIR_KAGGLE,image,filename)

            bbox = bboxes.loc[(bboxes['filename'] == filename) & (bboxes['label'] == int(image))]
            #print(path)
            img = cv2.imread(path)

            # Scale image. Want random between maybe 1/20 and 1/5 of image size? 
            lego_height = random.randint(int(HIGTH/15), int(HIGTH/3))
            lego_scale_factor = lego_height/img.shape[0]
            lego_width = int(lego_scale_factor*img.shape[1])

            #width = int(img.shape[1] *lego_scale_factor)
            #height = int(img.shape[0] *lego_scale_factor)
            dim = (lego_width, lego_height)
            #print(dim)

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
    
    # Some augmentation on final image. 

    # Always blur a little to remove lines between background and lego pieces
    background = augment_data.blur(background)

    # Some randnoise_
    noise_mean = random.randint(-3, 3)
    noise_std = random.randint(0, 10)
    background = augment_data.add_noise(background, noise_mean, noise_std)

    return background, boxes


# List of backgrounds as strings
# List of images as strings
def build_dataset(backgrounds, images, size):
    label_boxes = pd.DataFrame(columns=["Image name", "Label", "X-low", "Y-low", "X-high", "Y-high"])
    # For each image we want to construct
    for i in range(size):
        
        # Pick a random background
        back = random.choice(backgrounds)

        # Select pieces at random for this image
        num_of_elements = random.randint(MIN_PER_IMAGE, MAX_PER_IMAGE)
        elements = random.choices(images, k=num_of_elements)

        image, boxes = generate_image_from_list(back, elements, colour="grey")
        filename = str(i) + FORMAT
        write_to_file(image, filename)
        for box in boxes:
            label_boxes = label_boxes.append({"Image name":filename,"Label":box[0],
                                            "X-low":box[1],"Y-low":box[2],
                                            "X-high":box[3],"Y-high":box[4]}, ignore_index=True)
        #cv2.imshow(image)

        if (i % 100 == 0):
            print("Image number: " + str(i) + " finished")
    # Save boxes
    #print(label_boxes)
    label_boxes.to_csv(LABELCSV, index=False)
    return
    
images = ["3003", "3004", "3022", "3023"]

#backgrounds = ["carpet", "grass", "legotechnic", "legotechnic2", "treefloor"]

# All images in background folder
backgrounds = os.listdir(BACKDIR)
build_dataset(backgrounds, images, 1000)
#background_name = random.choice(backgrounds)
#img, boxes = generate_image_from_list(background_name, images, colour="grey")

#cv2.imshow("result", img)
#cv2.waitKey(0)
#cv2.destroyAllWindows() 

import cv2
import numpy as np
import pandas as pd
import os
import random
import augment_data
DATADIR = "data"
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

background = cv2.imread(os.path.join(DATADIR,BACKGROUNDIR,"grass.jpeg"))
background = cv2.resize(background, (600, 400), interpolation=cv2.INTER_AREA)
back_width = background.shape[1]
back_height = background.shape[0]
composition = {"3003":1,"3004":2,"3022":0,"3023":10} # currently 0 for 3022 cuz filenames bad
max_index = 400

bboxes = pd.read_csv("data/test/kaggle_bbox.csv")
# All bounding boxes for one image, in the form (label, x_low, y_low, x_high, y_high)

# Function for generation one image
def generate_image(background, composition, colour="grey"):

    boxes = []
    for label in composition:
        for i in range(1,composition[label] + 1):
            lego_scale_factor = random.uniform(0.8, 1)
            rnd_index = random.randint(1, max_index)
            filename = num_to_namestring(rnd_index) + ".png"
            path = os.path.join(DATADIR,"kaggle",label,filename)
            bbox = bboxes.loc[(bboxes['filename'] == filename) & (bboxes['label'] == int(label))]
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
            boxes.append([label, x_low, y_low, x_high, y_high])
            #print(boxes)
            # Also draw bounding box for visualization
            #img = cv2.rectangle(img, (x_low, y_low), (x_high, y_high), (255, 0, 0), 2)
            #cv2.imshow("test",img)
            #cv2.waitKey(0) 
            #cv2.imshow("back", background)
            #cv2.waitKey(0) 
    background = augment_data.add_noise(background, 0, 5)
    background = augment_data.blur(background, (10, 10))

    return background, boxes


background, boxes = generate_image(background, composition, colour="random")
cv2.imshow("back", background)
cv2.waitKey(0) 
cv2.destroyAllWindows() 

show_img = background.copy()

for box in boxes:
    #print(box)
    show_img = cv2.rectangle(show_img, (int(box[1]), int(box[2])), (int(box[3]), int(box[4])), (255, 0, 0), 2)

cv2.imshow("With boxes", show_img)
cv2.waitKey(0) 
cv2.destroyAllWindows() 
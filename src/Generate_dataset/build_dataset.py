
import cv2
import pandas as pd
import os
import random
import generate_image_from_list as gen

# Helper for saving images and appending to list of boxes
def write_to_file(image, write_dir, idx, boxes, label_boxes):
    filename = str(idx) + '.jpeg'       # Set filename to index
    cv2.imwrite(os.path.join(write_dir,'images', filename), image)        # Write to desired directory
    for box in boxes:       # Append all bounding boxes to pandas dataframe to write it to csv
        label_boxes = label_boxes.append({"Image name":filename,"Label":box[0],
                                        "X-low":box[1],"Y-low":box[2],
                                        "X-high":box[3],"Y-high":box[4]}, ignore_index=True)
    return label_boxes          # The label-boxes will go on through the entire dataset


# List of backgrounds as strings
# List of images as strings
def build_dataset(backdir, images, synt_image_dir, raw_image_dir, size,
                    min_per_image, max_per_image, write_dir, idx=0, 
                    synt_ratio=10, back_width=600, back_height=400, colour="grey", rotation=0, show=False):
    # List all images in backgrounds directory
    backgrounds = [back for back in os.listdir(backdir) if (back.endswith('.png') or back.endswith('jpeg') or back.endswith('jpg')) ]

    # Create dataframe for all bounding boxes
    label_boxes = pd.DataFrame(columns=["Image name", "Label", "X-low", "Y-low", "X-high", "Y-high"])
    # Make random images in all of the size
    for i in range(size):

        # Pick one background for this image
        background = random.choice(backgrounds)
        background = cv2.imread(os.path.join(backdir,background))
        # Decide how many pieces in this image
        num_of_elements = random.randint(min_per_image, max_per_image)
        elements = random.choices(images, k=num_of_elements)    # Pick images at random

        # Generate one image
        image, boxes = gen.generate_image_from_list(background, back_width, back_height, 
                                                images, raw_image_dir, synt_image_dir, synt_ratio, 
                                                colour, rotation)

        # Show the image with bounding boxes
        if (show):
            show_im = image.copy()
            for box in boxes:
                show_im = cv2.rectangle(show_im, (box[1], box[2]), (box[3], box[4]), (255,0,0))

            cv2.imshow("result", show_im)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
        # Add augmentation to image afterwards (like blur, noise etc)

        # Write image to file and add bounding boxes to the list
        label_boxes = write_to_file(image, write_dir, idx, boxes, label_boxes)

        if (idx % 1 == 0):
            print("Image number: " + str(idx) + " finished")

        # Always increment index to get unique images
        idx += 1
    label_boxes.to_csv(os.path.join(write_dir, 'labels'), index=False)

    # To make more datasets we must return index
    return idx
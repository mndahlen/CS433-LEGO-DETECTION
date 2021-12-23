"""
Read images from a directory and augment using noise, blur, motion blur and grayscale conversion.
"""

import cv2
import os
import helpers as helper
import random

def augment_image(image, add_noise=False, add_blur=False, 
                    add_motion_blur=False, to_black_and_white=False, noise_mean=0, noise_std=0, 
                    blur_kernel=(1,1), motion_blur_dir="horisontal", motion_blur_factor=1):
    # Set up values if given as random (within limits)
    if (noise_mean == 'random'):
        noise_mean = random.randint(-2, 2)
    if (noise_std == 'random'):
        noise_std = random.randint(0, 5)
    if (blur_kernel == 'random'):
        blur_grade = random.randint(2, 6)
        blur_kernel=((blur_grade, blur_grade))
    if (motion_blur_dir == 'random'):
        motion_blur_dir = random.choice(["horizontal", "vertical"])
    if (motion_blur_factor == 'random'):
        motion_blur_factor = random.randint(2, 15)

    # Now add all desired augmentation
    if add_noise:
        image = helper.add_noise(image, noise_mean, noise_std)
    
    if add_blur:
        image = helper.blur(image, blur_kernel)

    if add_motion_blur:
        image = helper.motion_blur(image, motion_blur_dir, motion_blur_factor)

    if to_black_and_white:
        image = helper.image_to_black_and_white(image)
  
    return image

def augment_dataset(dir, add_noise=False, add_blur=False, 
                    add_motion_blur=False, to_black_and_white=False, noise_mean=0, noise_std=0, 
                    blur_kernel=(1,1), motion_blur_dir="horizontal", motion_blur_factor=1, overwrite=True):
    # Find all images in directory
    backgrounds = [back for back in os.listdir(os.path.join(dir, 'images')) if (back.endswith('.png') or back.endswith('jpeg') or back.endswith('jpg')) ]
    # Each image to be augmented
    for image_path in backgrounds:
        image = cv2.imread(os.path.join(dir, 'images', image_path))
        aug_img = augment_image(image, add_noise, add_blur, 
                    add_motion_blur, to_black_and_white, noise_mean, noise_std, 
                    blur_kernel, motion_blur_dir, motion_blur_factor)
        # Overwrite with the new image if we want that, otherwise append _1
        # Note: Must adapt other code to read bounding boxes from correct image in that case
        if overwrite:
            cv2.imwrite(os.path.join(dir, 'images', image_path), aug_img)
        else:
            cv2.imwrite(os.path.join(dir, 'images', 'aug_' + image_path), aug_img)
        
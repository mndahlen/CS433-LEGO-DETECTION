# Read images from a directory and augment each of them as desired
import cv2
import os
import augment_image as aug

def augment_dataset(dir, add_noise=False, add_blur=False, 
                    add_motion_blur=False, to_black_and_white=False, noise_mean=0, noise_std=0, 
                    blur_kernel=(1,1), motion_blur_dir="horizontal", motion_blur_factor=1, overwrite=True):
    # Find all images in directory
    backgrounds = [back for back in os.listdir(os.path.join(dir, 'images')) if (back.endswith('.png') or back.endswith('jpeg') or back.endswith('jpg')) ]
    # Each image to be augmented
    for image_path in backgrounds:
        image = cv2.imread(os.path.join(dir, 'images', image_path))
        aug_img = aug.augment_image(image, add_noise, add_blur, 
                    add_motion_blur, to_black_and_white, noise_mean, noise_std, 
                    blur_kernel, motion_blur_dir, motion_blur_factor)
        # Overwrite with the new image if we want that, otherwise append _1
        # Note: Must adapt other code to read bounding boxes from correct image in that case
        if overwrite:
            cv2.imwrite(os.path.join(dir, 'images', image_path), aug_img)
        else:
            cv2.imwrite(os.path.join(dir, 'images', 'aug_' + image_path), aug_img)
        
# File for augmenting one image using the functions in helpers
import random
import helpers as helper
import cv2
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
# Script for calling functions for generating and augmenting dataset

import build_dataset as build
import augment_dataset as augment
# Directories. Change here if images are in other directories
BACKGROUNDIR = "data/greyish_background"
DATADIR_SYNTHETIC = "data/bricks_3D" 
DATADIR_RAW = "data/bricks_photo"
PIECES = ["2540", "3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]

# Write directories. Change between making different datasets if you don't want to overwrite
WRITEDIR = "data/syntetic_data_v2"
LABELCSV = "data/syntetic_data_v2/labels/labels.csv"

# Size of images in the dataset
WIDTH = 600
HEIGHT = 400

# Specifications for the dataset
MIN_PER_IMAGE = 10
MAX_PER_IMAGE = 25
SYNTHETIC_RATIO = 10
SIZE = 10

# Generate a dataset
build.build_dataset(BACKGROUNDIR, PIECES, DATADIR_SYNTHETIC, DATADIR_RAW, SIZE, MIN_PER_IMAGE, MAX_PER_IMAGE, WRITEDIR, idx=0, synt_ratio=SYNTHETIC_RATIO, back_width=WIDTH, back_height=HEIGHT, colour="grey", rotation='random', show=False)

# Augment the constructed dataset
augment.augment_dataset(WRITEDIR, add_noise=False, add_blur=False, 
                    add_motion_blur=True, to_black_and_white=True, noise_mean=0, noise_std=0, 
                    blur_kernel=(3,3), motion_blur_dir="horizontal", motion_blur_factor=10, overwrite=False)
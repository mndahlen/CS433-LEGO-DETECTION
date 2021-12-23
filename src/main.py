"""
Main script for creating datasets.
Some parameters are more important than others:
- WIDTH: Width of images in dataset
- HEIGHT: Height of images in dataset
- SYNTHETIC_RATIO: Synthetic:real, the ratio of synthetic bricks to real bricks. 
                   Set this to a high value since the number of real brick cutouts are relatively few.
- SIZE: Number of images in dataset.
"""

import build_dataset as build
import augment_dataset as augment

# Select if you want to generate A, B or not.
GENERATE_A = True
GENERATE_B = True

# Directories for backgrounds and brick cutouts.
BACKGROUNDIR_GRAY = "data/backgrounds/gray"
BACKGROUNDIR_WILD = "data/backgrounds/wild"
DATADIR_SYNTHETIC = "data/bricks_3D" 
DATADIR_RAW = "data/bricks_photo"
PIECES = ["2540", "3001", "3003", "3004", "3020", "3021", "3022", "3023", "3039", "3660"]

# Write directories. Change between making different datasets if you don't want to overwrite
WRITEDIR_A = "data/datasets/A"
WRITEDIR_B = "data/datasets/B"

# Parameters
WIDTH = 600
HEIGHT = 400
SYNTHETIC_RATIO = 10
SIZE = 10

if GENERATE_A:
    # GENERATE
    build.build_dataset(BACKGROUNDIR_WILD, PIECES, DATADIR_SYNTHETIC, DATADIR_RAW, SIZE,
                        WRITEDIR_A, idx=0, synt_ratio=SYNTHETIC_RATIO, back_width=WIDTH, 
                        back_height=HEIGHT, colour="random", rotation='random',placement_style="random")

    # AUGMENT
    augment.augment_dataset(WRITEDIR_A, add_noise=True, add_blur=True, 
                            add_motion_blur=True, to_black_and_white=False, noise_mean=0, noise_std=0.1, 
                            blur_kernel=(1,1), motion_blur_dir="horizontal", motion_blur_factor=3, overwrite=True)

if GENERATE_B:
    # GENERATE
    build.build_dataset(BACKGROUNDIR_GRAY, PIECES, DATADIR_SYNTHETIC, DATADIR_RAW, SIZE, 
                        WRITEDIR_B, idx=0, synt_ratio=SYNTHETIC_RATIO, back_width=WIDTH, 
                        back_height=HEIGHT, colour="grey", rotation='random',placement_style="uniform")

    # AUGMENT
    augment.augment_dataset(WRITEDIR_B, add_noise=False, add_blur=False, 
                            add_motion_blur=True, to_black_and_white=True, noise_mean=0, noise_std=0, 
                            blur_kernel=(1,1), motion_blur_dir="horizontal", motion_blur_factor=10, overwrite=True)
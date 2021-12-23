"""
Inits directories for datasets. This is mainly for use in the readme demo!
"""

import os

A_MAIN = "data/datasets/A"
A_YOLO_MAIN = "data/datasets/A_YOLO"

B_MAIN = "data/datasets/B"
B_YOLO_MAIN = "data/datasets/B_YOLO"

# Create directory for datasets
if not os.path.exists(A_MAIN):
    os.makedirs(A_MAIN)
    os.makedirs(A_MAIN + "/images")
    os.makedirs(A_MAIN + "/labels")

if not os.path.exists(B_MAIN):
    os.makedirs(B_MAIN)
    os.makedirs(B_MAIN + "/images")
    os.makedirs(B_MAIN + "/labels")

if not os.path.exists(A_YOLO_MAIN):
    os.makedirs(A_YOLO_MAIN)
    os.makedirs(A_YOLO_MAIN + "/images")
    os.makedirs(A_YOLO_MAIN + "/labels")
    os.makedirs(A_YOLO_MAIN + "/images/train")
    os.makedirs(A_YOLO_MAIN + "/images/val")
    os.makedirs(A_YOLO_MAIN + "/images/test")
    os.makedirs(A_YOLO_MAIN + "/labels/train")
    os.makedirs(A_YOLO_MAIN + "/labels/val")
    os.makedirs(A_YOLO_MAIN + "/labels/test")
    os.makedirs(A_YOLO_MAIN + "/labels/all")

if not os.path.exists(B_YOLO_MAIN):
    os.makedirs(B_YOLO_MAIN)
    os.makedirs(B_YOLO_MAIN + "/images")
    os.makedirs(B_YOLO_MAIN + "/labels")
    os.makedirs(B_YOLO_MAIN + "/images/train")
    os.makedirs(B_YOLO_MAIN + "/images/val")
    os.makedirs(B_YOLO_MAIN + "/images/test")
    os.makedirs(B_YOLO_MAIN + "/labels/train")
    os.makedirs(B_YOLO_MAIN + "/labels/val")
    os.makedirs(B_YOLO_MAIN + "/labels/test")
    os.makedirs(B_YOLO_MAIN + "/labels/all")

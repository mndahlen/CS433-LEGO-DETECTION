# Detection and classification of Lego bricks in a pile of Legos

## Introduction
This project was the final course-project in CS-433 at EPFL. For details of the project you are referred to the report which is available in docs/. The main focus of the project was to generate data for training YOLOv5s for detection of lego bricks. Brick types were restricted to: *2540, 3001, 3003, 3004, 3020, 3021, 3022, 3023, 3039, 3660*. As a result two main datasets were generated: 

- **Set A**: Many colors, bricks randomly placed on background.
- **Set B**: Grayscale, bricks uniformly placed on background.

**Detecting bricks in a sparse setting using YOLO trained on Set A**

<img src="docs/figures/set_A_sparse.jpg" width="600">

\
**Detecting bricks in a tight setting using YOLO trained on Set B**

<img src="docs/figures/set_B_benchmark.jpg" width="600">



## How to run
Navigate to the parent directory of this repository.

Then run:

```
python3 src/main.py
```

This will generate 10 images of Set_A and Set_B as explained in the report. Configure the main.py script to generate more than 10 images. Note that you have to convert the dataset to a format usable for YOLO before, scripts for this is available in data/datasets/YOLO, however these will need to be modified and you will have to create directories to make it work.

## Repository explanation
### src
Contains scripts for running main.py for generation of data: 
- **main.py**: Main script to generate datasets. Should be configured before use.
- **helpers.py**: Helper functions for image manipulation such as augmentation. Also helpers for calculating bounding-boxes.
- **build_dataset.py**: Primary module used by main.py to generate datset.
- **BrickPlacer.py**: Module with two classes (UniformBrickPlacer and RandomBrickPlacer) to calculate placement of brick on background. Used in build_dataset.py
- **augment_dataset.py**: Module with functions for augmenting final dataset after creation. Is used in main.py

### data
- **/backgrounds**: Backgrounds to be used for generating dataset. Brick cutouts will be pasted on the backgrounds.
- **/bricks_3D**: Brick cutouts from rendered images of Lego bricks.
- **/bricks_photo**: Brick cutouts from real images of Legos.
- **/datasets**: Datasets generated with the dataset generator have been placed here. Also contains scripts for converting dataset to YOLO format.
- **/maya_brick_rendering**: Taken from Kaggle Lego repository (https://www.kaggle.com/joosthazelzet/lego-brick-images). 

### models
- **set_A.pt**: YOLOv5s trained on Set A.
- **set_B.pt**: YOLOv5s trained on Set B.


### docs
Contains figures for report and this readme. Also contains report.pdf.

## Sources
https://www.kaggle.com/joosthazelzet/lego-brick-images

And more cited in report.

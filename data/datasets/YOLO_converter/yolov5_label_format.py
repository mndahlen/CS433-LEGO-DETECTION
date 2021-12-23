"""
This model converts our generated dataset to YOLO format.
"""

import pandas as pd
import numpy as np

LABELDIR = 'data/datasets/A/labels/labels.csv'
SAVELABELDIR = 'data/datasets/A_YOLO/labels/all/'

def create_txt_annotations():
	labels = pd.read_csv(LABELDIR)

	# Yolov5 needs .txt file for each image with one line per bounding box
	# Each line must be in the following format: [category integer 0 indexed] x_center y_center width height
	labels['x_center'] = (labels['X-high'] + labels['X-low']) / (2 * 600)
	labels['y_center'] = (labels['Y-high'] + labels['Y-low']) / (2 * 400)
	labels['width'] = (labels['X-high'] - labels['X-low']) / 600
	labels['height'] = (labels['Y-high'] - labels['Y-low']) / 400

	unique_labels = np.unique(labels.Label)
	for i, label in enumerate(unique_labels):
		labels.Label = labels.Label.apply(lambda x: i if x == label else x)

	entries = ['Label', 'x_center', 'y_center', 'width', 'height']
	for image_name in np.unique(labels['Image name']):
		img_df = labels[labels['Image name'] == image_name][entries]
		np.savetxt('{}{}.txt'.format(SAVELABELDIR,image_name.replace('.jpeg', '')), img_df.values, fmt=['%d', '%f', '%f', '%f', '%f'])

create_txt_annotations()

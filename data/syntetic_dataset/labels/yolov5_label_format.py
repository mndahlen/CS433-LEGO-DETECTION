import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def create_txt_annotations():
	labels = pd.read_csv('data/syntetic_dataset/labels/labels.csv')

	# yolov5 needs .txt file for each image with one line per bounding box
	# each line must be in the following format: [category integer 0 indexed] x_center y_center width height
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
		np.savetxt('data/syntetic_dataset/txt_labels_yolov5/{}.txt'.format(image_name.replace('.jpeg', '')), img_df.values, fmt=['%d', '%f', '%f', '%f', '%f'])


create_txt_annotations()
classes = {0: 3003, 1: 3004, 2: 3022, 3: 3023}


# check annotations
def plot_bounding_box(image, annotation_list, classes):
	annotations = np.array(annotation_list)
	w, h = image.size
	plotted_image = ImageDraw.Draw(image)
	transformed_annotations = np.copy(annotations)
	transformed_annotations[:, [1, 3]] = annotations[:, [1, 3]] * w
	transformed_annotations[:, [2, 4]] = annotations[:, [2, 4]] * h
	transformed_annotations[:, 1] = transformed_annotations[:, 1] - (transformed_annotations[:, 3] / 2)
	transformed_annotations[:, 2] = transformed_annotations[:, 2] - (transformed_annotations[:, 4] / 2)
	transformed_annotations[:, 3] = transformed_annotations[:, 1] + transformed_annotations[:, 3]
	transformed_annotations[:, 4] = transformed_annotations[:, 2] + transformed_annotations[:, 4]
	for ann in transformed_annotations:
		obj_cls, x0, y0, x1, y1 = ann
		plotted_image.rectangle(((x0, y0), (x1, y1)))
		plotted_image.text((x0, y0 - 10), str(classes[obj_cls]))

	plt.imshow(np.array(image))
	plt.show()


# img to test
img_number = 3

# get annotation file
annotation_file = 'data/syntetic_dataset/txt_labels_yolov5/{}.txt'.format(img_number)
with open(annotation_file, "r") as file:
	annotation_list = file.read().split("\n")[:-1]
	annotation_list = [x.split(" ") for x in annotation_list]
	annotation_list = [[float(y) for y in x] for x in annotation_list]

# get the corresponding image file
image_file = 'data/syntetic_dataset/images/{}.jpeg'.format(img_number)
assert os.path.exists(image_file)

# load the image
image = Image.open(image_file)

# plot the bounding box
plot_bounding_box(image, annotation_list, classes)

import os
import shutil
from sklearn.model_selection import train_test_split

# read images and annotations
images = [os.path.join('images', x) for x in os.listdir('images')]
annotations = [os.path.join('txt_labels_yolov5', x) for x in os.listdir('txt_labels_yolov5') if x[-3:] == "txt"]

# careful some images don't have annotations
a = [int(path.replace('.jpeg', '').replace('images/', '')) for path in images]
b = [int(path.replace('.txt', '').replace('txt_labels_yolov5/', '')) for path in annotations]
missing_ann = list(set(a) - set(b))
remove_img = ['images/{}.jpeg'.format(n) for n in missing_ann]
print(remove_img)
images = list(set(images) - set(remove_img))

images.sort()
annotations.sort()

# split the dataset into train-valid-test splits (80-10-10)
train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size=0.2, random_state=1)
val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size=0.5, random_state=1)

working_dir = '/Users/antoineescoyez/Desktop/cs433/CS433-PROJ2-ALAEMD/datasets/'
dirs = ['images/train',  'images/val',  'images/test', 'labels/train', 'labels/val',  'labels/test']


# utility function to move images
def move_files_to_folder(list_of_files, destination_folder):
	for f in list_of_files:
		try:
			shutil.move(f, destination_folder)
		except:
			print(f)
			assert False


# move the splits into their folders
move_files_to_folder(train_images, working_dir + 'images/train')
move_files_to_folder(val_images, working_dir + 'images/val/')
move_files_to_folder(test_images, working_dir + 'images/test/')
move_files_to_folder(train_annotations, working_dir + 'labels/train/')
move_files_to_folder(val_annotations, working_dir + 'labels/val/')
move_files_to_folder(test_annotations, working_dir + 'labels/test/')


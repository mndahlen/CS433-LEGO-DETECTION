import os
import shutil
from sklearn.model_selection import train_test_split

LOADDATASETDIR = "data/datasets/A"
SAVEDATASETDIR = 'data/datasets/A_YOLO'

# read images and annotations
images = [os.path.join(LOADDATASETDIR + "/images", x) for x in os.listdir(LOADDATASETDIR + "/images")]
annotations = [os.path.join(SAVEDATASETDIR + "/labels/all", x) for x in os.listdir(SAVEDATASETDIR + "/labels/all") if x[-3:] == "txt"]

# careful some images don't have annotations
a = [int(path.replace('.jpeg', '').replace(os.path.join(LOADDATASETDIR + "/images\\"), '')) for path in images]
b = [int(path.replace('.txt', '').replace(SAVEDATASETDIR + "/labels/all\\", '')) for path in annotations]

missing_ann = list(set(a) - set(b))
remove_img = ["{}/images/{}.jpeg".format(LOADDATASETDIR,n) for n in missing_ann]
images = list(set(images) - set(remove_img))

images.sort()
annotations.sort()

# split the dataset into train-valid-test splits (80-10-10)
train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size=0.2, random_state=1)
val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size=0.5, random_state=1)

working_dir = SAVEDATASETDIR

# utility function to move images
def move_files_to_folder(list_of_files, destination_folder):
	for f in list_of_files:
		try:
			shutil.move(f, destination_folder)
		except:
			print(f)
			assert False

# move the splits into their folders
move_files_to_folder(train_images, working_dir + '/images/train')
move_files_to_folder(val_images, working_dir + '/images/val/')
move_files_to_folder(test_images, working_dir + '/images/test/')
move_files_to_folder(train_annotations, working_dir + '/labels/train/')
move_files_to_folder(val_annotations, working_dir + '/labels/val/')
move_files_to_folder(test_annotations, working_dir + '/labels/test/')


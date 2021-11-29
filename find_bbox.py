import cv2
import numpy as np

im = cv2.imread('data\kaggle\\3004\\0001.png')

# Get bbox of image (We expect everything but lego to be black, I.E 0 intensity)
im_1_channel = np.sum(im,2)
im_find_x = np.sum(im_1_channel,0)
im_find_y = np.sum(im_1_channel,1)

x_low = 0
x_high = 255
y_low = 0
y_high = 255

idx = 0
low_found = False
for i in im_find_x:
    if not low_found:
        if i != 0:
            low_found = True
            x_low = idx
    else:
        if i == 0:
            x_high = idx
            break
    idx += 1

idx = 0
low_found = False
for i in im_find_y:
    if not low_found:
        if i != 0:
            low_found = True
            y_low = idx
    else:
        if i == 0:
            y_high = idx
            break
    idx += 1

print(x_low,x_high,y_low,y_high)
im = cv2.rectangle(im, (x_low, y_low), (x_high, y_high), (255, 0, 0), 2)
cv2.imshow("test",im)
cv2.waitKey(0) 

cv2.destroyAllWindows() 

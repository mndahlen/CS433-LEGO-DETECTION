import cv2

capture = cv2.VideoCapture('2540.mp4')
frameNr = 0

while (True):
    # process frames
    success, frame = capture.read()
    print(frameNr)
    cv2.imwrite('../brick_recording_split/2540/2540_{}.png'.format(frameNr),frame)
    frameNr += 1
from Video import VideoCamera, RPiCamera
import cv2
vid = cv2.VideoCapture('./test/traffic.mp4')

while True:
    _,img = vid.read()
    cv2.imshow('image',img)
    if cv2.waitKey(1) == 'q':
        cv2.destroyAllWindows()
        exit()
import StreamingClient
import time
import cv2
from imageai.Detection import ObjectDetection
import argparse
import tkinter
import Calling
TEL = ['66966494859','66836889001','66840995919']
ap = argparse.ArgumentParser()
ap.add_argument('--host',required=True,help='camera server url',default='http://192.168.31.22:5000')
ap.add_argument('--debug',default = False, type=bool)
args = vars(ap.parse_args())



client = StreamingClient.StreamingClient(args['host'])
client.connect()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("./weight/yolo.h5")
detector.loadModel()



while not client.isConnected: pass
i = 0
while True:
    frame = client.image.copy()
    height,width = frame.shape[:2]
    # center rectangle
    # p1 =  height//4, width//4
    # p2 =  height*3//4, width*3//4
    
    p1 = 0, width//2
    p2 = height, width

    detectArea = frame[p1[0]:p2[0], p1[1]:p2[1]]
    
    _, detections = detector.detectObjectsFromImage(input_image=detectArea,input_type='array',output_type='array', minimum_percentage_probability=30,)
    detectArea[:,:,2] += 64
    persons = list(filter(lambda detection: detection['name'] == 'person' ,detections))
    for person in persons:
        points = person['box_points']
        detectArea = cv2.rectangle(detectArea,points[:2], points[2:], color=(0,0,255),thickness=2)
    
    frame[p1[0]:p2[0], p1[1]:p2[1]] = detectArea
    frame = cv2.rectangle(frame,p1[::-1], p2[::-1],color=(0,255,0),thickness=2)
    if len(persons) > 0:
        if len(persons) == 1:
            msg = 'Alert: {} Person'.format(1)
        else:
            msg = 'Alert: {} Persons'.format(len(persons))
        cv2.putText(frame, msg, (0,64), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255) ,3)
        if not args['debug']:
            Calling.call(TEL,'Camera 123 was detected invader')
    
    
    frame = cv2.resize(frame,None,fx=2,fy=2)
    cv2.imshow('f',frame)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    i+=1
    print(i)
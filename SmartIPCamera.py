from Video import VideoCamera, RPiCamera
import StreamingClient
import time
import cv2
from imageai.Detection import ObjectDetection
MAX_FPS = 30



client = StreamingClient.StreamingClient('http://localhost:5000')
client.connect()
detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath("./weight/yolo-tiny.h5")
detector.loadModel()
while not client.isConnected:pass
while True:
    frame = client.image
    height,width = frame.shape[:2]
    # yield frame
    p1 =  height//4, width//4
    p2 =  height*3//4, width*3//4
    
    detectArea = frame[p1[0]:p2[0], p1[1]:p2[1]]
    detectArea, detections = detector.detectObjectsFromImage(input_image=detectArea,input_type='array',output_type='array', minimum_percentage_probability=30,)
    
    persons = list(filter(lambda detection: detection['name'] == 'person' ,detections))
    
    frame[p1[0]:p2[0], p1[1]:p2[1]] = detectArea
    frame = cv2.rectangle(frame,p1[::-1], p2[::-1],color=(0,255,0),thickness=2)
    
    cv2.imshow('f',frame)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
    time.sleep(1/MAX_FPS)

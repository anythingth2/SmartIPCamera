from flask import Flask, render_template,request, Response
import cv2
from threading import Timer 
import time
from imageai.Detection import ObjectDetection


cam = cv2.VideoCapture(0)
app = Flask(__name__)
detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath("./weight/yolo-tiny.h5")
detector.loadModel()

def generateFrame():
    while cam.isOpened():
        _, frame = cam.read()

        height,width = frame.shape[:2]
    # yield frame
        p1 =  height//4, width//4
        p2 =  height*3//4, width*3//4
        
        detectArea = frame[p1[0]:p2[0], p1[1]:p2[1]]
        detectArea, detections = detector.detectObjectsFromImage(input_image=detectArea,input_type='array',output_type='array', minimum_percentage_probability=30,)
        
        persons = list(filter(lambda detection: detection['name'] == 'person' ,detections))
        
        frame[p1[0]:p2[0], p1[1]:p2[1]] = detectArea
        frame = cv2.rectangle(frame,p1[::-1], p2[::-1],color=(0,255,0),thickness=2)
        
        _, buff = cv2.imencode('.jpg',frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buff.tobytes() + b'\r\n')

@app.route('/index')
def index():
    return 'Hello'
@app.route('/vid')
def video_feed():
    return Response(generateFrame(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/image')
def image():
    ret, frame = cam.read()
    if not ret:
        return 'fail to capture image'
    ret, buff = cv2.imencode('.jpg',frame)
    if not ret:
        return 'fail to encode'
    return buff.tobytes()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
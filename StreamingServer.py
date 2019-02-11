from flask import Flask, render_template,request, Response
import cv2
from threading import Timer 
import time


cam = cv2.VideoCapture(0)
app = Flask(__name__)

def generateFrame():
    while cam.isOpened():
        _, frame = cam.read()
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
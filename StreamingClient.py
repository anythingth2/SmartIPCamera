import requests
import numpy as np
import cv2
from threading import Thread

class StreamingClient:
    def __init__(self, host):
        self.host = host
        self.image = None
        self.thread = None
        self.req = None
        self.isConnected = False 
    def __connect(self):
        print('connecting')
        self.req = requests.get(self.host+'/vid',stream=True)
        print('connected')
        byte = b''
        while True:
            cancel = False
            frame = np.zeros((2,2),dtype='uint8')
            while not cancel:
                try:
                    incomingByte = self.req.raw.read(1024)
                    byte += incomingByte
                    a = byte.find(b'\xff\xd8')
                    b = byte.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = byte[a:b+2]
                        byte = byte[b+2:]
                        self.image = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8,),cv2.IMREAD_COLOR)
                        self.isConnected = True
                        break
                except:
                    print('Failed to get image from server')
                    cancel = True
    def connect(self):
        self.thread = Thread(target=self.__connect)
        self.thread.daemon = True
        self.thread.start()
    
class LocalClient:
    def __init__(self):
        self.image = None
        self.thread = None
        self.req = None
        self.isConnected = False 
    def __connect(self):
        cam = cv2.VideoCapture(0)
        # while cam.is_open(
        self.isConnected = True
        while True:
            
            # cancel = False
            # frame = np.zeros((2,2),dtype='uint8')
            # while not cancel:
            #     try:
            #         incomingByte = self.req.raw.read(1024)
            #         byte += incomingByte
            #         a = byte.find(b'\xff\xd8')
            #         b = byte.find(b'\xff\xd9')
            #         if a != -1 and b != -1:
            #             jpg = byte[a:b+2]
            #             byte = byte[b+2:]
            #             self.image = cv2.imdecode(np.fromstring(jpg,dtype=np.uint8,),cv2.IMREAD_COLOR)
            #             self.isConnected = True
            #             break
            #     except:
            #         print('Failed to get image from server')
            #         cancel = True
            _, self.image = cam.read()
            
    def connect(self):
        self.thread = Thread(target=self.__connect)
        self.thread.daemon = True
        self.thread.start()
    

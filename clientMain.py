import cv2
import numpy as np
import pickle
import socket
import struct
import sys

"""사용자 실시간 얼굴 서버 전송로직"""

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 9999))

while True:

    ret, frame = cap.read()
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))  
    clientsocket.sendall(message_size + data)

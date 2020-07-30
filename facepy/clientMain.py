import cv2
import face_recognition
import hashlib

import numpy as np
import pickle
import socket
import struct
import sys
from table import CRUDdatabase


def login(id, pw):
    # GUI 구현
    db = CRUDdatabase()
    pw = hashlib.sha256(pw.encode())
    pw = pw.hexdigest()
    print(id, pw)
    if db.login(id, pw) == True:
        print('Login Success')
        # TODO 로그인후 켐 로직 실행
    else:
        print('Login False')


login('bcbc', 'bcbc')
"""사용자 실시간 얼굴 서버 전송로직"""
cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 9999))

while True:
    ret, frame = cap.read()
    data = pickle.dumps(frame)

    # Send message length first
    #cv2.imshow("VIdeo", frame)
    face_landmarks_list = face_recognition.face_landmarks(frame)
    if face_landmarks_list:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_encodings = np.asarray(face_encodings).T
        data = pickle.dumps(face_encodings)
        message_size = struct.pack("L", len(data))  # CHANGED
        clientsocket.sendall(message_size + data)

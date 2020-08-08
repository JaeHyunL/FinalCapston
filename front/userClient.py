import cv2
import face_recognition
import hashlib

import numpy as np
import pickle
import socket
import struct
import sys

"""사용자 실시간 얼굴 서버 전송로직"""

# USER GUI 구현

def clientExe():
    cap = cv2.VideoCapture(0)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 9999))
    clientsocket.send('bcbc,bcbc'.encode())
    loginMsg = clientsocket.recv(1024)
#    if loginMsg.decode() == 'True':
    while True:
        ret, frame = cap.read()
        data = pickle.dumps(frame)
        face_landmarks_list = face_recognition.face_landmarks(frame)
        # 현제 얼굴이 인식된 상태에서만 데이터를 전송함
        if face_landmarks_list:
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(
                frame, face_locations)
            face_encodings = np.asarray(face_encodings).T
            data = pickle.dumps(face_encodings)
            message_size = struct.pack("L", len(data))  # CHANGED
            clientsocket.sendall(message_size + data)
        cv2.imshow('frame_color', frame)
#    elif loginMsg.decode() == 'False':
        # TODO 로그인 실패 재로그인 기능 구현
#        pass
#

import cv2
import face_recognition
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

    # Send message length first
    cv2.imshow("VIdeo", frame)
    face_landmarks_list = face_recognition.face_landmarks(frame)
    if face_landmarks_list:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_encodings = np.asarray(face_encodings).T
        data = pickle.dumps(face_encodings)
        message_size = struct.pack("L", len(data))  # CHANGED
        clientsocket.sendall(message_size + data)

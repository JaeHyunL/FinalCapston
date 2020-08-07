import cv2
import face_recognition
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import socket
import struct
import time

from database import Database
from threading import Thread
from table import CRUDdatabase


""" 사용자  받은 
데이터 이미지 처리"""


def getDataToImage(HOST, PORT):
    #global frame
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)

    conn, addr = s.accept()
    print(s.accept())
    data = b''
    payload_size = struct.calcsize("L")

    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]  # CHANGED

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)
        
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imwrite('./UserImage/firstImage.jpg', frame)
        cv2.imshow("good", frame)
        # insert_Image(frame)
        # cv2.waitKey(1)
        #db = CRUDdatabase()
        # db.getDbImage()
        #ad = CRUDdatabase()
        #aq = "./UserImage/client"
        # ad.insertImage(str(aq))
        getImageDataToDB(frame)


"""디비에서 이미지 가져오기"""


def getDbImage():
    ad = CRUDdatabase()
    a = ad.getImage(1)
    img = cv2.imread(a['image_file_str'])
    plt.imshow(img)
    plt.show()


def getImageDataToDB(frame):
    ad = CRUDdatabase()
    face_landmarks_list = face_recognition.face_landmarks(frame)
    if face_landmarks_list:

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_encodings = np.asarray(face_encodings).T
   #     cv2.imshow(frame)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.imwrite('./UserImage/tty.jpg', frame)
            cv2.imshow(frame)

        #df = pd.DataFrame(face_encodings)
        # ad.insertcsv(df)
        # df.to_csv('./UserImage/captured_feature_data.csv',
        #          index=False, header=None)


if __name__ == "__main__":
    getDataToImage("127.0.0.1", 9999)

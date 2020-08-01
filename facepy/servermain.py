import cv2
import face_recognition
import numpy as np
import matplotlib.pyplot as plt
import hashlib
import pandas as pd
import pickle
import socket
import struct
import time
from database import Database
from threading import Thread
from table import CRUDdatabase


def getDataToImage(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    conn, addr = s.accept()
    data = b''
    payload_size = struct.calcsize("L")
    id, pw = conn.recv(1024).decode().split(',')

    if login(id, pw) == True:
        conn.sendall('True'.encode())
        userName =userNamelookup(id)
        while True:
            while len(data) < payload_size:
                data += conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
    #     print(frame)
            getImageDataToDB(frame,userName)
#    elif login(id, pw) == False:
#        s.send('False'.encode())


"""디비에서 이미지 가져오기"""


def getDbImage():
    db = CRUDdatabase()
    a = db.get_Image(1)
    img = cv2.imread(a['image_file_str'])
    plt.imshow(img)
    plt.show()


def getImageDataToDB(frame,userName):
    db = CRUDdatabase()
    db.insert_FaceDifference(frame,userName)


def attendance():
    # 생각해보니꺼 유저 출결정보를 가지고
    # 이미지에 있는데이터 셋들을 가져와서
    # 비교를 떄리는거지 근데 디비 구조를 파악해야대는데
    # 디비 구조가 클래스 코드로 비교해서
    #
    pass


def login(id, pw):

    db = CRUDdatabase()
    pw = hashlib.sha256(pw.encode())
    pw = pw.hexdigest()
    if db.login(id, pw) == True:
        return True
    else:
        return False


def userNamelookup(id):
    db = CRUDdatabase()
    userInfo = db.userLookup(id)
    userInfo = dict(*userInfo)
    return userInfo['user_name']


if __name__ == "__main__":
    getDataToImage("127.0.0.1", 9999)

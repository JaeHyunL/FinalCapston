import cv2
import matplotlib.pyplot as plt
import pickle
import socket
import struct
import time 

from database import Database
from table import CRUDdatabase

""" 사용자  받은 
데이터 이미지 처리"""
def getDataToImage(HOST,PORT):
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)

    conn, addr = s.accept()

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
        print("반복이안되는이유는?")
        
        frame = pickle.loads(frame_data)
        cv2.imwrite('./UserImage/clientJPG.jpg', frame)
        time.sleep(0.1)
        cv2.waitKey(1)

"""디비에서 이미지 가져오기"""
def getDbImage():
    ad = CRUDdatabase()
    a = ad.getImage(1)
    img = cv2.imread(a['image_file_str'])
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    getDataToImage("127.0.0.1",9999)
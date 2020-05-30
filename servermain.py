import pickle
import socket
import struct
from database import Database
import cv2
from table import CRUDdatabase
import matplotlib.pyplot as plt

HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

conn, addr = s.accept()

data = b''  # CHANGED
payload_size = struct.calcsize("L")  # CHANGED

while True:

    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)
    a = input()
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]  # CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    #클라에서 받는 데이터  저장 
    frame = pickle.loads(frame_data)
    cv2.imwrite('./UserImage/clientJPG.jpg', frame)
    # Display
    if a == "q":
        break
    cv2.waitKey(1)

ad = CRUDdatabase()
a = ad.getImage(1)
img = cv2.imread(a['image_file_str'])
plt.imshow(img)
plt.show()

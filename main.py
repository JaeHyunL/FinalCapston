from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
import cv2
import socket
import io
import facerecognition
# Flask 서버 설정
app = Flask(__name__)
# cv2 사용 0번째 카메라로 video캡쳐 시작
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
vc = cv2.VideoCapture(0)


@app.route('/')
def index():
    # 비디오 캡처 시작
    """Video streaming ."""
    return render_template('test.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


def gen():

    # 비디오 캡처기능
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        frame = facerecognition.detectAndDisplay(frame)
        cv2.imwrite('pic.jpg', frame)
        # 제네레이터를 사용하여 객채를읽어옴
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """비디오스트리밍 경로 .{{ url_for('video_feed') }} 지정."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

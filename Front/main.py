import cv2
import socket
import io
import hashlib
import os
from flask import jsonify, Flask, render_template, Response, request, redirect, make_response, session
from flask_socketio import SocketIO, send
from sitable import Signdatabase
import jwt
from clientMain2 import clientExe
# Flask 서버 설정
app = Flask(__name__)
# cv2 사용 0번째 카메라로 video캡쳐 시작
app.config['SECRET_KEY'] = 'BCODE_Flask'
socketio = SocketIO(app)
vc = cv2.VideoCapture(0)
tmepUserID = ''


@app.route('/signup/info', methods=['GET', 'POST'])
def sigUP():
    if request.method == 'POST':
        # 회원가입요청
        studendt_no = request.form['student_num']
        studendt_pass = request.form['student_pass']
        studendt_pass = hashlib.sha256(studendt_pass.encode())
        studendt_pass = studendt_pass.hexdigest()
        studendt_name = request.form['student_name']
        student_ID = request.form['student_ID']
        db = Signdatabase()
        db.insert_studentInfo(studendt_no, studendt_pass,
                              studendt_name, student_ID)
        return redirect('Registration')
    return render_template('signup.html')


# TODO 버튼 클릭 이벤트처리
@app.route('/signup/Registration', methods=['GET', 'POST'])
def registration():
    """Video streaming ."""
    # 저장로직
    if request.method == 'POST':
        print('애초에여기타긴타냐?')
        vc.release()
        cv2.destroyAllWindows()
    return render_template('index.html')


# TODO 로그인 인증 세션 발급 후 
@app.route("/signin", methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        db = Signdatabase()
        pw = hashlib.sha256(request.form['password'].encode())
        pw = pw.hexdigest()
        userid = request.form['username']
        result = db.auth(userid, pw)

        if result == True:

            session[userid] = userid
            global tmepUserID
            tmepUserID = userid
            return 'counter:' + str(session[userid])
        elif result == False:
            print('인증실패')
    return render_template('signin.html')

# def sign_tokken():


def gen():
    # 비디오 캡처기능
    """Video streaming generator function."""
    os.makedirs('./UserImage/{}'.format(tmepUserID), exist_ok=True)
    vc = cv2.VideoCapture(0)
    while (vc.isOpened()):
        rval, frame = vc.read()
        cv2.imwrite(
            './UserImage/{0}/{1}.jpg'.format(tmepUserID, tmepUserID+'firstImage'), frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('./UserImage/{0}/{1}.jpg'.format(tmepUserID, tmepUserID+'firstImage'), 'rb').read() + b'\r\n')
        if cv2.waitKey(1) & 0xFF == 27:
            break


@app.route('/video_feed')
def video_feed():
    """비디오스트리밍 경로 .{{ url_for('video_feed') }} 지정."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/logout')
def logout():
    # remove the username from the session if it is there

    print(session.pop('username', None))
    return render_template('signin.html')

#TODO 세션 발급 후 세션인증 되었을때만 처리 로직
#TODO 사용자가 누군지 알려줘야함 ^^ 
@app.route('/ClientOpen', methods=['GET', 'POST'])
def clientAction():
    if request.method == 'POST':

        clientExe()
    return render_template('action.html')


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

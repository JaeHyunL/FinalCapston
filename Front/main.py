import base64
import cv2
import socket
import io
import hashlib
import os
from flask import jsonify, Flask, render_template, Response, request, redirect, make_response, session
from flask_socketio import SocketIO, send
from sitable import Signdatabase
import jwt
from userClient import clientExe

app = Flask(__name__)
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


# TODO 저장로직
@app.route('/signup/Registration', methods=['GET', 'POST'])
def registration():
    """Video streaming ."""
    if request.method == 'POST':
        print('애초에여기타긴타냐?')
        vc.release()
        cv2.destroyAllWindows()
    return render_template('index.html')


@app.route("/signin", methods=['GET', 'POST'])
def signIn():
    if cookie_status() == b'':
        if request.method == 'POST':
            db = Signdatabase()
            pw = hashlib.sha256(request.form['password'].encode())
            pw = pw.hexdigest()
            print(request.form)
            userid = request.form['student_ID']
            result = db.auth(userid, pw)

            if result == True:
                userid = userid.encode('UTF-8')
                userid = base64.b64encode(userid)
                custom_resp = Response("COkkie 설정")
                custom_resp.set_cookie("USERID", userid)

                global tmepUserID
                tmepUserID = userid
                return custom_resp
            elif result == False:
                return '아이디 또는 비밀번호가 다릅니다. '
    elif cookie_status != b'':
        return '이미 로그인 되어져 있습니다! '
    return render_template('signin.html')


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
    custom_resp = Response("COOKIE 제거")
    custom_resp.set_cookie('USERID', expires=0)
    return custom_resp

# TODO 세션 발급 후 세션인증 되었을때만 처리 로직
# TODO 사용자가 누군지 알려줘야함 ^^
@app.route('/ClientOpen', methods=['GET', 'POST'])
def clientAction():
    if request.method == 'POST':

        clientExe()
    return render_template('action.html')


# 쿠키 값 확인 함수
@app.route("/loginstatus")
def cookie_status():
    tempstr = request.cookies.get('USERID', '빈문자열')
    tempstr = tempstr.encode("UTF-8")
    return base64.b64decode(tempstr)


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)

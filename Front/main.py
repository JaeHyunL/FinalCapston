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

#TODO 네브바 필요 
#TODO 화면전환 redirect 동적
#TODO 출결 관리 페이지 
#TODO 켐 인식 돌리는거 Break 문 필요 

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
        return redirect('../signin')
    return render_template('signup.html')


# TODO 저장로직
@app.route('/signup/Registration', methods=['GET', 'POST'])
def registration():
    """Video streaming ."""
    if login_status() == False:
        if request.method == 'POST':
            print('애초에여기타긴타냐?')
            vc.release()
            cv2.destroyAllWindows()
        return render_template('index.html')
    elif login_status() == True:
        return '로그인 인증이 안됬습니다. '


@app.route("/signin", methods=['GET', 'POST'])
def signIn():
    if login_status() == True:
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

                return custom_resp
            elif result == False:
                return '아이디 또는 비밀번호가 다릅니다. '
    elif login_status() == False:
        return '이미 로그인 되어져 있습니다! '
    return render_template('signin.html')


def gen(cookie):
    # 비디오 캡처기능
    """Video streaming generator function."""
    os.makedirs('./UserImage/{}'.format(cookie), exist_ok=True)
    vc = cv2.VideoCapture(0)
    while (vc.isOpened()):
        # 무한루프 깨는 로직 필요 ... 흠 .. 너무 세드하네 ;; 
        rval, frame = vc.read()
        cv2.imwrite(
            './UserImage/{0}/{1}.jpg'.format(cookie, cookie+'firstImage'), frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('./UserImage/{0}/{1}.jpg'.format(cookie, cookie+'firstImage'), 'rb').read() + b'\r\n')
        if cv2.waitKey(1) & 0xFF == 27:
            break


@app.route('/video_feed')
def video_feed():
    """비디오스트리밍 경로 .{{ url_for('video_feed') }} 지정."""
    mkStr = cookie_status()
    return Response(gen(mkStr),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/logout')
def logout():
    custom_resp = Response("COOKIE 제거")
    custom_resp.set_cookie('USERID', expires=0)
    return custom_resp


@app.route('/ClientOpen', methods=['GET', 'POST'])
def clientAction():
    if login_status() == False:
        if request.method == 'POST':

            clientExe(cookie_status())
    elif login_status() == True:
        redirect('/signin')
    return render_template('action.html')


# 쿠키 값 확인 함수.
@app.route("/loginstatus")
def cookie_status():
    tempstr = request.cookies.get('USERID', '빈문자열')
    tempstr = tempstr.encode("UTF-8")

    return (base64.b64decode(tempstr)).decode('UTF-8')

# 로그인 상태 여부 확인
def login_status():
   
    # 로그인이 안되어있을 때
    if cookie_status() == '':
        return True
    # 로그인이 되어 있을 때 
    elif cookie_status() != '':
        return False


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)


# 필요한거 네브바
# 함수 처리후 다음 페이지로 자연스럽게 이동
# 흠 ...

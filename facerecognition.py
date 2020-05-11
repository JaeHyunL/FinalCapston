from __future__ import print_function
import cv2 as cv
import argparse

# 화면탐지 함수


def detectAndDisplay(frame):
    # 그레이 이미지를 띄움 (컬러보다 효율이 좋음)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # 히스토그램 균일화
    frame_gray = cv.equalizeHist(frame_gray)

    # detectMultiScale 함수는 얼굴을 검출하며 인자값으로 (그레이 스케일 이미지를) 받는다
    # 얼굴이 검출되면 해당 위치를  리턴합니다 x , y w h
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x, y, w, h) in faces:

        # 검출된 부분을 타원으로 그려줌
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2),
                           0, 0, 360, (255, 0, 255), 4)

        # 회색 얼굴일때는 이런식으로 값을 계산해준다고합니다
        faceROI = frame_gray[y:y+h, x:x+w]

        # 눈은 항상 얼굴 안에 있기에 그 안에서 검출해준다.
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2, y2, w2, h2) in eyes:
            # 눈위에 원을 그려준다 그아래는 원의 크기를 정의함
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

    # 얼굴 감지 !
    return frame

#다음 코드는 정수 목록을 받아 합계 또는 최댓값을 출력하는 파이썬 프로그램입니다:
#argparse 를 사용하는 첫 번째 단계는 ArgumentParser 객체를 생성하는것 . 
parser = argparse.ArgumentParser(
    description='Code for Cascade Classifier tutorial.')


#parser에 add_argument 를 사용하여 학습된 xml 파일을 전송시켜줌 
parser.add_argument('--face_cascade', help='Path to face cascade.',
                    default='./haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.',
                    default='./haarcascade_eye_tree_eyeglasses.xml')

#카메라 번호를 추가해줌 (카메라가 한대이면 0 )
parser.add_argument(
    '--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()

#face_cascade_name 
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade

#cv에 있는 CascadeClassifier를 사용 
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

# -- 1. cascades 를 불러옴 (미리 준비된학습데이터와 함께 )
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

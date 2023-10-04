import cv2
import numpy as np
from shapely.geometry import Polygon
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero import Servo
import Adafruit_DHT
import time
from time import sleep

# s = AngularServo(17, min_angle=-45, max_angle=45)
# while True:
#     s.angle = -45.0
#     sleep(1)
#     s.angle = 45.0
#     sleep(1)


factory = PiGPIOFactory()
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

angle = 0
# count = 0
# operationStart = 0
# text = None
# face_center_x=0


# 서보모터 초기화
servo = AngularServo(17, min_angle=-45, max_angle=45, pin_factory=factory)


# 서보모터 제어 함수
def control_submotor(angle):
    # 서보모터를 해당 각도로 제어하는 코드 작성
    servo.angle = -angle
    print(angle)
#     servo.angle = -45
#     sleep(1)
#     servo.angle = 45.0
#     sleep(1)

    
while True:
    ret, frame = cap.read()
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     # define range of blue color in HSV
#     lower = np.array([0, 40, 80])
#     upper = np.array([20, 255, 255])
#     # Threshold the HSV image to get only blue colors
#     mask = cv2.inRange(hsv, lower, upper)
#     mask = cv2.blur(mask, (5, 5))
#     _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

        # 얼굴 검출 로직 추가
        #if operationStart == 1:
#         else:
    #print("얼굴 검출 시작")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = frame.shape[:2]
    center_x = width // 2  # 화면 중심 x 좌표
#     center_x = 250  # 화면 중심 x 좌표


    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
#     #시작시 문자 출력
#     if text is not None:
#         cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    for (x, y, w, h) in faces:
        # 얼굴의 중심 x 좌표 계산
        face_center_x = x + (w // 2)

        # 화면 중심과 얼굴 중심의 차이 계산
        diff_x = face_center_x - center_x
        threshold = 50

        # 일정 범위 이상 벗어난 경우 서보모터 제어
        if abs(diff_x) > threshold:
#                     print("각도 조절 시작")

            angle = (diff_x / center_x) * (45)  # 각도 계산 함수 호출
            angle = int(angle)
            
            

            control_submotor(angle)  # 서보모터 제어 함수 호출
            
            
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break



#     control_submotor(angle)

cap.release()
cv2.destroyAllWindows()    
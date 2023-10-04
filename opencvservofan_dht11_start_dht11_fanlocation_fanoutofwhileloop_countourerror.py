import cv2
import numpy as np
from shapely.geometry import Polygon
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero import Servo
import Adafruit_DHT
import time

factory = PiGPIOFactory()

DHT11_sensor = Adafruit_DHT.DHT11
DHT11_pin = 27



# 팬 출력값을 저장할 변수
fan_output = 0

#온습도센서/팬 출력
humidity, temperature = Adafruit_DHT.read_retry(DHT11_sensor, DHT11_pin)

if humidity is not None and temperature is not None:
    #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    
    # 온도 범위에 따라 팬 출력값 설정
    if temperature >= 30:
        fan_output = 3
    elif temperature >= 25 and temperature < 30:
        fan_output = 2
    else:
        fan_output = 1

else:
    print('Failed to get reading. Try again!')






cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


#loop 안에 넣으면 같이 초기화되어버림. 밖으로 빼야됨.import cv2
# angle = 0
count = 0
operationStart = 0
text = None

# 서보모터 초기화
servo = AngularServo(17, min_angle=-45, max_angle=45, pin_factory=factory)


# 서보모터 제어 함수
def control_submotor(angle):
    # 서보모터를 해당 각도로 제어하는 코드 작성
    servo.angle = angle

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = np.array([0, 40, 80])
    upper = np.array([20, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.blur(mask, (5, 5))
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # 컨투어가 하나 이상 존재하는지 확인
    if contours:
        contour_areas = [cv2.contourArea(cnt) for cnt in contours]
        max_contour_index = np.argmax(contour_areas)
        max_contour = contours[max_contour_index]
        cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)
        
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)
        
        
        
        if operationStart == 0:
            if defects is not None:
                #print("손 검출 시작")
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(max_contour[s][0])
                    end = tuple(max_contour[e][0])
                    far = tuple(max_contour[f][0])
                    cv2.line(frame, start, end, [255, 0, 0], 2)
                    cv2.circle(frame, far, 5, [0, 0, 255], -1)
                    if d > 16000:
                        count = count + 1
            
            if count > 3:
                text = "Start"
                operationStart = 1
                
            else:
                operationStart = 0
                count = 0
                

        # 얼굴 검출 로직 추가
        #if operationStart == 1:
        else:
            #print("얼굴 검출 시작")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = frame.shape[:2]
            center_x = width // 2  # 화면 중심 x 좌표

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            #시작시 문자 출력
            if text is not None:
                cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
            for (x, y, w, h) in faces:
                # 얼굴의 중심 x 좌표 계산
                face_center_x = x + (w // 2)

                # 화면 중심과 얼굴 중심의 차이 계산
                diff_x = face_center_x - center_x
                threshold = 50

                # 일정 범위 이상 벗어난 경우 서보모터 제어
                if abs(diff_x) > threshold:
#                     print("각도 조절 시작")
                    angle = (diff_x / center_x) * (25)  # 각도 계산 함수 호출
                    angle = int(angle)
                    if angle > 45:
                        angle = 45
                    elif angle < -45:
                        angle = -45
                    control_submotor(angle)  # 서보모터 제어 함수 호출
#                 else:
#                     angle = 0
#                     control_submotor(angle)
                    
            # 팬 출력값에 따라 팬을 제어
            if operationStart == 1:
                if fan_output == 3:
                    #print("fan 3")
                    # 높은 팬 출력값에 대한 동작
                    pass
                elif fan_output == 2:
                    #print("fan 2")
                    # 중간 팬 출력값에 대한 동작
                    pass
                elif fan_output == 1:
                    #print("fan 1")
                    # 낮은 팬 출력값에 대한 동작
                    pass
             
        
    else:
        print("findCountours failed")
    # 컨투어를 찾지 못한 경우에 대한 처리
    
    
    
        
            
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    

cap.release()
cv2.destroyAllWindows()


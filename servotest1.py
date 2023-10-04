from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
# help (AngularServo)


# from gpiozero import Servo
# 
# s = Servo(17)
# s.min() # measure the angle
# s.max() # measure the angle
# 

from time import sleep
factory = PiGPIOFactory()

# from gpiozero import AngularServo
# from gpiozero import Servo
# 
# servo = Servo(17)

# while True:
#     servo.min()
#     sleep(1)
#     servo.mid()
#     sleep(1)
#     servo.max()
#     sleep(1)
    
# while True:    
#     servo.value = -1    
#     sleep(1)
#     servo.value = 0 
#     sleep(1)
#     servo.value = 1    
#     sleep(1)
    

s = AngularServo(17, min_angle=-45, max_angle=45, pin_factory=factory)
while True:
    s.angle = -45
    sleep(10)
#     s.angle = -90.0
#     sleep(1)
#     s.angle = 0
#     sleep(1)
#     s.angle = 90.0
#     sleep(1)
    s.angle = 45
    sleep(10)
    
#     # 서보모터 제어 함수
# def control_submotor(angle):
#     # 서보모터를 해당 각도로 제어하는 코드 작성
#     servo.angle = angle
#     sleep(2)
# 
# # 서보모터 초기화
# servo = AngularServo(17, min_angle=-90, max_angle=90)    
#     
# count = 0    
# while True:
#     
#     face_center_x= 200
#     diff_x = face_center_x - 100
#     threshold = 50
# 
#     # 일정 범위 이상 벗어난 경우 서보모터 제어
#     if abs(diff_x) > threshold:
#         
#         angle = (diff_x / 100) * (90)  # 각도 계산 함수 호출
#         angle = int(angle)
#         
#         control_submotor(angle)  # 서보모터 제어 함수 호출
#         


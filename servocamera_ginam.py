import cv2
import numpy as np
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import math

factory = PiGPIOFactory()
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

img = None
servo = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
# , pin_factory=factory

loc = 0
x = 180
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    try:
        loc = (faces[0][0]+faces[0][2])//2
    except IndexError:
        pass
#     print(loc)
    if loc > 200:
        servo.value = math.sin(math.radians(x))
        x += 1
    if loc < 160:
        servo.value = math.sin(math.radians(x))
        x -= 1
        
    frame = cv2.resize(frame, (800,600))
    cv2.imshow('Detect',frame)
    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()
import cv2
from djitellopy import Tello
import time

drone = Tello()
drone.connect()

drone.streamon()

cap = drone.get_video_capture()

while True:
    success, img = cap.read()

    cv2.imshow('hi', img)

    if cv2.waitKey(5)& 0xFF == 27:
            break

drone.streaoff()
drone.end()
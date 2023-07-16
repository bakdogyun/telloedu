from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(30)
time.sleep(1)
tello.move_back(30)

tello.land()

tello.end()
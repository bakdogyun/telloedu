from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

time.sleep(2)
time.sleep(5)
tello.move_up(30)
time.sleep(5)
tello.move_down(30)
time.sleep(5)
tello.move_down(30)
time.sleep(3)

tello.land()
tello.end()
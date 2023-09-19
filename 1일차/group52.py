from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(150)
time.sleep(3)
tello.rotate_counter_clockwise(90)
tello.move_forward(150)


tello.rotate_clockwise(90)
tello.move_forward(150)
tello.rotate_clockwise(90)
time.sleep(10)
tello.move_forward(75)
tello.rotate_counter_clockwise(90)
tello.move_forward(30)

tello.land()
tello.end()
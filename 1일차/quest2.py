from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(30)
tello.rotate_clockwise(90)

tello.move_forward(30)
tello.rotate_clockwise(90)

tello.move_forward(30)
tello.rotate_counter_clockwise(90)

tello.move_forward(30)
tello.rotate_counter_clockwise(90)

tello.move_forward(30)
time.sleep(5)

tello.land()

tello.end()
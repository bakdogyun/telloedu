from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(30)
tello.rotate_clockwise(135)

tello.move_forward(30)
tello.rotate_counter_clockwise(135)

tello.move_forward(30)
tello.rotate_clockwise(135)

tello.move_forward(30)
tello.rotate_counter_clockwise(90)

tello.move_forward(50)
time.sleep(1)

tello.land()

tello.end()
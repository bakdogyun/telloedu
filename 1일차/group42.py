from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.rotate_clockwise(60)
tello.move_forward(30)
tello.rotate_counter_clockwise(90)
tello.move_forward(30)
tello.rotate_clockwise(90)
tello.move_forward(30)
tello.rotate_counter_clockwise(90)
tello.move_forward(30)
tello.rotate_clockwise(90)
tello.move_forward(30)
tello.rotate_counter_clockwise(90)
tello.move_forward(30)

tello.land()
tello.end()
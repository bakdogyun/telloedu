from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(50)
tello.rotate_clockwise(90)
tello.move_forward(150)
tello.rotate_counter_clockwise(90)
tello.move_forward(100)

tello.rotate_clockwise(90)
tello.move_forward(150)
tello.rotate_clockwise(90)
tello.move_forward(300)
tello.rotate_clockwise(90)
tello.move_forward(30)

tello.land()
tello.end()
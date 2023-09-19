from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(30)
tello.rotate_clockwise(180)
tello.move_forward(30)

tello.land()

tello.end()
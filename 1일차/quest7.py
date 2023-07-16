from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_forward(30)
tello.move_right(30)
tello.move_left(30)

tello.land()

tello.end()
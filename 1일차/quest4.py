from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()

for i in range(0,3):
    tello.move_forward(30)
    tello.rotate_clockwise(120)

tello.land()
tello.end()
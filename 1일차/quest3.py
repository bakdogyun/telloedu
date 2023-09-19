from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()

for i in range(0,12):
    tello.move_forward(20)
    tello.rotate_clockwise(30)

tello.land()
tello.end()
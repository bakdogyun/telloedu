from djitellopy import Tello

tello = Tello()

tello.connect()

tello.takeoff()

for i in range(0,4):
    tello.curve_xyz_speed(50,50,0,100,0,0,20)
    tello.curve_xyz_speed(50,-50,0,0,-100,0,20)

tello.land()
tello.end()
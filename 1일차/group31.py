from djitellopy import Tello
import time

tello = Tello()

tello.connect()

tello.takeoff()

tello.move_up(100)
for i in range(0,6):
    tello.curve_xyz_speed(50,50,0,0,100,0,20)
    tello.curve_xyz_speed(50,-50,0,0,-100,0,20)

tello.land()
tello.end()
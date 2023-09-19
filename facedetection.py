import cv2
from djitellopy import Tello

TOLERANCE_X = 5
TOLERANCE_Y = 5
SLOWDOWN_THRESHOLD_X = 20
SLOWDOWN_THRESHOLD_Y = 20
DRONE_SPEED_X = 20
DRONE_SPEED_Y = 20
SET_POINT_X = 960/2
SET_POINT_Y = 720/2

faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
drone = Tello()  
drone.connect()
drone.takeoff()


drone.streamon()

while True:
    frame = drone.get_frame_read().frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    i = 0

    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 5)  
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 12, (255, 0, 0), 1)

        cv2.circle(frame, (int(SET_POINT_X), int(SET_POINT_Y)), 12, (255, 255, 0), 8)
        i = i+1
        distanceX = x+w/2 - SET_POINT_X
        distanceY = y+h/2 - SET_POINT_Y

        up_down_velocity = 0
        right_left_velocity = 0

        if distanceX < -TOLERANCE_X:
            right_left_velocity = - DRONE_SPEED_X

        elif distanceX > TOLERANCE_X:
            right_left_velocity = DRONE_SPEED_X

        if distanceY < -TOLERANCE_Y:
            up_down_velocity = DRONE_SPEED_Y
        elif distanceY > TOLERANCE_Y:
            up_down_velocity = - DRONE_SPEED_Y


        if abs(distanceX) < SLOWDOWN_THRESHOLD_X:
            right_left_velocity = int(right_left_velocity / 2)
        if abs(distanceY) < SLOWDOWN_THRESHOLD_Y:
            up_down_velocity = int(up_down_velocity / 2)

        drone.send_rc_control(right_left_velocity, 0, up_down_velocity, 0)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
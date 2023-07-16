"""
키보드로 드론 조정하기
"""

from djitellopy import Tello
from cvzone.FaceDetectionModule import FaceDetector
import cv2, time


color = (255,255,0)

tello = Tello()
tello.connect()

tello.streamon()

#tello.set_video_fps(Tello.FPS_15)ㅈ
frame_read = tello.get_frame_read()

print("batter_status = ", tello.get_battery())
print(frame_read.frame.shape)

# Tello 이륙하기/30cm up
tello.takeoff()
tello.move_up(30)

# Tello 카메라로부터 이미지를 읽기
while (True):
    img = frame_read.frame
    img = cv2.resize(img,(int(img.shape[1]/2), int(img.shape[0]/2)))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    # 03> 화면의 중심점 구하기
    width,height = img.shape[1], img.shape[0]
    cx, cy = int(width/2), int(height/2)

    # 화면의 중심에서 얼굴의 중심점까지 선그리기
    color2 = (0,0,255)
    cv2.line(img,(0,cy),(width,cy), color2, 1) # x축
    cv2.line(img,(cx,0),(cx,height),color2, 1) # y축
            
    cv2.imshow("Drone Camera", img)


    # 7> 키보드로 제어하기
    key = cv2.waitKey(2) & 0xff
    if key == 27: # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)
    elif key == ord('x'):
        tello.streamoff()
        cv2.destroyAllWindows() 
        break

# 착륙하기
tello.land()


        




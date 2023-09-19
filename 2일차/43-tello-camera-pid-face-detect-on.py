"""
Tello Drone의 전송 영상에 얼굴 탐지 및 트래킹 (pid 기본 적용)
- CVZONE_FACE_DETECT를 사용
- 앞뒤로만 이동(forward-backward)

<참고>
https://github.com/yaroslava-tkachuk/tello_follow_me
https://www.youtube.com/watch?v=URSCmWMIkE4
"""

from djitellopy import Tello
from cvzone.FaceDetectionModule import FaceDetector 
import numpy as np
import cv2, time

color = (255,255,0)
color2 = (0,0,255)

span_sec = 5.0 # 5.0 sec
flag_face_detect = False # 초기설정

# pid기반의 제어를 활용하는 경우에 사용
pid = [0.4, 0.4, 0]
pError = 0
fbRange = [80, 140] # px
11
# Tello Drone 객체 생성 및 연결
tello = Tello()
tello.connect()

# 얼굴인식을 위한 cvzone 객체 생성
detector = FaceDetector() 

# 영상전송 모드 ON
tello.streamon()

# Tello Drone에서 이미지 캡처를 위한 Thread 구동
#tello.set_video_fps(Tello.FPS_15)
frame_read = tello.get_frame_read()

# 배터리와 이미지 기본 정보 표시
print("batter_status = ", tello.get_battery())
print(frame_read.frame.shape)

# 시간측정(15초 전에 명령어 전송)
current_time = time.time()	
pre_time = current_time

# Tello 이륙하기
tello.takeoff()
tello.move_up(50)

try:
    while (True):
        img = frame_read.frame

        # 720x960이미지를 360x480이미지로 크기 변환
        img = cv2.resize(img,(int(img.shape[1]/2), int(img.shape[0]/2)))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        # 화면의 중심점 구하기
        width,height = img.shape[1], img.shape[0]
        cx, cy = int(width/2), int(height/2)
        
        # cvzone의 기존화면 표시 방식을 OFF
        img, bboxs = detector.findFaces(img,False) 
        if bboxs: 
            center = bboxs[0]["center"]
            bbox = bboxs[0]["bbox"]

            fx,fy,fw,fh = bbox  # 탐지된 얼굴영역의 bbox
            fcx,fcy = center[0], center[1]  # 얼굴영역의 중심 좌표(x,y)

            # 원래 cvzone에서는 bbox와 확률을 표시하고 있으나, 여기서는 bbox만 표시
            img = cv2.rectangle(img, bbox, color, 2)
            cv2.circle(img, center, 5, color, cv2.FILLED)

            # 화면의 중심을 교차하는 x,y축 그리기
            cv2.line(img,(0,cy),(width,cy), color2, 1) # x축
            cv2.line(img,(cx,0),(cx,height),color2, 1) # y축
            #cv2.line(img,(cx,cy) ,center, color,2)

            # 얼굴탐지 사각형영역의 코위치에서 이미지의 가운데까지의 픽셀차이
            dx = fcx - cx
            dy = fcy - cy

            # 얼굴영역의 width pixel수 표시
            cv2.putText(img, f'{bbox[3]}px',
                                    (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_PLAIN,
                                    2, color, 2)

            if flag_face_detect:
                # pid 방식으로 제어
                fb = 0 # forwar-backward

                error = fcx - width//2
                speed = pid[0] * error + pid[1] * (error - pError)
                speed = int(np.clip(speed, -100, 100))

                if fw > fbRange[0] and fw < fbRange[1]:
                    fb = 0
                elif fw > fbRange[1]:
                    fb = -25
                elif fw < fbRange[0] and fw != 0:
                    fb = 25

                if fx == 0:
                    speed = 0
                    error = 0
                print("Speed=%s, fb=%s" % (speed, fb))
                
                tello.send_rc_control(0, fb, 0, speed)
                pError = error

        if flag_face_detect:
            cv2.putText(img, f"ON", (20,30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

        cv2.imshow("Tello Face Tracking", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('x') or key == ord('q'):
            cv2.destroyAllWindows()
            break 
        elif key == ord('u'):
             tello.move_up(30)
        elif key == ord('1'): # on
            flag_face_detect = True
        elif key == ord('2'): # off
            flag_face_detect = False
            tello.send_rc_control(0,0,0,0)

        # 5초 이상이면, 명령어 모드 전송으로 지속적으로 작동하도록 수행
        current_time = time.time()	
        if current_time - pre_time > span_sec :	
            tello.send_command_without_return("command")
            pre_time = current_time
                                
except( KeyboardInterrupt, SystemExit):    # Ctrl+c 적용가능
		print( "SIGINT 감지" )

# Tello Drone의 영상 전송 OFF
tello.streamoff()

tello.land()

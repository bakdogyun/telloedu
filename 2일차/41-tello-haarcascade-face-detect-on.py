"""
Tello Drone의 전송 영상에 얼굴 탐지 및 트래킹(haarcascade)
- send_rc_control()로 x,y,z방향으로 이동

<참고>
https://github.com/hsgucci404/tello/blob/master/Tello_CV_face/main.py
"""

from djitellopy import Tello
import numpy as np
import cv2, time

color = (255,255,0)
color2 = (0,0,255)

span_sec = 5.0 # 5.0 sec
flag_face_detect = False # 초기설정

# Tello Drone 객체 생성 및 연결
tello = Tello()
tello.connect()

# 영상전송 모드 ON
tello.streamon()

# Tello Drone에서 이미지 캡처를 위한 Thread 구동
# tello.set_video_fps(Tello.FPS_15)
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

cascPath = 'haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# 프레임수 카운트 및 얼굴인식 결과 저장
cnt_frame = 0
pre_faces = []	

try:
    while (True):
        img = frame_read.frame

        # 720x960 -> 360x480
        swidth, sheight = 480, 360
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        small_image = cv2.resize(img, dsize=(swidth,sheight) )
        scx, scy = swidth//2, sheight//2 # 스크린의 중심점
        
        cv_image = small_image

        # 화면의 중심을 교차하는 x,y축 그리기
        cv2.line(cv_image,(0,scy),(swidth,scy), color2, 1) # x축
        cv2.line(cv_image,(scx,0),(scx,sheight),color2, 1) # y축

        if flag_face_detect:
            cv2.putText(cv_image, f"ON", (20,30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

        if cnt_frame >= 5: # 3frame 마다 얼굴을 인식
            gray = cv2.cvtColor(small_image, cv2.COLOR_RGB2GRAY)
            gray = cv2.equalizeHist( gray )
            
            faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))
            
            pre_faces = faces
            cnt_frame = 0
            
        # 얼굴영역 탐지
        if len(pre_faces) == 0:
            pass
        else:
            x = pre_faces[0][0]
            y = pre_faces[0][1]
            w = pre_faces[0][2]
            h = pre_faces[0][3]
            
            cx = int( x + w/2 )
            cy = int( y + h/2 )

            # 얼굴영역을 표시
            cv2.rectangle(cv_image, (x, y), (x+w, y+h), color, 2)
            cv2.circle(cv_image, (cx,cy), 5, color, cv2.FILLED)
      
            if flag_face_detect:  # 얼굴이 탐지되고, 트래킹 모드가 ON이면
                a = b = c = d = 0

                # 목표 위치와의 차이에 gain을 곱한다 (이미지 크기는 480x360)
                dx = 0.4 * (240 - cx) # 화면중심과의 차이 x
                dy = 0.4 * (180 - cy) # 화면중심과의 차이 y
                dw = 0.7 * (100 - w)  # 기준 얼굴 크기 100px와의 차이

                dx = -dx # 제어 방향이 반대였기 때문에 -1을 곱하여 반대

                print('dx=%f  dy=%f  dw=%f'%(dx, dy, dw) )

                # 좌/우방향의 미작동 구간 설정(20cm)
                d = 0.0 if abs(dx) < 20.0 else dx  
                d =  100 if d >  100.0 else d
                d = -100 if d < -100.0 else d

                # 앞/뒤 방향의 미작동 구간 설정 (20cm)
                b = 0.0 if abs(dw) < 10.0 else dw
                b =  100 if b >  100.0 else b
                b = -100 if b < -100.0 else b

                # 위/아래 방향의 미작동 구간 설정 (20cm)
                c = 0.0 if abs(dy) < 20.0 else dy
                c =  100 if c >  100.0 else c
                c = -100 if c < -100.0 else c
                
                print("send_rc >> (LR=%s,FB=%s,UD=%s,YY=%s)"%(int(a), int(b), int(c), int(d)))
                # RC명령어 전송
                tello.send_rc_control(int(a), int(b), int(c), int(d))

        cnt_frame += 1
        
        cv2.imshow("Tello Face Tracking", cv_image)

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
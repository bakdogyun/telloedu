from djitellopy import Tello
from cvzone.FaceDetectionModule import FaceDetector 
import cv2, time

color = (255,255,0)
color2 = (0,0,255)

span_sec = 5.0 # 5.0 sec
flag_face_detect = False # 초기설정

# Tello Drone 객체 생성 및 연결
tello = Tello()
tello.connect()

# 얼굴인식을 위한 cvzone 객체 생성
detector = FaceDetector() 

# 영상전송 모드 ON
tello.streamon()

frame_read = tello.get_frame_read()


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


            # 얼굴탐지 사각형영역의 코위치에서 이미지의 가운데까지의 픽셀차이
            dx = fcx - cx
            dy = fcy - cy

            if flag_face_detect:
                # x,y,z축 상에서 이동 거리와 속도 계산
                a = b = c = d = 0

                # 목표 위치와의 차이에 gain을 곱한다 (이미지 크기는 480x360)
                dx = 0.4 * (240 - fcx) # 화면중심과의 차이 x
                dy = 0.4 * (180 - fcy) # 화면중심과의 차이 y
                dw = 0.7 * (100 - fw)  # 기준 얼굴 크기 100px와의 차이

                dx = -dx # 제어 방향이 반대였기 때문에 -1을 곱하여 반대

                # 좌/우방향의 미작동 구간 설정(20cm)
                d = 0.0 if abs(dx) < 20.0 else dx  
                d =  100 if d >  100.0 else d
                d = -100 if d < -100.0 else d

                # 앞/뒤 방향의 미작동 구간 설정 (20cm)
                b = 0.0 if abs(dw) < 20.0 else dw
                b =  100 if b >  100.0 else b
                b = -100 if b < -100.0 else b

                # 위/아래 방향의 미작동 구간 설정 (20cm)
                c = 0.0 if abs(dy) < 20.0 else dy
                c =  100 if c >  100.0 else c
                c = -100 if c < -100.0 else c
                
              
                tello.send_rc_control(int(a), int(b), int(c), int(d))



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
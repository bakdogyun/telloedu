"""
Tello Drone의 전송 영상에 얼굴 탐지 및 좌표 표시
- 얼굴 영역과 확률, 관련 정보 표시
"""

from djitellopy import Tello
from cvzone.FaceDetectionModule import FaceDetector 
import cv2

color = (255,255,0)
color2 = (0,0,255)

# Tello Drone 객체 생성 및 연결
tello = Tello()
tello.connect()

# 얼굴인식을 위한 cvzone 객체 생성
detector = FaceDetector() 

# 영상전송 모드 ON
tello.streamon()

# Tello Drone에서 이미지 캡처를 위한 Thread 구동
frame_read = tello.get_frame_read()

# 배터리와 이미지 기본 정보 표시
print("batter_status = ", tello.get_battery())
print(frame_read.frame.shape)

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

        # 원래 cvzone에서는 bbox와 확률을 표시하고 있으나, 여기서는 bbox만 표시
        img = cv2.rectangle(img, bbox, color, 2)
        cv2.circle(img, center, 5, color, cv2.FILLED)

        # 화면의 중심에서 얼굴의 중심점까지 선그리기
        cv2.line(img,(0,cy),(width,cy), color2, 1) # x축
        cv2.line(img,(cx,0),(cx,height),color2, 1) # y축
        cv2.line(img,(cx,cy) ,center, color,2)

        # 얼굴탐지 사각형영역의 코위치에서 이미지의 가운데까지의 픽셀차이
        dx = center[0] - cx
        dy = center[1] - cy

        # 좌표 표시 (얼굴중심좌표),(화면중심에서 얼굴중심간의 차이 pixel)
        cv2.putText(img, f'({center[0]},{center[1]}),({dx}px,{dy}px)',
                            (bbox[0], (bbox[1]+bbox[3])+20), cv2.FONT_HERSHEY_PLAIN,
                            1, color, 2)

        # 얼굴영역의 width pixel수 표시
        cv2.putText(img, f'{bbox[3]}px',
                                (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_PLAIN,
                                2, color, 2)

    cv2.imshow("Tello Face Detection", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x') or key == ord('q'):
        cv2.destroyAllWindows()
        break 


# Tello Drone의 영상 전송 OFF
tello.streamoff()
"""
Tello Drone의 전송 영상에 얼굴 탐지
- 얼굴 영역과 확률 표시
"""

from djitellopy import Tello
from cvzone.FaceDetectionModule import FaceDetector 
import cv2

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

    img, bboxs = detector.findFaces(img) 
    if bboxs: 
        # bboxInfo - "id","bbox","score","center" 
        center = bboxs[0]["center"] 
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED) 

    cv2.imshow("Tello Face Detection", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x') or key == ord('q'):
        cv2.destroyAllWindows()
        break 


# Tello Drone의 영상 전송 OFF
tello.streamoff()
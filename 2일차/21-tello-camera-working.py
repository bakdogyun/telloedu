"""
Tello Drone을 노트북/PC와 와이파이(Wi-Fi)로 연결 및 영상전송 점검
- Tello Drone의 와이파이 주소 접속
"""


from djitellopy import Tello
import cv2

# Tello Drone 객체 생성 및 연결
tello = Tello()
tello.connect()

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

    cv2.imshow("Tello Drone Camera", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x') or key == ord('q'):
        cv2.destroyAllWindows()
        break 


# Tello Drone의 영상 전송 OFF
tello.streamoff()



        




"""
Tello Drone에서 손가락을 구분하여 손포즈 인식 및 제어 (13개 Signs)
- Shaka, ILVU, OK
+ Victory, Thumb Up, Pinky
+ Rock, One, Two, Three, Four, Five
"""

from djitellopy import Tello
from cvzone.FaceDetectionModule import FaceDetector 
import cvzone.HandTrackingModule as hand
import cv2, time

color = (255,255,0)
command_mode = False
command_set =   ["One","Victory","ILVU","Shaka","Pinky","Three","Four","ThumbUp"]

# 손가락의 top index
tipids= [4, 8, 12, 16, 20] 
hand_digits = ['Rock','One','Two','Three','Four','Five']

# Tello Drone 객체 생성 및 연결
tello = Tello()
tello.connect()

# 손인식을 위한 cvzone 객체 생성
detector = hand.HandDetector(detectionCon=0.8, maxHands=2)

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

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    
    # 손가락의 개방여부를 확인
    # 엄지 손가락의 경우, 아래보다는 항상 위쪽에 위치 4번
    if hands:
        for hd in hands:  # 최대 2개의 손을 인식
            lmList = hd["lmList"] # landmark list
            x,y,width,height = hd["bbox"]

            if len(lmList) != 0: # lmList의1번째값이 1값
                fingers = []

                # 엄지의 경우, x축의 값으로 체크
                thumb_open = 0 # false
                if hd["type"] == 'Right':
                    if lmList[tipids[0]][0] > lmList[tipids[0]-1][0]:  # x좌표값 기준
                        thumb_open = 1
                else:  #  왼손의 경우 
                    if lmList[tipids[0]][0] < lmList[tipids[0]-1][0]:  # x좌표값 기준
                        thumb_open = 1
                fingers.append(thumb_open)
            
                # 엄지를 제외한 다른 손가락을 체크
                for i in range(1,len(tipids)):
                    finger_open = 0
                    if lmList[tipids[i]][1] < lmList[tipids[i]-2][1]:  # y 좌표값 기준
                        finger_open = 1
                    fingers.append(finger_open)
                
                #  손가락으로 표시한 값 출력하기
                nFingers = sum(fingers)
                
                #print("nFingers=",nFingers)
                #print(fingers)

                # 엄지 손가락의 오픈 여부 체크
                isThumbOpen=False
                if fingers[0] > 0:
                    isThumbOpen=True

                # 손가락이 하나도 펴지 않았다면 Rock/Zero, 모두 펼쳐져있다면 Five
                if nFingers == 0:
                    handpose_marker = hand_digits[nFingers] 
                    command_mode = True # ROCK   
                elif nFingers == 5:
                    handpose_marker = hand_digits[nFingers]
                else:
                    if not isThumbOpen: # 엄지 손가락이 열리지 않았다면 (1,2,3,4)
                        if nFingers > 0 and nFingers < 5:
                            handpose_marker = hand_digits[nFingers]
                            if (nFingers == 1) and (fingers[4] > 0):
                                handpose_marker = "Pinky"
                            if (nFingers == 2) and ((fingers[1]+fingers[2]) > 1) :
                                handpose_marker = "Victory"
                    else: # 엄지손가락 오픈
                        if nFingers == 1:
                            handpose_marker = "ThumbUp"
                        else:
                            if nFingers > 0 and nFingers < 5:
                                handpose_marker = hand_digits[nFingers]
                                # ILVU, Shaka, OK
                                if (nFingers == 2) and (fingers[0]+fingers[4] > 1):
                                    handpose_marker = "Shaka"
                                if (nFingers == 3) :
                                    if ((fingers[2]+fingers[3]) == 0):
                                        handpose_marker = "ILVU"
                    
                    #OK
                    if (nFingers > 2) and (fingers[2]+fingers[3]+fingers[4] > 2):
                            length, info = detector.findDistance(lmList[4][0:2], lmList[8][0:2])
                            if length < 50.0:
                                handpose_marker = "OK"
                                #command_mode = True
            
                # handpose_marker를 표시
                cv2.putText(img, f"{handpose_marker}", (x, y+height), 
                                cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                
                if command_mode:
                    cv2.putText(img, f"ON", (20,20), 
                                cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                
      
        # Tello Drone 제어하기
        if handpose_marker in command_set:
            if command_mode :
                if handpose_marker == "One":
                    print("ONE>move up")
                    #tello.move_up(30)
                elif handpose_marker == "Victory" :
                    print("VICTORY>move down")
                    #tello.move_down(30)
                elif handpose_marker == "Three" :
                    print("THREE>move forward")
                    #tello.move_forward(30)
                elif handpose_marker == "Four" :
                    print("FOUR>move backward")
                    #tello.move_back(30)
                elif handpose_marker == "ThumbUp" :
                    print("THUMBUP>move right")
                    #tello.move_right(30)
                elif handpose_marker == "Pinky" :
                    print("PINKY>move left")
                    #tello.move_left(30)
                elif handpose_marker == "Shaka" :
                    print("SHAKA>rotate clockwise")
                    #tello.rotate_clockwise(90)
                elif handpose_marker == "ILVU" :
                    print("ILV> rotate count clockwise")
                    #tello.rotate_counter_clockwise(90)

                # command 모드 설정을 reset
                command_mode = False
                time.sleep(0.1)
            
                           
    # 이미지 표시하기
    cv2.imshow("Hand Pose Image", img)

    key = cv2.waitKey(1) & 0xFF
    if  key == ord('q') or key == ord('x'):
        cv2.destroyAllWindows()
        break


# Tello Drone의 영상 전송 OFF
tello.streamoff()

"""
손가락을 구분하여 손포즈 인식 (4개의 숫자 인식)
- 1,2,3,4
"""

import cv2
import cvzone.HandTrackingModule as hand

color = (255,255,0)

cap = cv2.VideoCapture(0)
detector = hand.HandDetector(detectionCon=0.8, maxHands=2)

# 손가락의 top index
tipids= [4, 8, 12, 16, 20] 
hand_digits = ['Rock','One','Two','Three','Four','Five']

if not cap.isOpened(): 
    print("camera open failed") 
    exit() 

while True:
    # Get image frame
    ret, img = cap.read()
    if not ret: 
        print("Can't read camera") 
        break  

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
                
                print("nFingers=",nFingers)
                print(fingers)

                # 엄지 손가락의 오픈 여부 체크
                isThumbOpen=False
                if fingers[0] > 0:
                    isThumbOpen=True

                # 손가락이 하나도 펴지 않았다면 Rock/Zero, 모두 펼쳐져있다면 Five
                if nFingers == 0:
                    handpose_marker = hand_digits[nFingers]    
                elif nFingers == 5:
                    handpose_marker = hand_digits[nFingers]
                else:
                    if not isThumbOpen: # 엄지 손가락이 열리지 않았다면 (1,2,3,4)
                        if nFingers > 0 and nFingers < 5:
                            handpose_marker = hand_digits[nFingers]
                    else:
                        handpose_marker = hand_digits[nFingers]
                
                # handpose_marker를 표시
                cv2.putText(img, f"{handpose_marker}", (x, y+height), 
                                cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                
    # 이미지 표시하기
    cv2.imshow("Hand Pose Image", img)

    key = cv2.waitKey(2) & 0xFF
    if  key == ord('q') or key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
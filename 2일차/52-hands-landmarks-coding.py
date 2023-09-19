"""
PC/노트북의 카메라로부터 입력된 영상에서 손영역/랜드마크/손유형 식별
- 손의 영역 표시
- 손의 유형 : 왼손/오른손
- 손의 랜드마크
"""

from cvzone.HandTrackingModule import HandDetector 
import cv2, cvzone
import mediapipe as mp

color = (255,255,0)
color2 = (255,0,255)

# landmark drawing을 위한 클래스 설정
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

cap = cv2.VideoCapture(0) 
detector = HandDetector(detectionCon=0.8, maxHands=2) 

if not cap.isOpened(): 
    print("camera open failed") 
    exit() 

while True: 
    ret, img = cap.read()
    
    if not ret: 
        print("Can't read camera") 
        break  

    # 손과 손의 랜드마크 식별
    hands = detector.findHands(img,draw=False)
    if hands:
        hand1 = hands[0] 
        lmList1 = hand1["lmList"] # List of 21 Landmark points 
        bbox1 = hand1["bbox"] # Bounding box info x,y,w,h 
        centerPoint1 = hand1['center'] # center of the hand cx,cy 
        handType1 = hand1["type"] # Handtype Left or Right 
        
        #  손영역과 중심점, 손유형표시
        img = cv2.rectangle(img, bbox1, color, 2)
        cv2.circle(img, centerPoint1, 5, color, cv2.FILLED)
        cv2.putText(img, f'{handType1}',
                            (bbox1[0], (bbox1[1]-10)), cv2.FONT_HERSHEY_PLAIN,
                            2, color, 2)


        if len(hands) == 2:
            hand2 = hands[1] 
            lmList2 = hand2["lmList"] # List of 21 Landmark points 
            bbox2 = hand2["bbox"] # Bounding box info x,y,w,h 
            centerPoint2 = hand2['center'] # center of the hand cx,cy 
            handType2 = hand2["type"] # Hand Type "Left" or "Right"

            #  손영역과 중심점, 손유형표시
            img = cv2.rectangle(img, bbox2, color2, 2)
            cv2.circle(img, centerPoint2, 5, color2, cv2.FILLED)
            cv2.putText(img, f'{handType2}',
                            (bbox2[0], (bbox2[1]-10)), cv2.FONT_HERSHEY_PLAIN,
                            2, color2, 2)


    # Display 
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q') or key == ord('x'): 
        break


cap.release() 
cv2.destroyAllWindows()
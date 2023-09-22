"""
PC/노트북의 카메라로부터 입력된 영상에서 손영역 표시
"""

from cvzone.HandTrackingModule import HandDetector 
import cv2, cvzone

cap = cv2.VideoCapture(1) 
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
    handsList = hands[0]
    if handsList:
        hand1 = handsList[0] 
        bbox1 = hand1["bbox"] # Bounding box info x,y,w,h 

        cvzone.cornerRect(img, bbox1)

        if len(handsList) == 2:
            hand2 = handsList[1] 
            bbox2 = hand2["bbox"] # Bounding box info x,y,w,h

            cvzone.cornerRect(img, bbox2)

    # Display 
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q') or key == ord('x'): 
        break


cap.release() 
cv2.destroyAllWindows()
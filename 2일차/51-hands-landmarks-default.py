"""
PC/노트북의 카메라로부터 입력된 영상에서 손영역/랜드마크/손유형 식별
- 손의 영역 표시
- 손의 유형 : 왼손/오른손
- 손의 랜드마크
"""

from cvzone.HandTrackingModule import HandDetector 
import cv2

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

    # 손과 손의 랜드마크 식별 - findHands이 draw=True로 설정
    hands = detector.findHands(img)
    
    # Display 
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q') or key == ord('x'): 
        break


cap.release() 
cv2.destroyAllWindows()
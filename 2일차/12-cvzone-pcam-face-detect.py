from cvzone.FaceDetectionModule import FaceDetector 
import cv2

cap = cv2.VideoCapture(1)
detector = FaceDetector() 

if not cap.isOpened(): 
    print("camera open failed") 
    exit() 

while (True): 
    ret, img = cap.read()
    if not ret: 
        print("Can't read camera") 
        break 

    img, bboxs = detector.findFaces(img) 
    if bboxs: 
        # bboxInfo - "id","bbox","score","center" 
        center = bboxs[0]["center"] 
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED) 

    # 영상 화면은 좌우가 바뀐모습으로 표시
    cv2.imshow("Face Detection Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x') or key == ord('q'): 
        break 

cap.release() 
cv2.destroyAllWindows()
import cv2 

cap = cv2.VideoCapture(1) 

if not cap.isOpened(): 
    print("camera open failed") 
    exit() 

while (True): 
    ret, img = cap.read()
    if not ret: 
        print("Can't read camera") 
        break 

    # 영상 화면은 좌우가 바뀐모습으로 표시
    cv2.imshow("Notebook_Camera", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('x') or key == ord('q'): 
        break 

cap.release() 
cv2.destroyAllWindows()
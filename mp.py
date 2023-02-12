import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection.FaceDetection()
mp_face_keypoint = mp.solutions.face_detection
mp_face_process = mp_face_detection.process
mp_drawing = mp.solutions.drawing_utils

# For static images:
IMAGE_FILES = ['.보나.jpeg']
image = cv2.imread('./보나.jpeg')

img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
results = mp_face_detection.process(img)

annotated_image = image.copy()
for detection in results.detections:
    print('Nose tip:')
    print(mp_face_keypoint.get_key_point(
        detection, mp_face_keypoint.FaceKeyPoint.NOSE_TIP))
    mp_drawing.draw_detection(annotated_image, detection)
cv2.imwrite('./hi.jpeg',annotated_image)
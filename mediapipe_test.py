import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# For static images:
IMAGE_FILES = ['/home/ts/Documents/DMS/eye_28_label/images/images/000015.jpg']
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
        continue
    annotated_image = image.copy()
    left_landmark = [476]
    # left_landmark = [263,249,390, 373, 374, 380, 381, 382, 362, 466, 388, 387, 386, 385, 384, 398]
    right_landmark =[33, 7, 163, 144, 145, 153, 154, 155, 133, 246, 161, 160, 159, 158, 157, 173]
    left_iris = [474, 475, 476, 477]
    right_iris = [469, 470, 471, 472]
    keypoints = []
    for face_landmarks in results.multi_face_landmarks:
        for i in range(len(left_landmark)):
            x = int(face_landmarks.landmark[left_landmark[i]].x *image.shape[1])
            y = int(face_landmarks.landmark[left_landmark[i]].y * image.shape[0])
            keypoints.append((x,y))
    cv2.circle(annotated_image,keypoints[0],3,(255,0,0))
    cv2.imshow("show",annotated_image)
    key = cv2.waitKey(0)
    print(key)
    if key == 110:
        print('next')

    cv2.imwrite('/home/ts/Documents/DMS/eye_28_label/images/images/' + str(1000) + '.png', annotated_image)

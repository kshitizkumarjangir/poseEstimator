import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

holistic = mp_holistic.Holistic(min_detection_confidence=0.5,
                                min_tracking_confidence=0.5)

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print('Ignoring empty camera frame.')
        continue    # for image or video set it to break(end of file)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = holistic.process(image)

    # Draw landmark annotation on the image
    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_style.get_default_face_mesh_contours_style()
    )

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec= mp_drawing_style.get_default_pose_landmarks_style()
    )

    # Flip the image horizontally for a selfie-view display
    cv2.imshow("Mediapipe Holistic", cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()

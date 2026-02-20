import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

#  forehead and cheeks 
FOREHEAD_IDX = 10
LEFT_CHEEK_IDX = 234
RIGHT_CHEEK_IDX = 454

def get_face_rois(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    h, w, _ = frame.shape
    roi_dict = {}

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        try:
            forehead = landmarks[FOREHEAD_IDX]
            left_cheek = landmarks[LEFT_CHEEK_IDX]
            right_cheek = landmarks[RIGHT_CHEEK_IDX]

            roi_dict['forehead'] = (int(forehead.x * w), int(forehead.y * h))
            roi_dict['left_cheek'] = (int(left_cheek.x * w), int(left_cheek.y * h))
            roi_dict['right_cheek'] = (int(right_cheek.x * w), int(right_cheek.y * h))

        except IndexError:
            pass

    return roi_dict

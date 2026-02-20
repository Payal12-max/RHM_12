import cv2
import mediapipe as mp
import numpy as np

class FatigueAnalyzer:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]  
        self.RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]  
        self.blink_counter = 0
        self.ear_history = []
        self.in_blink = False
        self.cooldown = 0  
        self.EAR_THRESH = 0.21
        self.COOLDOWN_FRAMES = 5

    def _eye_aspect_ratio(self, landmarks, indices, image_w, image_h):
        p = [(int(landmarks[i].x * image_w), int(landmarks[i].y * image_h)) for i in indices]
        A = np.linalg.norm(np.array(p[1]) - np.array(p[5]))
        B = np.linalg.norm(np.array(p[2]) - np.array(p[4]))
        C = np.linalg.norm(np.array(p[0]) - np.array(p[3]))
        ear = (A + B) / (2.0 * C)
        return ear

    def analyze(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        fatigue_metrics = {"EAR": None, "BlinkRate": None}

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            left_ear = self._eye_aspect_ratio(landmarks, self.LEFT_EYE_IDX, w, h)
            right_ear = self._eye_aspect_ratio(landmarks, self.RIGHT_EYE_IDX, w, h)
            ear = (left_ear + right_ear) / 2.0
            self.ear_history.append(ear)

            if self.cooldown > 0:
                self.cooldown -= 1

            if ear < self.EAR_THRESH and not self.in_blink and self.cooldown == 0:
                self.blink_counter += 1
                self.in_blink = True
                self.cooldown = self.COOLDOWN_FRAMES  
            elif ear >= self.EAR_THRESH:
                self.in_blink = False

            fatigue_metrics["EAR"] = ear
            fatigue_metrics["BlinkRate"] = self.blink_counter

        return fatigue_metrics


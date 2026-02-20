import cv2
import time

def get_camera_stream(index=0):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Camera could not be opened. Check index or drivers.")
    return cap

def estimate_fps(cap, frame_count=100):
    count = 0
    start = time.time()
    while count < frame_count:
        ret, _ = cap.read()
        if not ret:
            break
        count += 1
    end = time.time()
    fps = count / (end - start)
    return fps

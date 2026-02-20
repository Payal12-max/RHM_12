import cv2
import time
import numpy as np
from camera_acquisition import get_camera_stream
from roi_manager import get_face_rois
from roi_signal_tracker import ROISignalTracker
from signal_processing import SignalProcessor

FPS = 20
tracker = ROISignalTracker(buffer_seconds=30, fps=FPS)
processor = SignalProcessor(fps=FPS)
cap = get_camera_stream()

FONT = cv2.FONT_HERSHEY_SIMPLEX
last_calc_time = time.time()
hr = None
hrv = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi_points = get_face_rois(frame)
    roi_green_values = {}

    for label, (x, y) in roi_points.items():
        if y < frame.shape[0] and x < frame.shape[1]:
            green_value = frame[y, x, 1]  # Green channel
            roi_green_values[label] = green_value
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(frame, label, (x+5, y-5), FONT, 0.5, (0, 255, 0), 1)

    tracker.update(roi_green_values)
    best_roi, _ = tracker.get_best_roi()
    best_signal = tracker.roi_buffers[best_roi]

    now = time.time()
    if now - last_calc_time > 5:
        hr, hrv = processor.calculate_hr_and_hrv(list(best_signal))
        last_calc_time = now

    #  metrics
    cv2.putText(frame, f"Best ROI: {best_roi}", (10, 30), FONT, 0.8, (0, 0, 255), 2)
    if hr:
        cv2.putText(frame, f"HR: {hr:.1f} BPM", (10, 60), FONT, 0.7, (255, 255, 255), 2)
    if hrv:
        cv2.putText(frame, f"HRV (SDNN): {hrv:.1f} ms", (10, 90), FONT, 0.7, (255, 255, 255), 2)

    cv2.imshow("Live HR/HRV Monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
from camera_acquisition import get_camera_stream
from roi_manager import get_face_rois
from roi_signal_tracker import ROISignalTracker

tracker = ROISignalTracker(buffer_seconds=30, fps=20)
cap = get_camera_stream()

FONT = cv2.FONT_HERSHEY_SIMPLEX

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

    # Feed green values into buffer
    tracker.update(roi_green_values)

    #  best ROI every frame
    best_roi, snr_scores = tracker.get_best_roi()
    cv2.putText(frame, f"Best ROI: {best_roi}", (10, 30), FONT, 0.8, (0, 0, 255), 2)

    y_offset = 60
    for roi, snr in snr_scores.items():
        text = f"{roi}: SNR={snr:.2f}"
        cv2.putText(frame, text, (10, y_offset), FONT, 0.6, (100, 255, 255), 1)
        y_offset += 25

    cv2.imshow("RHM ROI SNR Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


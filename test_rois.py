import cv2
from camera_acquisition import get_camera_stream
from roi_manager import get_face_rois

cap = get_camera_stream()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi_points = get_face_rois(frame)
    for label, (x, y) in roi_points.items():
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.putText(frame, label, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("FaceMesh ROI Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

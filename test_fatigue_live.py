import cv2
from camera_acquisition import get_camera_stream
from fatigue_analysis import FatigueAnalyzer

FONT = cv2.FONT_HERSHEY_SIMPLEX
analyzer = FatigueAnalyzer()
cap = get_camera_stream()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fatigue = analyzer.analyze(frame)
    ear = fatigue.get("EAR")
    blinks = fatigue.get("BlinkRate")

    if ear is not None:
        cv2.putText(frame, f"EAR: {ear:.3f}", (10, 30), FONT, 0.8, (0, 255, 255), 2)
    if blinks is not None:
        cv2.putText(frame, f"Blinks: {blinks}", (10, 60), FONT, 0.8, (255, 255, 0), 2)

    cv2.imshow("Fatigue Monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

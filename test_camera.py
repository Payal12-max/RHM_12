
import cv2
import camera_acquisition

cap = camera_acquisition.get_camera_stream()
fps = camera_acquisition.estimate_fps(cap)
print(f"Camera FPS: {fps:.2f}")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Live Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

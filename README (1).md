# Remote Hemodynamic Monitor (RHM )

**RHM ** is a real-time, non-contact, camera-based system that extracts Heart Rate (HR), Heart Rate Variability (HRV), and fatigue metrics (EAR, BlinkRate) from facial video using computer vision and signal processing.

It streams this data over **UDP sockets** every 5 seconds to support Mixed Reality (MR) overlays and IoT integration.

---

## ✅ Features

- Non-contact photoplethysmography (rPPG)
- Adaptive ROI selection (forehead, cheeks)
- Real-time HR and HRV estimation
- Eye Aspect Ratio (EAR) + Blink detection for fatigue
- Lightweight socket streamer (UDP)
- Designed for low-end hardware (i7 + webcam)

---

## 📦 Directory Structure

```
RHM_3.0_UDP/
├── camera_acquisition.py
|   client_test.py
|   fatigue_analysis.py
|   main_controller.py
|   mini_socket_test.py
|   README.md
|   requirements.txt
|   roi_manager.py
|   roi_signal_tracker.py
|   session_20251115_1439.csv
|   signal_processing.py
|   streaming.py
|   test_camera.py
|   test_fatigue_live.py
|   test_live_hr_hrv.py
|   test_rois.py
|   test_snr_switcher.py
|   validate_rhm_stream.py

---

##  Installation

1. Install Python 3.10+
2. Create virtual environment (optional)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

##  How to Run

In one terminal:
```bash
python main_controller.py
```

In another terminal:
```bash
python client_test.py
```

To log data for validation:
```bash
python validate_rhm_stream.py
```

---

##  Output Format (UDP JSON)

Every 5 seconds, the system sends:
```json
{
  "timestamp": 1700000000.12,
  "HR": 93.4,
  "HRV": 182.7,
  "EAR": 0.283,
  "BlinkRate": 21,
  "ROI": "right_cheek"
}
```

---

##  Use Cases

- MR/AR overlays for clinicians
- Passive fatigue/stress monitoring
- IoT-based cognitive state logging
- Academic research in human-computer interaction

---

## Contact

This project is designed for research collaboration . Contributions are welcome.

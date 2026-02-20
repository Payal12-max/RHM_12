import socket
import json
import csv
import time
import os
from datetime import datetime

PORT = 5005
LOG_DURATION = 60 
MASTER_FILE = "per_second_summary.csv" 

print(f"[Validator] Listening for {LOG_DURATION}s. Logging 1-second averages...")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.settimeout(1.0)

start_time = time.time()
data_buffer = [] 
file_exists = os.path.isfile(MASTER_FILE)

with open(MASTER_FILE, mode="a", newline="") as csvfile:
    fieldnames = ["timestamp", "second_elapsed", "HR", "HRV", "EAR", "BlinkRate", "ROI"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    if not file_exists:
        writer.writeheader()

    last_second = 0

    while True:
        try:
            data, _ = sock.recvfrom(2048)
            msg = json.loads(data.decode())
        
            entry = {"type": msg.get("stream")}
            if msg.get("stream") == "hr":
                entry["HR"] = msg["values"][0]
                entry["HRV"] = msg["metadata"].get("hrv")
                entry["ROI"] = msg["metadata"].get("roi_loc")
            elif msg.get("stream") == "fatigue":
                entry["EAR"] = msg["values"][0]
                entry["BlinkRate"] = msg["metadata"].get("blink_rate")
            
            data_buffer.append(entry)

        except socket.timeout:
            pass  

        elapsed = int(time.time() - start_time)

        if elapsed > last_second:
            hr_s = [x["HR"] for x in data_buffer if "HR" in x]
            hrv_s = [x["HRV"] for x in data_buffer if "HRV" in x]
            ear_s = [x["EAR"] for x in data_buffer if "EAR" in x]
            roi_s = [x["ROI"] for x in data_buffer if "ROI" in x]
            blink_s = [x["BlinkRate"] for x in data_buffer if "BlinkRate" in x]

            def get_avg(vals):
                return round(sum(vals) / len(vals), 2) if vals else ""

            row = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "second_elapsed": last_second,
                "HR": get_avg(hr_s),
                "HRV": get_avg(hrv_s),
                "EAR": get_avg(ear_s),
                "BlinkRate": blink_s[-1] if blink_s else "",
                "ROI": roi_s[-1] if roi_s else ""
            }

            
            if any([row["HR"], row["EAR"]]):
                writer.writerow(row)
                csvfile.flush()
                print(f"Sec {last_second} | HR: {row['HR']} | EAR: {row['EAR']}")

      
            data_buffer = []
            last_second = elapsed

        if elapsed >= LOG_DURATION:
            break

print(f"\n--- 60-Second Detailed Log Saved to {MASTER_FILE} ---")
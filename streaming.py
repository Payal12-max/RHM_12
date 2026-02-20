import socket
import json
import time

# CONFIGURATION
# 127.0.0.1 is for testing on your laptop. 
# Change this to Alex's IP when deploying in the lab.
UDP_IP = "127.0.0.1"
UDP_PORT = 5005  # Standardized port for the lab
DEVICE_ID = "rhm_cam_01"

class SocketStreamer:
    def __init__(self, host=UDP_IP, port=UDP_PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allow reusing the address to avoid "Address already in use" errors
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.target = (self.host, self.port)
        self.running = False
        print(f"[UDPStreamer] Targeted to {self.host}:{self.port}")

    def start(self):
        self.running = True

    def send_packet(self, stream_type, values, metadata=None):
        """
        Builds the standard 'Lab-Ready' packet with timestamps.
        """
        if not self.running:
            return

        # 1. Build the Standard Payload (Matches packet_schema.md)
        payload = {
            "device_id": DEVICE_ID,
            "stream": stream_type,          # e.g., "hr", "fatigue"
            "sample_index": 0,              # You can add a counter here if needed
            "timestamp_utc_ms": int(time.time() * 1000),      # Wall clock for sync
            "timestamp_monotonic_ms": int(time.monotonic() * 1000), # Uptime for lag check
            "values": values if isinstance(values, list) else [values],
            "metadata": metadata or {}
        }
        
        # 2. Send via UDP
        try:
            data = json.dumps(payload).encode('utf-8')
            self.sock.sendto(data, self.target)
        except Exception as e:
            print(f"[UDPError] {e}")

    def stop(self):
        try:
            self.sock.close()
        except Exception:
            pass
        self.running = False
        print("[UDPStreamer] Socket closed.")
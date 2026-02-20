import socket
import json
import datetime

# CONFIGURATION
# 0.0.0.0 means "Listen to ALL traffic coming to this computer"
UDP_IP = "0.0.0.0" 
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"✅ LISTENING for Lab Data on port {UDP_PORT}...")
print(f"   (Press Ctrl+C to stop)")

packet_count = 0

while True:
    try:
        # Receive data (buffer size 65536 is standard max for UDP)
        data, addr = sock.recvfrom(65536)
        
        # Decode the JSON
        pkt = json.loads(data.decode('utf-8'))
        
        packet_count += 1
        
        # Calculate human-readable time from the packet's timestamp
        ts = pkt.get('timestamp_utc_ms', 0) / 1000.0
        time_str = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S.%f')[:-3]
        
        # Print a clean summary row
        # We handle cases where 'values' might be missing or empty
        vals = pkt.get('values', [])
        stream_type = pkt.get('stream', 'unknown')
        device = pkt.get('device_id', 'unknown')
        
        print(f"[{packet_count}] {time_str} | {device} | {stream_type.upper()} | Val: {vals}")
        
    except KeyboardInterrupt:
        print("\nStopping...")
        break
    except Exception as e:
        print(f" Error parsing packet: {e}")
import time
from streaming import SocketStreamer

streamer = SocketStreamer(port=5010)
streamer.start()

print("[Test] Waiting 30 seconds for client...")
time.sleep(30)

print("[Test] Sending dummy payload...")
streamer.send({"HR": 80, "HRV": 55, "BlinkRate": 3})

streamer.stop()

import cv2
import time
import requests
import os
from pathlib import Path

# Config
CAMERA_INDEX = 1 # OBS Virtual Cam
DURATION = 20 # seconds
OUTPUT_DIR = "manual_recordings"
AGENT_URL = "http://localhost:8001/agent"
CAMERA_ID = "cam1_test"
LATITUDE = "12.9716"
LONGITUDE = "77.5946"

def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f"manual_test_{timestamp}.mp4"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Create synthetic video instead of camera
    width, height = 640, 480
    fps = 15.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
    
    import numpy as np
    
    print(f"Generating synthetic video (20s) to {filepath}...")
    
    # Generate 5 seconds of video (enough for test)
    frames_to_generate = int(fps * 5) 
    
    for i in range(frames_to_generate):
        # Create a frame with changing color
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        color_val = (i * 5) % 255
        frame[:] = (0, 0, color_val) # BGR
        
        cv2.putText(frame, f"TEST VIDEO FRAME {i}", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        out.write(frame)
        
    out.release()
    print("Synthetic video generation complete.")

    # Upload
    print(f"Uploading to Agent at {AGENT_URL}...")
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filename, f, 'video/mp4')}
            data = {
                'camera_id': CAMERA_ID,
                'latitude': LATITUDE,
                'longitude': LONGITUDE,
                'event_type': 'Fire'
            }
            response = requests.post(AGENT_URL, files=files, data=data)
            print("Upload Response Code:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    main()

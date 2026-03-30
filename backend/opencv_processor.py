import cv2
import requests

API_URL = "http://127.0.0.1:8000/traffic"

video_path = "traffic_video.mp4"  # your video file

cap = cv2.VideoCapture(video_path)
print("Running...")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize (faster processing)
    frame = cv2.resize(frame, (640, 480))

    # Convert to grayscale (basic processing)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ---- DUMMY LOGIC (replace later) ----
    lanes = {
        "N": 10,
        "S": 5,
        "E": 3,
        "W": 7
    }

    pedestrian = False  # simulate

    data = {
        "intersection_id": "I1",
        "lanes": lanes,
        "pedestrian": pedestrian
    }

    try:
        requests.post(API_URL, json=data)
    except:
        print("Backend not reachable")

    cv2.imshow("Traffic Feed", frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import requests
import time

API_URL = "http://127.0.0.1:8000/traffic/dual"


video_B = "road2.mp4"
video_A = "road1.mp4"

capB = cv2.VideoCapture(video_B)
capA = cv2.VideoCapture(video_A)


fgbgA = cv2.createBackgroundSubtractorMOG2()
fgbgB = cv2.createBackgroundSubtractorMOG2()



def count_vehicles(frame, fgbg):
    mask = fgbg.apply(frame)

    # 🔥 Better noise handling
    mask = cv2.GaussianBlur(mask, (5,5), 0)
    _, mask = cv2.threshold(mask, 180, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 400:   # 🔥 LOWER threshold
            count += 1
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    return count


print("🚦 Dual Road Traffic System Running...")

while True:
    retA, frameA = capA.read()
    retB, frameB = capB.read()

    if not retA or not retB:
        print("Video ended")
        break

    frameA = cv2.resize(frameA, (400, 300))
    frameB = cv2.resize(frameB, (400, 300))

    countA = count_vehicles(frameA, fgbgA)
    countB = count_vehicles(frameB, fgbgB)

    print(f"Road A: {countA} | Road B: {countB}")

    # 🚶 (optional toggle for demo)
    pedestrian = False

    data = {
        "road_A": countA,
        "road_B": countB,
        "pedestrian": pedestrian
    }

    try:
        res = requests.post(API_URL, json=data)
        signal = res.json()
    except:
        print("Backend not reachable")
        signal = {}

    signalA = signal.get("road_A", "RED")
    signalB = signal.get("road_B", "RED")

    # 🟢 Display signals
    cv2.putText(frameA, f"A: {signalA}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,255,0) if signalA=="GREEN" else (0,0,255), 2)

    cv2.putText(frameB, f"B: {signalB}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,255,0) if signalB=="GREEN" else (0,0,255), 2)

    # 📊 Show counts
    cv2.putText(frameA, f"Count: {countA}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(frameB, f"Count: {countB}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # 🖥 Combine both videos
    combined = cv2.hconcat([frameA, frameB])

    cv2.imshow("Smart Traffic System", combined)

    # ⏳ small delay
    time.sleep(1)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capA.release()
capB.release()
cv2.destroyAllWindows()
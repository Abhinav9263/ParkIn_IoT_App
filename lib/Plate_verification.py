import cv2
import easyocr
import requests

# 👇 YOUR CAMERA IP GOES HERE
CAMERA_URL = "http://192.168.31.196:8080/video"  # Replace with your mobile IP cam stream URL
SERVER_URL = "http://192.168.31.45:5000/entry"   # Your Flask server URL

reader = easyocr.Reader(['en'])

cap = cv2.VideoCapture(CAMERA_URL)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Optional: Show live feed
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 🧠 OCR every 1 second or based on condition
    # Resize for speed
    small = cv2.resize(frame, (640, 480))
    result = reader.readtext(small)

    for detection in result:
        text = detection[1]
        if len(text) >= 6 and any(char.isdigit() for char in text):  # Basic check
            plate = text.upper().replace(" ", "").strip()
            print("Detected Plate:", plate)

            # ✅ Send to Flask server for slot verification
            try:
                r = requests.post(SERVER_URL, json={'plate': plate})
                print("Server Response:", r.json())
            except:
                print("Failed to connect to server")

            break  # Only send one plate per frame check

cap.release()
cv2.destroyAllWindows()



#   cd C:\Users\abhin\Flutter\ParkIn_App2\lib
 #   python Plate_verification.py

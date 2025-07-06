# 🚗 ParkIn: AI-Enabled IoT Smart Parking System

ParkIn is an **AI + IoT-powered smart parking system** that uses an **ESP32**, **IP Camera**, and **Flutter App** to automate vehicle entry, booking, gate control, and real-time slot status updates — making parking smarter and seamless.

---

## 🧠 Key Features

- 📸 **Automatic number plate detection** (EasyOCR + IP Camera)
- 🔓 **Servo-controlled gate** via ESP32
- 📍 **Real-time slot booking** via Flutter
- 🔁 **IR & Ultrasonic sensors** for vehicle detection & parking confirmation
- 📡 **ESP32 updates slot status** to Flask server
- 🔥 Firebase (optional) for cloud support

---

## 🧰 Tech Stack

| Layer         | Technology                   |
|---------------|-------------------------------|
| Controller    | ESP32                         |
| AI Detection  | Python + OpenCV + EasyOCR     |
| App           | Flutter (Web/Android)         |
| Backend       | Flask (Python)                |
| Sensors       | IR Sensor, Ultrasonic Sensor  |
| Actuator      | Servo Motor                   |
| DB (optional) | Firebase Realtime Database    |

---

## ⚙️ ESP32 Pin Configuration

| Component            | ESP32 Pin |
|----------------------|-----------|
| IR Sensor            | D12       |
| Ultrasonic Trigger   | D14       |
| Ultrasonic Echo      | D27       |
| Servo Motor          | D5        |
| Green LED            | D18       |
| Red LED              | D19       |

---

## 🚀 Quick Setup Guide

### 1️⃣ Flask + Number Plate Server (Python)

Install dependencies:
```bash
pip install flask flask-cors easyocr opencv-python requests
Run the server:

bash
cd lib
python server.py
Run number plate detection:

bash
python Plate_verification.py
Edit the IP camera stream inside Plate_verification.py:

python
CAMERA_URL = "http://<CAMERA_IP>:8080/video"
2️⃣ Upload ESP32 Code
Use the file esp_code/park_in_esp.ino
Required Libraries (Install in Arduino IDE):

WiFi.h

HTTPClient.h

ServoESP32 ✅ (⚠️ Not the regular Servo lib!)

Update this line in code:

cpp
const char* serverUrl = "http://<YOUR_PC_IP>:5000/update_slot";
Upload to ESP32. Done!

3️⃣ Run Flutter App
bash
flutter clean
flutter pub get
flutter run -d chrome
Update IP in Flutter:

dart
final String apiUrl = "http://<YOUR_PC_IP>:5000/api";
📲 App Flow
IR Sensor detects vehicle

IP camera scans number plate

Flask server verifies it

ESP32 receives signal and opens gate

Ultrasonic sensor confirms parked status

Slot updates sent to server

Flutter UI updates slot color/status

🧪 API Testing (Optional)

curl -X POST http://<your_ip>:5000/entry \
  -H "Content-Type: application/json" \
  -d '{"plate": "WB12AB1234"}'
📝 Future Enhancements
 Firebase integration

 Dynamic ESP mapping

 Role-based access (Admin/User)

 Payment system integration

 Notifications / SMS

📁 Project Structure

ParkIn_App/
├── lib/
│   ├── main.dart
│   ├── parking_screen.dart
│   ├── Plate_verification.py
│   └── server.py
├── esp_code/
│   └── park_in_esp.ino
└── README.md
🤝 Contribution
Feel free to open issues, suggestions, or pull requests.

 Made with ❤️ by Abhinav

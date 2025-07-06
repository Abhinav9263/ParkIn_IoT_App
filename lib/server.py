from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🚗 Slot Data
slots = {
    '1': {'status': 'Available', 'vehicle_number': ''},
    '2': {'status': 'Available', 'vehicle_number': ''},
    '3': {'status': 'Available', 'vehicle_number': ''},
}

# 🔍 Number Plate to Slot Mapping (for auto-entry)
PLATE_TO_SLOT = {
    'WB12AB1234': '1',
    'WB34CD5678': '2',
}

# 🔗 ESP32 Controller Endpoint (common for gate control)
ESP_URL = 'http://192.168.31.89/open'  # 🔁 Replace with your ESP32 IP

# 🟢 Get All Slot Data
@app.route('/api/slots', methods=['GET'])
def get_slots():
    return jsonify(slots)

# 📦 Book a Slot via Flutter App
@app.route('/api/book_slot', methods=['POST'])
def book_slot():
    data = request.get_json()
    slot_id = data.get('slot_id')
    vehicle = data.get('vehicle_number')

    if slot_id in slots and slots[slot_id]['status'] == 'Available':
        slots[slot_id]['status'] = 'Booked'
        slots[slot_id]['vehicle_number'] = vehicle
        return jsonify({'status': 'success', 'slot': slot_id}), 200
    return jsonify({'status': 'failed'}), 400

# 🚘 Auto Entry from IP Cam Number Plate
@app.route('/entry', methods=['POST'])
def entry():
    data = request.get_json()
    plate = data.get('plate', '').strip().upper()

    slot = PLATE_TO_SLOT.get(plate)
    if not slot:
        return jsonify({'status': 'unauthorized'}), 403

    try:
        # 🧠 Allow ESP to open the gate
        requests.get(ESP_URL, timeout=2)

        # 🧾 Update slot info
        slots[slot]['status'] = 'Booked'
        slots[slot]['vehicle_number'] = plate
        return jsonify({'status': 'granted', 'slot': slot}), 200

    except requests.exceptions.RequestException:
        return jsonify({'status': 'esp_error'}), 500

# 🛰️ ESP32 Sends Slot Occupancy Status
@app.route('/update_slot', methods=['POST'])
def update_slot():
    data = request.get_json()
    slot_id = data.get('slot_id')
    status = data.get('status')  # Expected: "Occupied", "Available"

    if slot_id in slots:
        slots[slot_id]['status'] = status
        if status == 'Available':
            slots[slot_id]['vehicle_number'] = ''
        print(f"[INFO] Slot {slot_id} updated to {status}")
        return jsonify({'status': 'updated'}), 200

    return jsonify({'status': 'error', 'message': 'Invalid slot'}), 400

# 🔥 Start Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


#   cd C:\Users\abhin\Flutter\ParkIn_App2\lib
#  python server.py

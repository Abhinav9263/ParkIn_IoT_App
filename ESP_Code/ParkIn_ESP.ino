#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>  // Use the correct servo library for ESP32

// Wi-Fi Credentials
const char* ssid = "AirFiber-e54e72";
const char* password = "XKYX3uQs2f6yFRL6";

// Flask server endpoint
const char* serverUrl = "http://192.168.31.45:5000/update_slot";
const String slotId = "1";  // Slot managed by this ESP

// Pins
#define IR_SENSOR_PIN 12
#define TRIG_PIN 14
#define ECHO_PIN 27
#define SERVO_PIN 5
#define GREEN_LED 18
#define RED_LED 19

Servo gateServo;

void setup() {
  Serial.begin(115200);

  pinMode(IR_SENSOR_PIN, INPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);

  gateServo.setPeriodHertz(50);  // Set PWM frequency
  gateServo.attach(SERVO_PIN, 500, 2400); // Min and max pulse width
  gateServo.write(0); // Initially closed

  // Connect WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected!");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (digitalRead(IR_SENSOR_PIN) == LOW) {
    Serial.println("🚗 Vehicle detected by IR sensor");

    delay(2000); // Simulate time taken for plate verification

    openGate();

    delay(5000); // Time for car to enter

    float distance = measureDistance();
    Serial.print("📏 Ultrasonic Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    if (distance < 30.0) { // Threshold for parked vehicle
      Serial.println("✅ Car parked. Sending to server...");
      sendSlotUpdate("Occupied");

      digitalWrite(RED_LED, HIGH);
    } else {
      Serial.println("❌ Car not properly parked.");
    }

    delay(5000);
    digitalWrite(RED_LED, LOW);
  }

  delay(1000);
}

void openGate() {
  Serial.println("🔓 Opening gate...");
  gateServo.write(90);            // Open gate
  digitalWrite(GREEN_LED, HIGH);
  delay(3000);                    // Keep open for 3 seconds
  gateServo.write(0);             // Close gate
  digitalWrite(GREEN_LED, LOW);
  Serial.println("🔒 Gate closed.");
}

float measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.034 / 2; // in cm
  return distance;
}

void sendSlotUpdate(String status) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"slot_id\":\"" + slotId + "\",\"status\":\"" + status + "\"}";
    int httpResponseCode = http.POST(json);

    if (httpResponseCode > 0) {
      Serial.println("📡 Server response: " + http.getString());
    } else {
      Serial.print("❌ HTTP error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("⚠️ WiFi not connected");
  }
}

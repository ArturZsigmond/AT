// Pin Definitions
const int lightPin = A0;
const int soundPin = A1;
const int proximityPin = 7;

const int ledPin = 8;
const int buzzerPin = 11;

// Thresholds
const int lightThreshold = 300;   // adjust based on your room
const int soundThreshold = 50;

// Alarm timing
const int alarmDuration = 3000;

// State system
int state = 0;
// 0 = idle
// 1 = screaming
// 2 = beeping

unsigned long stateStartTime = 0;

// Beep control
int beepCount = 0;
bool buzzerState = false;
unsigned long lastBeepToggle = 0;

void setup() {
  pinMode(proximityPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // Read sensors
  int lightValue = analogRead(lightPin);
  int soundValue = analogRead(soundPin);
  int proximityValue = digitalRead(proximityPin);

  Serial.print("Light: "); Serial.print(lightValue);
  Serial.print(" | Sound: "); Serial.print(soundValue);
  Serial.print(" | Proximity: "); Serial.println(proximityValue);

  // ===== CHECK CONDITIONS =====
  bool badLight = lightValue < lightThreshold;
  bool badSound = soundValue > soundThreshold;
  bool objectDetected = (proximityValue == LOW);

  bool alarmTrigger = badLight || badSound || objectDetected;

  // ===== STATE 0: IDLE =====
  if (state == 0) {
    digitalWrite(ledPin, LOW);
    digitalWrite(buzzerPin, LOW);

    if (alarmTrigger) {
      state = 1;
      stateStartTime = millis();
      Serial.println("ALARM TRIGGERED → SCREAMING");
    }
  }

  // ===== STATE 1: SCREAMING =====
  else if (state == 1) {
    digitalWrite(ledPin, HIGH);
    digitalWrite(buzzerPin, HIGH);

    if (millis() - stateStartTime >= alarmDuration) {
      state = 2;
      beepCount = 0;
      buzzerState = false;
      lastBeepToggle = millis();
      Serial.println("SCREAM DONE → BEEPING");
    }
  }

  // ===== STATE 2: BEEPING =====
  else if (state == 2) {
    if (millis() - lastBeepToggle >= 300) {
      buzzerState = !buzzerState;
      digitalWrite(buzzerPin, buzzerState);
      digitalWrite(ledPin, buzzerState);

      lastBeepToggle = millis();

      if (buzzerState == true) {
        beepCount++;
      }
    }

    if (beepCount >= 3) {
      state = 0;
      digitalWrite(buzzerPin, LOW);
      digitalWrite(ledPin, LOW);
      Serial.println("DONE → BACK TO IDLE");
    }
  }

  delay(20);
}
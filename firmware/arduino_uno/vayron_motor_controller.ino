
/*
 * VAYRON AMR - Arduino Uno Motor Controller
 * Driver: L298N
 * Serial protocol: M,left,right\n
 * Speed range: -1.0 to +1.0
 * Independent command timeout: 500 ms
 *
 * IMPORTANT:
 * Verify these pin assignments against actual wiring
 * before connecting motor power.
*/
#include <stdlib.h>
#include <string.h>

const unsigned long SERIAL_TIMEOUT_MS = 500;
const unsigned long BAUD_RATE = 115200;

// Left L298N channel
const int LEFT_EN  = 5;  // PWM
const int LEFT_IN1 = 7;
const int LEFT_IN2 = 8;

// Right L298N channel
const int RIGHT_EN  = 6; // PWM
const int RIGHT_IN1 = 9;
const int RIGHT_IN2 = 10;

unsigned long lastCommandTime = 0;
bool commandReceived = false;

char inputBuffer[64];
size_t inputIndex = 0;

void stopMotors() {
  analogWrite(LEFT_EN, 0);
  analogWrite(RIGHT_EN, 0);

  digitalWrite(LEFT_IN1, LOW);
  digitalWrite(LEFT_IN2, LOW);
  digitalWrite(RIGHT_IN1, LOW);
  digitalWrite(RIGHT_IN2, LOW);
}

void setMotor(int pwmPin, int in1, int in2, float speed) {
  speed = constrain(speed, -1.0f, 1.0f);

  if (speed > 0.0f) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  } else if (speed < 0.0f) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }

  int pwm = (int)(abs(speed) * 255.0f);
  analogWrite(pwmPin, pwm);
}

bool parseCommand(char *line, float &left, float &right) {
  if (line[0] != 'M' || line[1] != ',') {
    return false;
  }

  char *firstComma = strchr(line, ',');
  if (firstComma == nullptr) return false;

  char *secondComma = strchr(firstComma + 1, ',');
  if (secondComma == nullptr) return false;

  char *endPtrLeft;
  char *endPtrRight;

  left = strtof(firstComma + 1, &endPtrLeft);
  right = strtof(secondComma + 1, &endPtrRight);

  if (endPtrLeft != secondComma || *endPtrRight != '\0') {
    return false;
  }

  if (left < -1.0f || left > 1.0f ||
      right < -1.0f || right > 1.0f) {
    return false;
  }

  return true;
}

void processLine(char *line) {
  float leftSpeed;
  float rightSpeed;

  if (!parseCommand(line, leftSpeed, rightSpeed)) {
    stopMotors();
    commandReceived = false;
    return;
  }

  setMotor(LEFT_EN, LEFT_IN1, LEFT_IN2, leftSpeed);
  setMotor(RIGHT_EN, RIGHT_IN1, RIGHT_IN2, rightSpeed);

  lastCommandTime = millis();
  commandReceived = true;
}

void setup() {
  pinMode(LEFT_EN, OUTPUT);
  pinMode(LEFT_IN1, OUTPUT);
  pinMode(LEFT_IN2, OUTPUT);

  pinMode(RIGHT_EN, OUTPUT);
  pinMode(RIGHT_IN1, OUTPUT);
  pinMode(RIGHT_IN2, OUTPUT);

  stopMotors();
  Serial.begin(BAUD_RATE);
  lastCommandTime = millis();
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      inputBuffer[inputIndex] = '\0';
      processLine(inputBuffer);
      inputIndex = 0;
    } else if (c != '\r') {
      if (inputIndex < sizeof(inputBuffer) - 1) {
        inputBuffer[inputIndex++] = c;
      } else {
        inputIndex = 0;
        stopMotors();
        commandReceived = false;
      }
    }
  }

  if (!commandReceived ||
      millis() - lastCommandTime > SERIAL_TIMEOUT_MS) {
    stopMotors();
  }
}


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

const int ENCODER_PIN = 2; // HW-201 OUT
const unsigned long ENCODER_REPORT_MS = 100;
const unsigned long ENCODER_DEBOUNCE_US = 2000;
const float PULSES_PER_REV = 1.0;

volatile unsigned long encoderPulseCount = 0;
volatile unsigned long lastEncoderPulseUs = 0;
volatile unsigned long encoderPulseIntervalUs = 0;
volatile bool encoderHasPulse = false;

unsigned long lastEncoderReportMs = 0;

const unsigned long SERIAL_TIMEOUT_MS = 500;
const unsigned long BAUD_RATE = 115200;

// Left L298N channel: OUT3/OUT4
const int LEFT_EN  = 6;  // ENB, PWM
const int LEFT_IN1 = 9;  // IN3
const int LEFT_IN2 = 10; // IN4

// Right L298N channel: OUT1/OUT2
const int RIGHT_EN  = 5; // ENA, PWM
const int RIGHT_IN1 = 7; // IN1
const int RIGHT_IN2 = 8; // IN2

unsigned long lastCommandTime = 0;
bool commandReceived = false;

char inputBuffer[64];
size_t inputIndex = 0;

void encoderISR() {
  unsigned long now = micros();

  if (lastEncoderPulseUs == 0 ||
      now - lastEncoderPulseUs >= ENCODER_DEBOUNCE_US) {

    if (lastEncoderPulseUs != 0) {
      encoderPulseIntervalUs = now - lastEncoderPulseUs;
    }

    lastEncoderPulseUs = now;
    encoderPulseCount++;
    encoderHasPulse = true;
  }
}

void reportEncoderFeedback() {
  unsigned long nowMs = millis();

  if (nowMs - lastEncoderReportMs < ENCODER_REPORT_MS) {
    return;
  }

  unsigned long nowUs = micros();

  noInterrupts();
  unsigned long count = encoderPulseCount;
  unsigned long lastPulseUs = lastEncoderPulseUs;
  unsigned long intervalUs = encoderPulseIntervalUs;
  bool hasPulse = encoderHasPulse;
  interrupts();

  unsigned long pulseAgeUs = nowUs - lastPulseUs;

  unsigned long staleTimeoutUs =
      (intervalUs > 750000UL) ? intervalUs * 2UL : 1500000UL;

  float rpm = 0.0f;

  if (hasPulse && intervalUs > 0 &&
      pulseAgeUs <= staleTimeoutUs) {
    rpm = 60000000.0f /
          (intervalUs * PULSES_PER_REV);
  }

  Serial.print("E,");
  Serial.print(count);
  Serial.print(",");
  Serial.println(rpm, 2);

  lastEncoderReportMs = nowMs;
}

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

  left = strtod(firstComma + 1, &endPtrLeft);
  right = strtod(secondComma + 1, &endPtrRight);

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
  pinMode(ENCODER_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_PIN), encoderISR, FALLING);
  Serial.begin(BAUD_RATE);
  lastCommandTime = millis();
  lastEncoderReportMs = millis();
}

void loop() {
  reportEncoderFeedback();
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

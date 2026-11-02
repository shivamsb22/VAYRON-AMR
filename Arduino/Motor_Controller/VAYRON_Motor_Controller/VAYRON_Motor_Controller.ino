/*
 * VAYRON AMR - Arduino Uno Motor Controller
 * Driver: L298N
 * Drive: 4-wheel differential / skid steer
 *
 * Left motors  -> L298N OUT1 / OUT2
 * Right motors -> L298N OUT3 / OUT4
 *
 * Serial protocol at 115200 baud:
 * M,<left_speed>,<right_speed>
 * Example: M,0.500,0.500
 */

const int ENA = 5;
const int IN1 = 7;
const int IN2 = 8;

const int ENB = 6;
const int IN3 = 9;
const int IN4 = 10;

const unsigned long COMMAND_TIMEOUT_MS = 500;

unsigned long lastCommandTime = 0;
char inputBuffer[48];
byte inputIndex = 0;

void setMotor(int pwmPin, int inA, int inB, float speed) {
  speed = constrain(speed, -1.0, 1.0);

  if (speed > 0.0) {
    digitalWrite(inA, HIGH);
    digitalWrite(inB, LOW);
  } else if (speed < 0.0) {
    digitalWrite(inA, LOW);
    digitalWrite(inB, HIGH);
  } else {
    digitalWrite(inA, LOW);
    digitalWrite(inB, LOW);
  }

  int pwm = (int)(abs(speed) * 255.0);
  analogWrite(pwmPin, pwm);
}

void stopMotors() {
  setMotor(ENA, IN1, IN2, 0.0);
  setMotor(ENB, IN3, IN4, 0.0);
}

void processCommand(char *command) {
  char *type = strtok(command, ",");
  char *leftText = strtok(NULL, ",");
  char *rightText = strtok(NULL, ",");

  if (type == NULL || leftText == NULL || rightText == NULL) {
    stopMotors();
    return;
  }

  if (strcmp(type, "M") != 0) {
    stopMotors();
    return;
  }

  float leftSpeed = atof(leftText);
  float rightSpeed = atof(rightText);

  if (!isfinite(leftSpeed) || !isfinite(rightSpeed)) {
    stopMotors();
    return;
  }

  leftSpeed = constrain(leftSpeed, -1.0, 1.0);
  rightSpeed = constrain(rightSpeed, -1.0, 1.0);

  setMotor(ENA, IN1, IN2, leftSpeed);
  setMotor(ENB, IN3, IN4, rightSpeed);

  lastCommandTime = millis();
}

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();

  Serial.begin(115200);
  lastCommandTime = millis();
}

void loop() {
  while (Serial.available() > 0) {
    char incoming = Serial.read();

    if (incoming == '\n') {
      inputBuffer[inputIndex] = '\0';
      processCommand(inputBuffer);
      inputIndex = 0;
    } else if (incoming != '\r') {
      if (inputIndex < sizeof(inputBuffer) - 1) {
        inputBuffer[inputIndex++] = incoming;
      } else {
        inputIndex = 0;
        stopMotors();
      }
    }
  }

  if (millis() - lastCommandTime > COMMAND_TIMEOUT_MS) {
    stopMotors();
  }
}

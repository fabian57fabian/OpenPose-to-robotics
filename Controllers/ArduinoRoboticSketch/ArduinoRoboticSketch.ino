#include <Servo.h>
Servo servoX;
Servo servoY;
Servo servoZ;

#define packetLength 9
#define min_angle 0
#define max_angle 180

byte recvArray[packetLength];
int count;
byte tmpByte;

void setup() {
  servoX.attach(9);
  servoY.attach(10);
  servoZ.attach(11);
  delay(30);
  servoX.write(90);
  servoY.write(170);
  servoZ.write(55);
  Serial.begin(9600);  // initialize serial communications at 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    delay(10);
    receiveBytes();
    if (count + 1 >= packetLength) {
      ManageDataReceived();
    }
  } else {
    delay(10);
  }
}

void receiveBytes() {
  count = 0;
  while (Serial.available()) {
    tmpByte = Serial.read();
    if (count < packetLength) {
      recvArray[count] = tmpByte;
    }
    count = count + 1;
  }
}

void ManageDataReceived() {
  int angle = getAngle(0);
  if (angle >= min_angle && angle <= max_angle) {
    servoX.write(angle);
    delay(1);
  }
  angle = getAngle(1);
  if (angle >= min_angle && angle <= max_angle) {
    servoY.write(angle);
    delay(1);
  }
  angle = getAngle(2);
  if (angle >= min_angle && angle <= max_angle) {
    servoZ.write(angle);
    delay(1);
  }
}

int getAngle(short servo) {
  if (servo < 0 || servo > 3) {
    return 90;
  }
  int angle = (recvArray[(3*servo) +0] - 48) * 100;
  angle = angle + (recvArray[(3*servo) +1] - 48) * 10;
  angle = angle + (recvArray[(3*servo) +2] - 48) * 1;
  return angle;
}

void blink_led_builtin(int num) {
  for (int i = 0; i < num; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
}

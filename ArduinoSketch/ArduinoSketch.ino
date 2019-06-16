#include <Servo.h>
Servo servoH;

#define packetLength 10
#define min_angleH 10
#define max_angleH 170

byte recvArray[packetLength];
int count;
byte tmpByte;

void setup() {
  servoH.attach(9);
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
  int angle=getAngle();
  if(angle >= min_angleH && angle <=max_angleH){
    //blink_led_builtin(2);
    servoH.write(angle);
    delay(1);
  }
}

int getAngle(){
  int angle=(recvArray[0]-48)*100;
  angle=angle+(recvArray[1]-48)*10;
  angle=angle+(recvArray[2]-48)*1;
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

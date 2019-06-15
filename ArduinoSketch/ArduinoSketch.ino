#define packetLength 10

byte recvArray[packetLength];
int count;
byte tmpByte;

void setup() {
  Serial.begin(9600);  // initialize serial communications at 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    delay(30);
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
  char a = recvArray[0];
  switch (a) {
    case 'f':
      //Go forward
      break;
    case 'b':
      //Go backward
      break;
    case 'r':
      //Go Right
      break;
    case 'l':
      //Go Left
      break;
  }
  //blink_led_builtin(num);
}

void blink_led_builtin(int num) {
  for (int i = 0; i < num; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
  }
}

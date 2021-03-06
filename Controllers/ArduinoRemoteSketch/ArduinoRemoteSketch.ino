# include<SoftwareSerial.h>

#define TxD 3
#define RxD 2

char c;

SoftwareSerial bluetooth(RxD, TxD);

void setup() {
  Serial.begin(38400);
  Serial.println("Started");
  bluetooth.begin(38400);
}

void loop() {
  if (Serial.available()) {
    c = Serial.read();
    bluetooth.write(c);
  } else {
    delay(5);
  }
}

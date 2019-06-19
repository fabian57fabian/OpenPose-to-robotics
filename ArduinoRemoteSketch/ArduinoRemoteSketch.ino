# include<SoftwareSerial.h>

#define TxD 3
#define RxD 2
#define LED_PIN 13

char c;

SoftwareSerial bluetooth(RxD, TxD);

void setup() {
  Serial.begin(9600);
  Serial.println("Started");
  bluetooth.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    c = Serial.read();
    bluetooth.write(c);
  } else {
    delay(5);
  }
}

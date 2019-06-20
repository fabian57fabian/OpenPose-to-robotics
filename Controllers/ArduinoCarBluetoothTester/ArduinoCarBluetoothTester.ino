# include<SoftwareSerial.h>

#define TxD 3
#define RxD 2

char c;

SoftwareSerial bluetooth(RxD, TxD);

void setup() {
  Serial.begin(9600);
  Serial.println("Started");
  bluetooth.begin(38400);
}

void loop() {
  if (bluetooth.available())
  {
    c = bluetooth.read();
    Serial.write(c);
  }
  else{
    delay(10);
  }
}

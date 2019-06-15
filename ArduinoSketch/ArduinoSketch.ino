String readString="";

void setup() {
  Serial.begin(9600);  // initialize serial communications at 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
    }
  }
  if (readString.length() > 0) {
    ManageDataReceived();
  }else{
      delay(10);
  }
}

void ManageDataReceived(){
  blink_led_builtin();
}

void blink_led_builtin() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
  }
}

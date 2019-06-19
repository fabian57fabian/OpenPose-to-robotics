// Basic bluetooth test sketch. HC-06_01_9600
// HC-06 ZS-040
//
//
//  Uses hardware serial to talk to the host computer and software serial for communication with the bluetooth module
//
//  Pins
//  BT VCC to Arduino 5V out.
//  BT GND to GND
//  BT RX to Arduino pin 3 (through a voltage divider)
//  BT TX to Arduino pin 2 (no need voltage divider)
//
//  When a command is entered in the serial monitor on the computer
//  the Arduino will relay it to the bluetooth module and display the result.
//
//  These HC-06 modules require capital letters and no line ending
//

#include <SoftwareSerial.h>
SoftwareSerial BTSerial(2,3); // RX | TX

void setup()
{
  Serial.begin(9600);
  Serial.println("Started");
  BTSerial.begin(38400);
  Serial.println("BtnConnected");
  /*
  Serial.println("Sending AT");
  BTSerial.write("A"); delay(50);
  BTSerial.write("T"); delay(50);
  delay(500);
  while (BTSerial.available()) {
    Serial.write(BTSerial.read());
  }
  Serial.println();
  delay(500);
  */
  
  //Serial.println("Sending AT+NAMEOpenPoseReceiver");
  //BTSerial.write("AT+NAMEOpenPoseReceiver");
  /*
  BTSerial.write("A"); delay(20);
  BTSerial.write("T"); delay(20);
  BTSerial.write("+"); delay(20);
  BTSerial.write("N"); delay(20);
  BTSerial.write("A"); delay(20);
  BTSerial.write("M"); delay(20);
  BTSerial.write("E"); delay(20);
  BTSerial.write("O"); delay(20);
  BTSerial.write("p"); delay(20);
  BTSerial.write("e"); delay(20);
  BTSerial.write("n"); delay(20);
  BTSerial.write("P"); delay(20);
  BTSerial.write("o"); delay(20);
  BTSerial.write("s"); delay(20);
  BTSerial.write("e"); delay(20);
  BTSerial.write("R"); delay(20);
  BTSerial.write("e"); delay(20);
  BTSerial.write("c"); delay(20);
  BTSerial.write("e"); delay(20);
  BTSerial.write("i"); delay(20);
  BTSerial.write("v"); delay(20);
  BTSerial.write("e"); delay(20);
  BTSerial.write("r"); delay(20);
  */
  /*
  delay(500);
  while (BTSerial.available()) {
    Serial.write(BTSerial.read());
  }
  Serial.println();
  */
}

void send_chname(){
  Serial.println("Sending AT+NAMEOpenPoseReceiver");
  BTSerial.write("AT+NAMEopenPoseReceiver"); delay(20);
  delay(100);
  /*
  while (BTSerial.available()) {
    Serial.write(BTSerial.read());
  }
  Serial.println();
  delay(50);
  */
}

char c;
void read_(){
  if (BTSerial.available())
    {  
        c = BTSerial.read();
        Serial.write(c);
    }
 
    // Keep reading from Arduino Serial Monitor and send to HC-05
    if (Serial.available())
    {
        c =  Serial.read();
        BTSerial.write(c);  
    }
}

void manage_and_write(){
  // Keep reading from HC-06 and send to Arduino Serial Monitor
  if (BTSerial.available())
    Serial.write(BTSerial.read());

  // Keep reading from Arduino Serial Monitor and send to HC-06
  if (Serial.available())
    BTSerial.write(Serial.read());

  continue_send();
}

void continue_send(){
  Serial.println("Sending data");
  BTSerial.write('acca\r\n');
  delay(50);
}

void loop()
{
  read_();

  /*
  Serial.println("Sending AT");
  BTSerial.write("A"); delay(20);
  BTSerial.write("T"); delay(20);
  delay(100);
  while (BTSerial.available()) {
    Serial.write(BTSerial.read());
  }
  */
}

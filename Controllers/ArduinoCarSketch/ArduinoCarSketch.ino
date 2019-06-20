//---------------------------------------------------------------------------------------------------------------------------------------
//Basic Remote Control Car - Bill Tarpy - North East CoderDojo  17/01/2015
//Feel free to use this software as a basis for your own.
#include <SoftwareSerial.h> //the library for seial communication
#include <Servo.h>
#include <AFMotor.h> // the library for the Adafruit L293 Arduino Motor Shield

char incomingCommand = 'C'; // for incoming serial data
int speed_min = 100; //the minimum "speed" the motors will turn - take it lower and motors don't turn
int speed_max = 255; //the maximum "speed" the motors will turn – you can’t put in higher
int pinServo = 10;
int pinState = 22;
int avanti = 90, destra = 70, sinistra = 110;
int pinFrontLights, pinBackLights, pinHorn;
int MODE;
Servo sterzo;

//new mode analog part 2
byte commands[4] = {0x00, 0x00, 0x00, 0x00};
byte prevCommands[4] = {0x01, 0x01, 0x01, 0x01};
//end

int speedM = speed_max; // set both motors to maximum speed
AF_DCMotor motor(1); // create motor #3, 1KHz pwm

void setup() {
  MODE = 1;
  Serial.begin(9600);
  Serial1.begin(38400);
  sterzo.attach(pinServo);
}

void LOOP1DigitalAPP() {
  motor.setSpeed(speedM);
  if (digitalRead(pinState) == LOW) {
    motor.run(RELEASE);
    sterzo.write(avanti);
    Serial.println("Stop\n");//display message for test purposes
    incomingCommand = '*';
  }
  else {
    if (Serial1.available() > 0) {
      incomingCommand = Serial1.read();
    }
  }

  switch (incomingCommand)
  {
    case 'S':
      // stop all motors
      { motor.run(RELEASE); // stopped
        Serial.println("Stop\n"); //display message for test purposes when connected to a serial monitor
        sterzo.write(avanti);
        incomingCommand = '*';
      }
      break;

    case 'F':
      // turn it on going forward
      {
        motor.run(FORWARD);
        sterzo.write(avanti);

        Serial.println("Forward\n");//display message for test purposes when connected to a serial monitor
        incomingCommand = '*';
      }
      break;

    case 'B':
      // turn it on going backward
      { motor.run(BACKWARD);
        sterzo.write(avanti);

        Serial.println("Backward\n");//display message for test purposes when connected to a serial monitor
        incomingCommand = '*';
      }
      break;

    case 'L':
      // turn left
      {
        //motor.run(FORWARD);
        sterzo.write(sinistra);
        Serial.println("Rotate Left\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;


    case 'R':
      // turn right
      {
        //motor.run(FORWARD);
        sterzo.write(destra);
        Serial.println("Rotate Right\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case 'G':
      // turn forward left
      {
        motor.run(FORWARD);
        sterzo.write(sinistra);
        Serial.println("Go Forward Left\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case 'I':
      // turn forward right
      {
        motor.run(FORWARD);
        sterzo.write(destra);
        Serial.println("Go Forward Right\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case 'H':
      // turn backward left
      {
        motor.run(BACKWARD);
        sterzo.write(sinistra);
        Serial.println("Go Backward Left\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case 'J':
      // turn backward right
      {
        motor.run(BACKWARD);
        sterzo.write(destra);
        Serial.println("Go BAckward Rght\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case 'D':
      // stop all
      {
        motor.run(RELEASE);
        sterzo.write(avanti);
        Serial.println("Stop\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '0':
      // set speed
      {
        speedM = speed_min;
        Serial.println("Speed 1\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '1':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 2) + speed_min;
        Serial.println("Speed 1\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '2':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 3) + speed_min;
        Serial.println("Speed 2\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '3':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 4) + speed_min;
        Serial.println("Speed 3\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '4':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 5) + speed_min;
        Serial.println("Speed 4\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '5':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 6) + speed_min;
        Serial.println("Speed 5\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '6':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 7) + speed_min;
        Serial.println("Speed 6\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '7':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 8) + speed_min;
        Serial.println("Speed 7\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '8':
      // set speed
      {
        speedM = (((speed_max - speed_min) / 10) * 9) + speed_min;
        Serial.println("Speed 8\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case '9':
      // set speed
      {
        speedM = speed_max;
        Serial.println("Speed 9\n");//display message for test purposes
        incomingCommand = '*';
      }
      break;

    case 'X':
      {
        MODE = 2;
        Serial.println("Mode Changed 10\n");//display message for test purposes
      }
      break;
  }
  Serial.println(speedM);
}

void loop() {
  switch (MODE) {
    case 1:
      LOOP1DigitalAPP();
      break;
    case 2:
      delay(1000);
      break;
    default:
      delay(1000);
      break;
  }
}

#include <Servo.h>
#include <AFMotor.h> // the library for the Adafruit L293 Arduino Motor Shield

#define TRIM_L 40

char incomingCommand = '~'; // for incoming serial data
int speed_min = 40; //the minimum "speed" the motors will turn - take it lower and motors don't turn
int speed_max = 150; //the maximum "speed" the motors will turn – you can’t put in higher
int pinState = 22;

int speedFB = 0;
int speed_balance = 0;
int speedR = 0;       //speed right engine
int speedL = 0;       //speed left engine
AF_DCMotor motorL(1);          // create motor #1, 1KHz pwm
AF_DCMotor motorR(2);          // create motor #1, 1KHz pwm

int selected_dir_R = FORWARD;
int selected_dir_L = FORWARD;

void setup() {
  Serial.begin(38400);       //Bluetooth module
}

void manageTurnFromSpeed(int c) {
  if (c == 105) {
    speedR = speedL = speedFB;
  }
  else if (c > 105) {
    speedR = speedFB;
    speedL = map(c, 105, 126, speedFB, speed_min);
  } else {
    speedL = speedFB;
    speedR = map(c, 85, 105, speed_min, speedFB);
  }
}

void loop() {
  incomingCommand = 'K';      //This is an unused char command
  //Check if no bluetooth connection
  if (digitalRead(pinState) == LOW) {
    motorR.setSpeed(0);
    motorL.setSpeed(0);
    //motorR.run(RELEASE);
    //motorL.run(RELEASE);
  }
  else {
    if (Serial.available() > 0) {
      incomingCommand = Serial.read();
    }
    if (incomingCommand >= 48 && incomingCommand <= 57) {
      //Manage speed
      speedR = speedL = speedFB = (((speed_max - speed_min) / 10) * ((incomingCommand - 48) + 1)) + speed_min;
    } else if (incomingCommand >= 85 && incomingCommand <= 126) {
      //Manage Steering from [85, 126] to [destra, sinistra]
      manageTurnFromSpeed(incomingCommand);
    } else {
      switch (incomingCommand)
      {
        case 'S':              // stop all motors
          {
            speedR = speedL = speedFB = 0;
            selected_dir_R = RELEASE;
            selected_dir_L = RELEASE;
          }
          break;
        case 'F':              // Go Forward
          {
            selected_dir_R = FORWARD;
            selected_dir_L = FORWARD;
          }
          break;
        case 'B':              // Go Backward
          {
            selected_dir_R = BACKWARD;
            selected_dir_L = BACKWARD;
          }
          break;
        case 'L':              // turn left
          {
            manageTurnFromSpeed(85);
          }
          break;
        case 'R':              // turn right
          {
            manageTurnFromSpeed(126);
          }
          break;
        case 'T':              // steer front
          {
            manageTurnFromSpeed(105);
          }
          break;
        case 'D':              // stop all
          {
            speedR = speedL = speedFB = 0;
            selected_dir_R = RELEASE;
            selected_dir_L = RELEASE;
          }
          break;
      }
    }
    speed_balance = speedL - TRIM_L;
    if (speed_balance < 0) {
      speed_balance = 0;
    }
    motorR.setSpeed(speedR);
    motorL.setSpeed(speed_balance);
    motorR.run(selected_dir_R);
    motorL.run(selected_dir_L);
  }
}

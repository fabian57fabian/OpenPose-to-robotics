#include <SoftwareSerial.h> //the library for seial communication
#include <Servo.h>
//#include <AFMotor.h> // the library for the Adafruit L293 Arduino Motor Shield

char incomingCommand = '~'; // for incoming serial data
int speed_min = 100; //the minimum "speed" the motors will turn - take it lower and motors don't turn
int speed_max = 255; //the maximum "speed" the motors will turn – you can’t put in higher
int pinServo = 9;
int pinState = 22;
int avanti = 90, destra = 70, sinistra = 110;

Servo sterzo;

int speedM = speed_max;       //speed
int steerAngle = avanti;      //steer var

//New vars
#define RELEASE 1
#define FORWARD 2
#define BACKWARD 3

#define MOTOR_IN1 10
#define MOTOR_IN2 11
#define MOTOR_EN_1_2 6


class AF_DCMotor {
  public:
    //AF_DCMotor(int number);
    AF_DCMotor::AF_DCMotor(int number) {
      this->number = number;
    }
    void AF_DCMotor::run(int n) {
      switch (n) {
        case 1:
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN2, LOW);
          break;
        case 2:
        digitalWrite(MOTOR_IN1, HIGH);
        digitalWrite(MOTOR_IN2, LOW);
          break;
        case 3:
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN2, HIGH);
          break;
      }
    }
    void AF_DCMotor::setSpeed(int n) {
      analogWrite(MOTOR_EN_1_2, n);
    }
  private:
    int number;
};
//end new vars
AF_DCMotor motor(1);          // create motor #3, 1KHz pwm

void setup() {
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  pinMode(MOTOR_EN_1_2, OUTPUT);
  Serial.begin(38400);         //For Debugging
  //Serial1.begin(38400);       //Bluetooth module
  sterzo.attach(pinServo);    //Steer Servo
}

void loop() {
  incomingCommand = '~';      //This is an unused char command
  //Check if no bluetooth connection
  //if (digitalRead(pinState) == LOW) {
  if (false) {
    motor.run(RELEASE);
    sterzo.write(avanti);
    //Serial.println("Stop\n");//display message for test purposes
  }
  else {
    if (Serial.available() > 0) {
      incomingCommand = Serial.read();
    }
    if (incomingCommand >= 48 && incomingCommand <= 57) {
      //Manage speed
      speedM = (((speed_max - speed_min) / 10) * ((incomingCommand - 48) + 1)) + speed_min;
      motor.setSpeed(speedM);
    } else if (incomingCommand >= 97 && incomingCommand <= 122) {
      //Manage Steering from [97, 122] to [destra, sinistra]
      steerAngle = map(incomingCommand, 97, 122, sinistra, destra);
      sterzo.write(steerAngle);
    } else {
      switch (incomingCommand)
      {
        case 'S':              // stop all motors
          { motor.run(RELEASE); // stopped
            //Serial.println("Stop\n"); //display message for test purposes when connected to a serial monitor
          }
          break;
        case 'F':              // Go Forward
          {
            motor.run(FORWARD);
            //Serial.println("Forward\n");//display message for test purposes when connected to a serial monitor
          }
          break;
        case 'B':              // Go Backward
          { motor.run(BACKWARD);
            //Serial.println("Backward\n");//display message for test purposes when connected to a serial monitor
          }
          break;
        case 'L':              // turn left
          {
            steerAngle = sinistra;
            sterzo.write(sinistra);
            //Serial.println("Rotate Left\n");//display message for test purposes
          }
          break;
        case 'R':              // turn right
          {
            steerAngle = destra;
            sterzo.write(destra);
            //Serial.println("Rotate Right\n");//display message for test purposes
          }
          break;
        case 'T':              // steer front
          { steerAngle = avanti;
            sterzo.write(avanti);
            //Serial.println("Steer Front\n");//display message for test purposes
          }
          break;
        case 'D':              // stop all
          { motor.run(RELEASE);
            steerAngle = avanti;
            sterzo.write(avanti);
          }
          break;
      }
    }
  }
  //Serial.println(speedM);
}

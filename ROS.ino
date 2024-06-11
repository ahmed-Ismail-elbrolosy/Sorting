#include <ros.h>
#include <std_msgs/String.h>
#include <Servo.h>

ros::NodeHandle nh;

#include <AccelStepper.h>
unsigned long t;
// Define the stepper motor and the pins that is connected to
AccelStepper stepper1(1, 2, 3); // (Type of driver: with 2 pins, STEP, DIR)
// twelve serv
Servo blueServo;
Servo redServo;

const int enable=6;
int servoPosition = 0;
int increment = 1; // Degree change per step
unsigned long previousMillis = 0;
const long interval = 20; // Interval at which to update servo position (milliseconds)
unsigned long currentMillis = millis();
blueServo.attach(10);
void Callback(const std_msgs::String &msg) {
  
  if (strcmp(msg.data, "Blue color detected!") == 0) {
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    servoPosition += increment;

    // Reverse direction at 0 and 180 degrees
    if (servoPosition >= 180 || servoPosition <= 0) {
      increment = -increment;
    }

    blueServo.write(servoPosition);
  }
 digitalWrite(enable,LOW);
stepper1.setSpeed(-2000);
//   //Step the motor with a constant speed previously set by setSpeed();
stepper1.runSpeed();   
  }
//    stepper1.setSpeed(-2000);
//    stepper1.runSpeed();
   //   unsigned long currentMillis = millis();

//  if (currentMillis - previousMillis >= interval) {
//    previousMillis = currentMillis;
//
//  // Step the motor with a constant speed previously set by setSpeed();
//    blueServo.write(180);
//  }// Wait for 1 second
//    blueServo.write(0);
//  }
//   else if (strcmp(msg.data, "Red color detected!") == 0) {
//    stepper1.setSpeed(-2000);
//    stepper1.runSpeed();
//    delay(10000);
//    //digitalWrite(enable,HIGH);
//    delay(5000);
//    redServo.write(180);
//    delay(1000); // Wait for 1 second
//    redServo.write(0);
//    stepper1.setSpeed(-2000);
//    stepper1.runSpeed();
//  }
  }


ros::Subscriber<std_msgs::String> CallbackedSub("Detection", &Callback);



void setup() {
  
  nh.initNode();
//  nh.subscribe(blueSub);
  nh.subscribe(CallbackedSub);
// attaches the servo on pin 9 to the servo object
Serial.begin(57600);
  stepper1.setMaxSpeed(2000);
  pinMode(10,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(6,OUTPUT);
  redServo.attach(11);
  blueServo.attach(10);
  //pinMode(enable,OUTPUT);}
}

void loop() {
unsigned long currentMillis = millis();

digitalWrite(enable,LOW);
stepper1.setSpeed(-2000);
//   //Step the motor with a constant speed previously set by setSpeed();
stepper1.runSpeed();
  nh.spinOnce();
delayMicroseconds(10);}

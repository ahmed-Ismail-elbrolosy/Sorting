#include <ros.h>
#include <std_msgs/String.h>
#include <Servo.h>

ros::NodeHandle nh;

//#include <AccelStepper.h>

// Define the stepper motor and the pins that is connected to
//AccelStepper stepper1(1, 2, 3); // (Type of driver: with 2 pins, STEP, DIR)
// twelve serv
Servo blueServo;
Servo redServo; 
//const int enable=6;


void Callback(const std_msgs::String &msg) {
  if (strcmp(msg.data, "Blue color detected!") == 0) {
      //digitalWrite(enable,HIGH);
      //delay(5000);
    
  // Step the motor with a constant speed previously set by setSpeed();
  
    blueServo.attach(9);
    blueServo.write(180);
    delay(1000); // Wait for 1 second
    blueServo.write(0);
    //stepper1.setSpeed(-2000);
    //stepper1.runSpeed();
  }
   else if (strcmp(msg.data, "Red color detected!") == 0) {
    //digitalWrite(enable,HIGH);
    //delay(5000);
    redServo.attach(10);
    redServo.write(180);
    delay(1000); // Wait for 1 second
    redServo.write(0);
    //stepper1.setSpeed(-2000);
    //stepper1.runSpeed();
  }
  }


ros::Subscriber<std_msgs::String> CallbackedSub("Detection", &Callback);



void setup() {
  nh.initNode();
//  nh.subscribe(blueSub);
  nh.subscribe(CallbackedSub);
// attaches the servo on pin 9 to the servo object
  //stepper1.setMaxSpeed(2000);
  Serial.begin(9600);
  //pinMode(enable,OUTPUT);}
}

void loop() {
  //digitalWrite(enable,LOW);
  //stepper1.setSpeed(-2000);
  // Step the motor with a constant speed previously set by setSpeed();
  //stepper1.runSpeed();
  nh.spinOnce();
  


 
}

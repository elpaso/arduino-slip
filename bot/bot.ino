/**
 Bot
*/


#include <Wire.h>
#include "LiquidCrystal_SR.h"

//LiquidCrystal_SR lcd(8,7,TWO_WIRE);
//                   | |
//                   | \-- Clock Pin
//                   \---- Data/Enable Pin

// Data, Clock e Enable. Enable must be connected to both pin 12 on the SR and
// pin 6 on the LCD
//
// See: https://bitbucket.org/fmalpartida/new-liquidcrystal/wiki/schematics#!latch-shift-register
//
//
LiquidCrystal_SR lcd(6,8,7);

#define trigPin A0
#define echoPin A1

int switchPin = 2;    // switch input
int motor1Pin1 = 3;    // pin 2 on L293D
int motor1Pin2 = 4;    // pin 7 on L293D
int enable1Pin = 9;   // pin 1 on L293D


int motor2Pin1 = 12;    // pin 2 on L293D
int motor2Pin2 = 11;    // pin 7 on L293D
int enable2Pin = 10;   // pin 1 on L293D


int ledPin = 13;

byte speed=0;

void setup() {
  // set the switch as an input:
  pinMode(switchPin, INPUT);

  // set all the other pins you're using as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  // set all the other pins you're using as outputs:
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // set enablePin high so that motor can turn on:
  // digitalWrite(enablePin, HIGH);

  lcd.begin(16,2);               // initialize the lcd
  lcd.home ();
  lcd.print("Bot ready.");

}

void left(boolean forward){
    digitalWrite(motor1Pin1, forward);   // set pin 2 on L293D low
    digitalWrite(motor1Pin2, !forward);  // set pin 7 on L293D high
}

void right(boolean forward){
    digitalWrite(motor2Pin1, forward);   // set pin 2 on L293D low
    digitalWrite(motor2Pin2, !forward);  // set pin 7 on L293D high
}


void loop() {
  long duration, distance;
  speed = 245; // 170 min
  analogWrite(enable1Pin, speed);
  analogWrite(enable2Pin, speed);
  lcd.home ();
  //lcd.print("Speed ");
  //lcd.print(speed);
  digitalWrite(trigPin, LOW);  // Added this line
  delayMicroseconds(2); // Added this line
  digitalWrite(trigPin, HIGH);
//  delayMicroseconds(1000); - Removed this line
  delayMicroseconds(10); // Added this line
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  lcd.clear();
  lcd.print(distance);
  if(distance > 50){
    left(1);
    right(1);
  } else {
    left(1);
    right(0);
  }
  delay(100);
  /*
  // if the switch is high, motor will turn on one direction:
  if (digitalRead(switchPin) == HIGH) {
    digitalWrite(motor1Pin1, LOW);   // set pin 2 on L293D low
    digitalWrite(motor1Pin2, HIGH);  // set pin 7 on L293D high
    digitalWrite(motor2Pin1, LOW);   // set pin 2 on L293D low
    digitalWrite(motor2Pin2, HIGH);  // set pin 7 on L293D high
  }
  // if the switch is low, motor will turn in the opposite direction:
  else {
    digitalWrite(motor1Pin1, HIGH);  // set pin 2 on L293D high
    digitalWrite(motor1Pin2, LOW);   // set pin 7 on L293D low
    digitalWrite(motor2Pin1, HIGH);  // set pin 2 on L293D high
    digitalWrite(motor2Pin2, LOW);   // set pin 7 on L293D low
 }
 */
}

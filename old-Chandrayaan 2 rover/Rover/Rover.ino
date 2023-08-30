#include <AFMotor.h>
#include <Servo.h>              // Add library
Servo solarpanel;
Servo mast; 
int servo_position = 0 ;
int mast_pos = 0 ;
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
char bt='S';
void setup()
{
  Serial.begin(9600);
  solarpanel.attach (10);
  mast.attach (9);
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
  solarpanel.write(0);
  mast.write(0);
  Stop();
}

void loop() {
 
bt=Serial.read();

if(bt=='f'|| bt=='F')
{
 forward(); 
}
if(bt=='b'|| bt=='B')
{
 backward(); 
}
if(bt=='L'|| bt=='l')
{
 left(); 
}
if(bt=='R'|| bt=='r')
{
 right(); 
}
if(bt=='X'||bt=='x')
{
 solarpanelON(); 
}
if(bt=='V'||bt=='v')
{
 solarpanelOFF();
}
if(bt=='W'||bt=='w')
{
 mastON();
}
if(bt=='U'||bt=='u')
{
 mastOFF();
}
if(bt=='S')
{
 Stop(); 
}
if(bt=='j'||bt=='J')
{
 Stop(); 
}

}
void forward()
{
     motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void backward()
{
     motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}
void left()
{
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}
void right()
{
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}
void Stop()
{
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}
void solarpanelON()
{
  for (servo_position = 0; servo_position <=180; servo_position +=1){

    solarpanel.write(servo_position);
    delay(10);
  }
}

void solarpanelOFF()
{
    for (servo_position=180; servo_position >= 0; servo_position -=1){

    solarpanel.write(servo_position);
    delay(10);
  }
}
void mastON()
{
  for (mast_pos = 0; mast_pos <=90; mast_pos +=1){

    mast.write(mast_pos);
    delay(10);
  }
}
void mastOFF()
{
for (mast_pos=90; mast_pos >= 0; mast_pos -=1){

    mast.write(mast_pos);
    delay(10);
}

  
}

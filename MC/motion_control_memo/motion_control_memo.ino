#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "trj.h"

Adafruit_PWMServoDriver driver = Adafruit_PWMServoDriver();

#define SERVOMIN0  120
#define SERVOMAX0  500
#define SERVOMIN1  130
#define SERVOMAX1  490
#define SERVOMIN2  115
#define SERVOMAX2  485
#define SERVO_FREQ 50
#define J_0_OFFSET 90
#define J_1_OFFSET 100
#define J_2_OFFSET 60
#define J_3_OFFSET 110
#define J_4_OFFSET 50
#define J_5_OFFSET 120

int8_t  angolo0, angolo1, angolo2, angolo3, angolo4, angolo5;
float pwm0, pwm1, pwm2, pwm3, pwm4, pwm5;
String buffer;
          
void setup() {
  Serial.begin(9600);
  driver.begin();
  driver.setOscillatorFrequency(27000000);
  driver.setPWMFreq(SERVO_FREQ);
  delay(10);
  pwm0 = map(-1.0485 + J_0_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm1 = map(25.6169 + J_1_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm2 = map(-58.4417 + J_2_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm3 = map(-1.9366 + J_3_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm4 = map(-32.8362 + J_4_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm5 = map(1.6272 + J_5_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  driver.setPWM(0, 0, pwm0);
  driver.setPWM(1, 0, pwm1);
  driver.setPWM(2, 0, pwm2);
  driver.setPWM(3, 0, pwm3);
  driver.setPWM(4, 0, pwm4);
  driver.setPWM(5, 0, pwm5);
}

void loop() {
  if(Serial.available()){
    Serial.readString();
    for(int i = 0; i < 300; i++){
      pwm0 = map(traj[i][0] + J_0_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
      pwm1 = map(traj[i][1] + J_1_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
      pwm2 = map(traj[i][2] + J_2_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
      pwm3 = map(traj[i][3] + J_3_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
      pwm4 = map(traj[i][4] + J_4_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
      pwm5 = map(traj[i][5] + J_5_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);

      driver.setPWM(0, 0, pwm0);
      driver.setPWM(1, 0, pwm1);
      driver.setPWM(2, 0, pwm2);
      driver.setPWM(3, 0, pwm3);
      driver.setPWM(4, 0, pwm4);
      driver.setPWM(5, 0, pwm5);
      delay(25);
    }
  }
}
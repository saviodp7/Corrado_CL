#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver driver = Adafruit_PWMServoDriver();

#define SERVOMIN0  120
#define SERVOMAX0  500
#define SERVOMIN1  130
#define SERVOMAX1  490
#define SERVOMIN2  115
#define SERVOMAX2  485
#define SERVO_FREQ 50
#define J_0_OFFSET 85
#define J_1_OFFSET 100
#define J_2_OFFSET 60
#define J_3_OFFSET 100
#define J_4_OFFSET 60
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
  pwm0 = map(0 + J_0_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm1 = map(0 + J_1_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm2 = map(0 + J_2_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm3 = map(0 + J_3_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm4 = map(0 + J_4_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm5 = map(0 + J_5_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
}

void loop() {
  if(Serial.available()){
    buffer = Serial.readString();
    sscanf(buffer.c_str(), "%d,%d,%d,%d,%d,%d", &angolo0, &angolo1, &angolo2, &angolo3, &angolo4, &angolo5);
  }

  pwm0 = map(angolo0 + J_0_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm1 = map(angolo1 + J_1_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm2 = map(angolo2 + J_2_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm3 = map(angolo3 + J_3_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);
  pwm4 = map(angolo4 + J_4_OFFSET, 0, 180, SERVOMIN0, SERVOMAX0);
  pwm5 = map(angolo5 + J_5_OFFSET, 0, 180, SERVOMIN1, SERVOMAX1);

  driver.setPWM(0, 0, pwm0);
  driver.setPWM(1, 0, pwm1);
  driver.setPWM(2, 0, pwm2);
  driver.setPWM(3, 0, pwm3);
  driver.setPWM(4, 0, pwm4);
  driver.setPWM(5, 0, pwm5);
  delay(500);

}
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver driver = Adafruit_PWMServoDriver();

#define SERVOMIN0  120
#define SERVOMAX0  489
#define SERVOMIN1  110
#define SERVOMAX1  475
#define SERVOMIN2  120
#define SERVOMAX2  475
#define SERVOMIN3  75
#define SERVOMAX3  465
#define SERVOMIN4  80
#define SERVOMAX4  460
#define SERVOMIN5  80
#define SERVOMAX5  460

#define SERVO_FREQ 50
#define J_0_OFFSET 0
#define J_1_OFFSET 0
#define J_2_OFFSET 0
#define J_3_OFFSET 0
#define J_4_OFFSET 0
#define J_5_OFFSET 0

int angolo0, angolo1, angolo2, angolo3, angolo4, angolo5;
float pwm0, pwm1, pwm2, pwm3, pwm4, pwm5;
String buffer, angolo0_string, angolo1_string, angolo2_string, angolo3_string, angolo4_string, angolo5_string;

void setup() {
  Serial.begin(9600);
  driver.begin();
  driver.setOscillatorFrequency(27000000);
  driver.setPWMFreq(SERVO_FREQ);
  delay(10);
  pwm0 = map(0, -90, 80, SERVOMIN0, SERVOMAX0);
  pwm1 = map(0, -90, 90, SERVOMIN1, SERVOMAX1);
  pwm2 = map(0, -90, 90, SERVOMIN2, SERVOMAX2);
  pwm3 = map(0, -90, 90, SERVOMIN3, SERVOMAX3);
  pwm4 = map(0, -90, 90, SERVOMIN4, SERVOMAX4);
  pwm5 = map(0, -90, 90, SERVOMIN5, SERVOMAX5);

  driver.setPWM(0, 0, pwm0);
  driver.setPWM(1, 0, pwm1);
  driver.setPWM(2, 0, pwm2);
  driver.setPWM(3, 0, pwm3);
  driver.setPWM(4, 0, pwm4);
  driver.setPWM(5, 0, pwm5);
}

void loop() {
  if(Serial.available()){
    buffer = Serial.readString();
    sscanf(buffer.c_str(), "%d,%d,%d,%d,%d,%d", &angolo0, &angolo1, &angolo2, &angolo3, &angolo4, &angolo5);
  }
  pwm0 = map(angolo0, -90, 80, SERVOMIN0, SERVOMAX0);
  pwm1 = map(angolo1, -90, 90, SERVOMIN1, SERVOMAX1);
  pwm2 = map(angolo2, -90, 90, SERVOMIN2, SERVOMAX2);
  pwm3 = map(angolo3, -90, 90, SERVOMIN3, SERVOMAX3);
  pwm4 = map(angolo4, -90, 90, SERVOMIN4, SERVOMAX4);
  pwm5 = map(angolo5, -90, 90, SERVOMIN5, SERVOMAX5);

  driver.setPWM(0, 0, pwm0);
  driver.setPWM(1, 0, pwm1);
  driver.setPWM(2, 0, pwm2);
  driver.setPWM(3, 0, pwm3);
  driver.setPWM(4, 0, pwm4);
  driver.setPWM(5, 0, pwm5);
  delay(500);

}
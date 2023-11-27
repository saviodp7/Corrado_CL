#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "trj.h"

Adafruit_PWMServoDriver driver = Adafruit_PWMServoDriver();

#define N_POINTS  300
#define N_JOINTS  6
#define F_POSITIONS 50
#define SERVOMIN  120
#define SERVOMAX  500
#define SERVO_FREQ 50
#define J_0_OFFSET 0
#define J_1_OFFSET -5
#define J_2_OFFSET 0
#define J_3_OFFSET -80
#define J_4_OFFSET -30
#define J_5_OFFSET 27

float  theta[N_JOINTS];
float pwm[N_JOINTS];
const float offset[N_JOINTS] = {J_0_OFFSET, J_1_OFFSET, J_2_OFFSET, J_3_OFFSET, J_4_OFFSET, J_5_OFFSET};
const float home_position[N_JOINTS] = {0, 0, 0, 0, 0, 0};
String buffer;

void get_pwm(float pwm[], float theta[], float offset[]){
  for(int i = 0; i < N_JOINTS; i++){
    pwm[i] = map(theta[i] + offset[i], -90, 90, SERVOMIN, SERVOMAX);
  }
}

void write_position(float pwm[]){
  for(int i = 0; i < N_JOINTS; i++)
    driver.setPWM(i, 0, pwm[i]);
}

void execute_traj(float pwm[], float traj[N_POINTS][N_JOINTS], float offset[]){
  for(int i = 0; i < N_POINTS; i++){
      for(int j = 0; j < N_JOINTS; j++)
        pwm[j] = map(traj[i][j] + offset[j], -90, 90, SERVOMIN, SERVOMAX);
      write_position(pwm);
      delay(1000/F_POSITIONS);
  }
}

void homing(){
  get_pwm(pwm, home_position, offset);
  write_position(pwm);
}
          
void setup() {
  Serial.begin(9600);
  driver.begin();
  driver.setOscillatorFrequency(27000000);
  driver.setPWMFreq(SERVO_FREQ);
  delay(10);

  homing();
  delay(500);
}

void loop() {
  if(Serial.available()){
    Serial.readString();
    execute_traj(pwm, traj, offset);
  }
  homing();
}
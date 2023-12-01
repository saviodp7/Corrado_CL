#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "trj.h"

Adafruit_PWMServoDriver driver = Adafruit_PWMServoDriver();

#define SERVOMIN0  120
#define SERVOMAX0  489
#define SERVOMIN1  110
#define SERVOMAX1  475
#define SERVOMIN2  120
#define SERVOMAX2  475
#define SERVOMIN3  77
#define SERVOMAX3  463
#define SERVOMIN4  80
#define SERVOMAX4  460
#define SERVOMIN5  80
#define SERVOMAX5  460

#define N_POINTS  300
#define N_JOINTS  6
#define F_POSITIONS 50
#define SERVO_FREQ 50

float theta[N_JOINTS];
float pwm[N_JOINTS];
int servo_ns[N_JOINTS][2] = {SERVOMIN0, SERVOMAX0, SERVOMIN1, SERVOMAX1, SERVOMIN2, SERVOMAX2,
                             SERVOMIN3, SERVOMAX3, SERVOMIN4, SERVOMAX4, SERVOMIN5, SERVOMAX5};
const float home_position[N_JOINTS] = {-1.05,25.62,-58.44,-1.94,-32.84,1.63};
String buffer;

void get_pwm(float pwm[], float theta[], int servo_ns[][2]){
  for(int i = 0; i < N_JOINTS; i++){
    if(i == 0){
      pwm[i] = map(theta[i], -90, 80, servo_ns[i][0], servo_ns[i][1]);
    }
    else{
      pwm[i] = map(theta[i], -90, 90, servo_ns[i][0], servo_ns[i][1]);
    }
  }
}

void write_position(float pwm[]){
  for(int i = 0; i < N_JOINTS; i++)
    driver.setPWM(i, 0, pwm[i]);
}

void execute_traj(float pwm[], float traj[N_POINTS][N_JOINTS], int servo_ns[][2]){
  for(int i = 0; i < N_POINTS; i++){
    for(int j = 0; j < N_JOINTS; j++){
      if(j == 0){
        pwm[j] = map(traj[i][j], -90, 80, servo_ns[j][0], servo_ns[j][1]);
      }
      else{
        pwm[j] = map(traj[i][j], -90, 90, servo_ns[j][0], servo_ns[j][1]);
      }
    }
    write_position(pwm);
    delay(1000/F_POSITIONS);
  }
}

void homing(){
  get_pwm(pwm, home_position, servo_ns);
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
    execute_traj(pwm, traj, servo_ns);
  }
  homing();
}
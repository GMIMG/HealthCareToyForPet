#include "AccelStepper.h"
#include "MultiStepper.h"

////////////////////////소리 추가코드////////////////////////
#include <SoftwareSerial.h>
#include <DFPlayer_Mini_Mp3.h>

SoftwareSerial mySerial(9, 10); // RX, TX
///////////////////////////////////////////////////////////

//#define MOTOR_STEPS 1600  //1600이 한바퀴, 한스텝 0.9도
#define M1Rate 5
#define M2Rate 4
#define DIR1  6
#define DIR2  5
#define STEP1  3
#define STEP2  2
#define Mpin  7 //microstep
////////////////////////////////////////////////////
/////////////////////////////////모터 설정하기
AccelStepper stepper1(1, STEP1, DIR1);
AccelStepper stepper2(1, STEP2, DIR2); 
MultiStepper steppers;
long positions[2];
long pos[2];
int a=0, b=0; // pan, tilt 절대각도
int q=0; //char로 받은 데이터 열 
int k=0;

int s=0;

int ledPin = 8;  
int speakerpin = 9; //스피커가 연결된 디지털핀 설정

String inputString = ""; 
char inputStringC[8]={NULL};
boolean frameComplete = false;

int sensor1 = 11; // 포토인터럽터 핀 번호
int sensor2 = 12; // 포토인터럽터 핀 번호


void setup() {  
  /////////////////////////////////////////시리얼통신 설정
  Serial.begin(115200);  
  inputString.reserve(20);  //max 20 char. 

  ///////////////////////////////////////모터 초기설정
  //pinMode(Mpin, OUTPUT); //microstep
  //digitalWrite(Mpin, HIGH);

  stepper1.setMaxSpeed(1200);
  stepper1.setAcceleration(50);
  stepper2.setMaxSpeed(1200);
  stepper2.setAcceleration(50);
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0);
  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);

   /////////////////////////////////photointerrupt 초기설정 
  pinMode(sensor1, INPUT); // 포토인터럽터 입력으로 설정
  pinMode(sensor2, INPUT); // 포토인터럽터 입력으로 설정

  /////////////////////////////////레이저 초기설정
  pinMode(ledPin, OUTPUT);      // sets the digital pin as output   
  digitalWrite(ledPin, LOW);
  
  ////////////////////////////////소리 추가 초기설정
  //Serial.begin (9600);
  mySerial.begin (9600);
  mp3_set_serial (mySerial);  //set softwareSerial for DFPlayer-mini mp3 module 
  mp3_set_volume (30);
  } 
  
  
  
  
  
  
  
  
void loop() {

  if(frameComplete==true){
    Serial.print(inputStringC);
  ////////////////////연수 CODE 첨부하는 부분////////////////
   if (inputStringC[0]!='@'){
     s=0;///sound code
     if(inputString == "up\n"){ // 위 tilt
        positions[1]+=(-100)*M2Rate;
        steppers.moveTo(positions);
        steppers.runSpeedToPosition();
     }   
     else if(inputString == "down\n"){ // 아래 tilt
        positions[1] += (100)*M2Rate;
        steppers.moveTo(positions);
        steppers.runSpeedToPosition();
     }
     else if(inputString == "left\n"){ //왼쪽 pan
        positions[0]+=(100)*M1Rate;
        steppers.moveTo(positions);
        steppers.runSpeedToPosition();
     }
     else if(inputString == "right\n"){ // 오른쪽 pan
        positions[0] += (-100)*M1Rate;
        steppers.moveTo(positions);
        steppers.runSpeedToPosition();
     }
     
     else if(inputString == "stop\n"){
        digitalWrite(ledPin, LOW);
        
        stepper1.setCurrentPosition(0);
        stepper2.setCurrentPosition(0);
        init_stepmotor();
        positions[0]=0;
        positions[1]=0;
        stepper1.setCurrentPosition(0);
        stepper2.setCurrentPosition(0);
     }

     inputString="";
     frameComplete = false;
   }
    
   /////////////////////예은 CODE 첨부하는 부분//////////////////////////
   else if(inputStringC[0]=='@') { //1개는 무조건 '' 여러개는 무조건 ""
     if (s==0){        
       mp3_play (1);
       delay (5000);
       s=1;
        }
     else {
       mp3_play(2);
       delay(500);
     }  
      
      digitalWrite(ledPin, HIGH);
      
      
      //tone(speakerpin,500,500);  //500: 음의 높낮이(주파수), 1000: 음의 지속시간(1초)
      //delay(500);
      if (inputStringC[1]=='+'){
         pos[0]=(int)((inputStringC[2]-'0')*10+(inputStringC[3]-'0'));
      }
      else if (inputStringC[1] =='-'){
         pos[0]=(int)((inputStringC[2]-'0')*10+(inputStringC[3]-'0'));
         pos[0]=-pos[0];
      }
        
      if (inputStringC[4]=='+'){
        pos[1]=(int)((inputStringC[5]-'0')*10+(inputStringC[6]-'0'));
      }
      else if (inputStringC[4]=='-'){
        pos[1]=(int)((inputStringC[5]-'0')*10+(inputStringC[6]-'0'));
        pos[1]=-pos[1];
      }

      positions[0]=pos[0]*(800/180)*M1Rate;//(-400~+400)
      positions[1]=pos[1]*(800/180)*M2Rate;
      
      steppers.moveTo(positions);  //절대각도임(상대각도 아님)
      steppers.runSpeedToPosition();
      inputString = "";   
      frameComplete=false; 
    }//yeaun
    else{
    }
  //Serial.print((int)(positions[0]));
  //Serial.print(" ");
  //Serial.println((int)(positions[1]));
  }//frameComplete==ture

}//loop











void init_stepmotor() {
/*
  long po[2];
  int sm1=0;
  int sm2=0;
  for (int i=0; i<1000; i++){
    if(digitalRead(sensor2)){sm2=1;}
    if(digitalRead(sensor1)){sm1=1;}
    if (!sm2){
      if(i%2==1){po[0]=i*M1Rate;}
      else{po[0]=-i*M1Rate;}
    }
    if (!sm1){
      if(i%2==1){po[1]=i*M2Rate;}
      else{po[1]=-i*M2Rate;}
    }
    steppers.moveTo(po); 
    steppers.runSpeedToPosition();

  }
  */
  
  long po[2];
  int sm1=0;
  int sm2=0;
  po[0]=-50*(800/180)*M1Rate;
  po[1]=10*(800/180)*M2Rate;
  steppers.moveTo(po);
  steppers.runSpeedToPosition();
  delay(1000);
  
  for (int i=0;i<150;i++) {
    if(digitalRead(sensor2)){
      sm2=1;
    }
    if(digitalRead(sensor1)){
      sm1=1;
    }
  
    if (!sm2){
    po[0]+=(M1Rate*(800/180));
    }
    if (!sm1){
    po[1]+=(-M2Rate*(800/180));
    }
  
  steppers.moveTo(po); 
  steppers.runSpeedToPosition();
  }


}













void serialEvent() {
  
  while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    inputString += inChar;
    inputStringC[q]=inChar;
    q++;
    
    if (inChar == '\n') {      
      frameComplete = true;
      q=0;
      }
  }
}

#include "AccelStepper.h"
#include "MultiStepper.h"

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
  
  positions[0]=0;
  positions[1]=0;
  ///////////////////////////////////////모터 초기값 찾기
  
pinMode(sensor1, INPUT); // 포토인터럽터 입력으로 설정
pinMode(sensor2, INPUT); // 포토인터럽터 입력으로 설정


/*
  init_stepmotor(positions);
  positions[0]=0;
  positions[1]=0;
*/
  /////////////////////////////////레이저 초기설정
  pinMode(ledPin, OUTPUT);      // sets the digital pin as output   
  digitalWrite(ledPin, LOW);
  } 
  
void loop() {
  
  if (frameComplete==true){
    
////////////////////연수 CODE 첨부하는 부분////////////////
    if (inputStringC[0]!='@'){

   
     
       ////////////////////////////////////////////
         ////////////       위 tilt b     ////////////////
         ///////////////////////////////////////////
           if(inputString == "up\n"){
           //positions[0]
            positions[1]+=(-100)*M2Rate;
   
             steppers.moveTo(positions); 
             steppers.runSpeedToPosition();
             inputString="";
             frameComplete = false;
           }
          ////////////////////////////////////////////
         ////////////       아래 tilt     ////////////////
         ///////////////////////////////////////////
           else if(inputString == "down\n"){
             //positions[0]
            positions[1] += (100)*M2Rate;
   
             steppers.moveTo(positions); 
             steppers.runSpeedToPosition();
             inputString="";
             frameComplete = false;
           }
           ////////////////////////////////////////////
         ////////////       왼쪽 pan     ////////////////
         ///////////////////////////////////////////
           else if(inputString == "left\n"){
            positions[0]+=(100)*M1Rate;
            //positions[1]=positions[1]*(800/180)*M2Rate;
   
             steppers.moveTo(positions); 
             steppers.runSpeedToPosition();
             inputString="";
             frameComplete = false;
           }
          ////////////////////////////////////////////
         ////////////       오른쪽 pan   ////////////////
         ///////////////////////////////////////////
           else if(inputString == "right\n"){
             positions[0] += (-100)*M1Rate;
            //positions[1]=positions[1]*(800/180)*M2Rate;
   
             steppers.moveTo(positions); 
             steppers.runSpeedToPosition();
             inputString="";
             frameComplete = false;
           }
           
            else if(inputString == "stop\n"){
              k++;
              init_stepmotor(positions);
              positions[0]=0;
              positions[1]=0;
              //delay(1000);
              if(k%2==1){

              digitalWrite(ledPin, HIGH);}
            else
              {digitalWrite(ledPin, LOW);}
              
               inputString="";
             frameComplete = false;
           }
     
           
      
      }

       /////////////////////예은 CODE 첨부하는 부분//////////////////////////
      else if(inputStringC[0]=='@') { //1개는 무조건 '' 여러개는 무조건 ""
        digitalWrite(ledPin, HIGH);
        tone(speakerpin,500,500);  //500: 음의 높낮이(주파수), 1000: 음의 지속시간(1초)
        delay(500);   

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
      //positions[0]-=400*a;
      //positions[1]-=400*b;
      
      steppers.moveTo(positions);  //절대각도임(상대각도 아님)
      steppers.runSpeedToPosition();
      inputString = "";   
      frameComplete=false; 
    
      }//yeaun
      
      else{
      }
  }//if(framecomplete)
}//loop


void init_stepmotor(long positions[]) {
  int sm1=0;
  int sm2=0;
  positions[0]+=-60*(800/180)*M1Rate;
  positions[1]+=20*(800/180)*M2Rate;
  steppers.moveTo(positions); 
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
  positions[0]+=(M1Rate*(800/180));
  }
  if (!sm1){
  positions[1]+=(-M2Rate*(800/180));
  }
  
  steppers.moveTo(positions); 
  steppers.runSpeedToPosition();
  }

  positions[1]+=(10*(800/180)*M2Rate);
  steppers.moveTo(positions);
  steppers.runSpeedToPosition();
}

void serialEvent() {  
  while (Serial.available()) {
        
    char inChar = (char)Serial.read();
    //while(1){
      //if(inChar=='@'){break;}
      //}    
    inputString += inChar;
    inputStringC[q]=inChar;
    q++;    
    if (inChar == '\n') {      
      frameComplete = true; 
      q=0;   
      }  
      } 
      }


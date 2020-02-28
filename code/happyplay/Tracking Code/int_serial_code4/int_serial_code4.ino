#include <AccelStepper.h>
#include <MultiStepper.h>

#define MOTOR_STEPS 1600  //1600이 한바퀴, 한스텝 0.9도
#define M1Rate 5
#define M2Rate 4
#define DIR1  6
#define DIR2  5
#define STEP1  3
#define STEP2  2

////////////////////////////////////////////////////
/////////////////////////////////모터 설정하기
AccelStepper stepper1(1, STEP1, DIR1);
AccelStepper stepper2(1, STEP2, DIR2); 
MultiStepper steppers;
long positions[2];
int a=0, b=0; // pan, tilt 절대각도
int q=0; //char로 받은 데이터 열 

String inputString = ""; 
char inputStringC[8]={NULL};
boolean frameComplete = false; 


void setup() {  
  /////////////////////////////////////////시리얼통신 설정
  Serial.begin(115200);  
  inputString.reserve(20);  //max 20 char. 


  ///////////////////////////////////////모터 초기설정
  stepper1.setMaxSpeed(5000);
  stepper1.setAcceleration(4000);

  stepper2.setMaxSpeed(5000);
  stepper2.setAcceleration(4000);
  
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0); 

  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);

  positions[0]=0;
  positions[1]=0;

   
  } 
  
void loop() {  
  if (frameComplete==true){
////////////////////연수 CODE 첨부하는 부분////////////////
    if (inputStringC[0]!='@'){
       ////////////////////////////////////////////
         ////////////       위 tilt b     ////////////////
         ///////////////////////////////////////////
           if(inputString == "up\n"){
           b+=1;
           stepper2.move(400*M2Rate);
           while (stepper2.currentPosition() != 400*M2Rate) 
           { stepper2.run(); }
             stepper2.stop(); 
             stepper2.setCurrentPosition(0);
             inputString="";
             frameComplete = false;
           }
          ////////////////////////////////////////////
         ////////////       아래 tilt     ////////////////
         ///////////////////////////////////////////
           else if(inputString == "down\n"){
            b-=1;
           stepper2.move(-400*M2Rate);
           while (stepper2.currentPosition() != -400*M2Rate) 
           { stepper2.run(); }
             stepper2.stop(); 
             stepper2.setCurrentPosition(0);
             inputString="";
             frameComplete = false;
           }
           ////////////////////////////////////////////
         ////////////       왼쪽 pan     ////////////////
         ///////////////////////////////////////////
           else if(inputString == "left\n"){
            a+=1;
           stepper1.move(400*M1Rate);
           while (stepper1.currentPosition() != 400*M1Rate) 
           { stepper1.run(); }
             stepper1.stop(); 
             stepper1.setCurrentPosition(0);
             inputString="";
             frameComplete = false;
           }
          ////////////////////////////////////////////
         ////////////       오른쪽 pan   ////////////////
         ///////////////////////////////////////////
           else if(inputString == "right\n"){
            a-=1;
           stepper1.move(-400*M1Rate);
           while (stepper1.currentPosition() != -400*M1Rate) 
           { stepper1.run(); }
             stepper1.stop(); 
             stepper1.setCurrentPosition(0);
             inputString="";
             frameComplete = false;
           }
     
           
      
      }

       /////////////////////예은 CODE 첨부하는 부분//////////////////////////
      else if(inputStringC[0]=='@') { //1개는 무조건 '' 여러개는 무조건 "".

      if (inputStringC[1]=='+'){
         positions[0]=(int)((inputStringC[2]-'0')*10+(inputStringC[3]-'0'));
        
        }

      else if (inputStringC[1] =='-'){
         positions[0]=(int)((inputStringC[2]-'0')*10+(inputStringC[3]-'0'));
         positions[0]=-positions[0];
        }

      if (inputStringC[4]=='+'){
        positions[1]=(int)((inputStringC[5]-'0')*10+(inputStringC[6]-'0'));
        }

      else if (inputStringC[4]=='-'){
        positions[1]=(int)((inputStringC[5]-'0')*10+(inputStringC[6]-'0'));
        positions[1]=-positions[1];
        }
        
      positions[0]=positions[0]*(800/180)*M1Rate;//(-400~+400)
      positions[1]=positions[1]*(800/180)*M2Rate;
      //positions[0]-=400*a;
      //positions[1]-=400*b;
      
      steppers.moveTo(positions);  //절대각도임(상대각도 아님)
      steppers.runSpeedToPosition();
      inputString = "";   
      frameComplete=false; 
    
}}}


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


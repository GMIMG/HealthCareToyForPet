#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


//서보모터 + 초음파
#include <Servo.h>
#include <NewPing.h>
Servo servo1, servo2;
float posDegrees1= 0, pre_posDegrees1=0; // 위
float posDegrees2= 0, pre_posDegrees2=0; // 아래
#define TRIGGER_CH4_PIN  2 //첫번째 Trigger pin/오른쪽부터 반시계방향
#define ECHO_CH4_PIN     16  //첫번째 Echo pin
#define TRIGGER_CH3_PIN  4 //두번째 Trigger pin
#define ECHO_CH3_PIN     17  //두번째 Echo Pin
#define TRIGGER_CH2_PIN  2 //세번째 Trigger pin
#define ECHO_CH2_PIN     27 //세번째 Echo pin
#define TRIGGER_CH1_PIN  4  //네번째 Trigger pin
#define ECHO_CH1_PIN     26  //네번째 Echo Pin
#define MAX_DISTANCE 50  //최대 측정 거리 설정(단위 cm)
//첫번째 NewPing 라이브러리 생성 (핀(TRIG, ECHO)과 최대 거리 설정)
NewPing sonar_ch1(TRIGGER_CH1_PIN, ECHO_CH1_PIN, MAX_DISTANCE); 
//두번째 NewPing 라이브러리 생성 (핀(TRIG, ECHO)과 최대 거리 설정)
NewPing sonar_ch2(TRIGGER_CH2_PIN, ECHO_CH2_PIN, MAX_DISTANCE); 
//세번째 NewPing 라이브러리 생성 (핀(TRIG, ECHO)과 최대 거리 설정)
NewPing sonar_ch3(TRIGGER_CH3_PIN, ECHO_CH3_PIN, MAX_DISTANCE); 
//네번째 NewPing 라이브러리 생성 (핀(TRIG, ECHO)과 최대 거리 설정)
NewPing sonar_ch4(TRIGGER_CH4_PIN, ECHO_CH4_PIN, MAX_DISTANCE); 
float sum_ave=0;
int count=0;
float Y=0, Y1=0, Y2=0, R1=0, R2=0, Deg1=0, Deg2=0, Deg=0, X1=0, X2=0, Deltax=0,  Deltay=0, r=0;
double so[4]={0};
int f=0, a=0, b=0, v=0, kk=0; 
float max=1, min=1;
float num[4][5]={{0},{0}};
float sum[4],ave[4]={0}; 
float x1=0, x2=0, x3=0; float y=0, y2=0, y3=0, deg_servo=0, rs=0, deg1=0, deg2=0, r1=0, r2=0, whe=0, rad=3.14159/180;
static const int servoPin1 = 25, servoPin2 = 22;
int pre_dir=0, dir=0;
int m=0;
int dog_size=1;
int e=0;
float dogspeed=18*3.14/180;
float deltax=0, deltay=0;
float size_of_vector=0;
float unit_vector_x=0,unit_vector_y=0;
int dogactive=0;
void sumsum(){
  for(b=0; b<4; b++){
  sum[b]={0}; //sum에 값이 계속 누적되면 안됨.
  max=num[b][0]; min=num[b][0];
  for(a=0; a<5; a++){
   if(num[b][a]>=max){
      max=num[b][a];
   }
   else{
        if(num[b][a]<=min){
            min=num[b][a]; }
        }
   }
   for(a=0; a<5; a++){
    sum[b]+=num[b][a];
    }
  ave[b]=(sum[b]-max-min)/3;
    //return ave;
  }
}
     
void R_Angle(){
  

  whe=90-atan(rs/38)*(180/3.14159);

}

void pantilt(){
  
so[0]=sonar_ch1.ping_cm();
so[1]=sonar_ch2.ping_cm();
so[2]=sonar_ch3.ping_cm();
so[3]=sonar_ch4.ping_cm();
for(b=0; b<4; b++){
  for(a=0; a<5; a++){
    num[b][a]=so[b];
    }
}
    
  sumsum();
  for(b=0; b<4; b++){
   Serial.println(ave[b]);}
   Serial.println("");
   delay (100);//최소한 29ms(50)이상은 대기를 해야한다고 함.

if((ave[0]+ave[1]+ave[2]+ave[3])==0){
  posDegrees1=pre_posDegrees1;
  posDegrees2=pre_posDegrees2;
  count++;
  if (count==15){
  posDegrees1=30;
  posDegrees2=90;
  count=0;
  }
}

  
else{
count=0; 
NEW_DIR();

deltax=(x2)-(x1);   deltay=(y2)-(y);
size_of_vector=sqrt((deltax)*(deltax)+(deltay)*(deltay));
unit_vector_x=deltax/size_of_vector;
unit_vector_y=deltay/size_of_vector;


x3=x2+(dog_size)*(unit_vector_x);                                                                                                                 
y3=y2+(dog_size)*(unit_vector_y);
 


deg_servo=atan(y3/x3)*180/3.14159; //xy 좌표를 r세타 좌표로 바꿈
rs=sqrt(x3*x3+y3*y3);

R_Angle(); 
posDegrees1=whe;
if(deg_servo<0){
posDegrees2=180+deg_servo;}

  if(deg_servo>0){
posDegrees2=deg_servo;}

x1=x2; y=y2;
  



}

if (isnan(posDegrees1)){
  posDegrees1=30;
}
if (posDegrees1 > 70){
  posDegrees1=70;
}
servo1.write(posDegrees1);
pre_posDegrees1=posDegrees1;

delay(50);
servo2.write(posDegrees2);
pre_posDegrees2=posDegrees2;





delay(50);
Serial.println("");
Serial.print("servo1=");
Serial.println(posDegrees1);
Serial.print("servo2=");
Serial.println(posDegrees2);
Serial.println("");
}

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);
char hourchar[3];
char minchar[3];
char secchar[3];
char ac[4];
int PLAYE = 21;
int value = 0;
int hour,mini,sec ,dis;
int goal=1000;
String actdata;
int q=0;
int REC=36;
int play=0;
int swPin=32;
int button=0;
#define Lazor_PIN 33
/*와이파이 설정*/
//const char *ssid = "Sound_2.4GHz";
//const char *password = "dmagidtlf";
//const char* ssid = "AndroidHotspot8192";      
//const char* password = "yeeun1212";  
//const char* ssid = "AndroidHotspot9360";      
//const char* password = "godvoice";
const char* ssid = "ktEgg_413";
const char* password = "info04813";

//const char* host = "192.168.28.63";
//const char* host = "192.168.43.251";
const char* host = "192.168.1.42";

void setup() {
  
  pinMode (Lazor_PIN,OUTPUT);
  pinMode (swPin,INPUT);
  /*콜백함수관련*/
  Serial.begin(115200);
  
//서보모터
   servo1.attach(servoPin1);
   servo2.attach(servoPin2);
  
//스피커
  pinMode (REC,OUTPUT);
  pinMode (PLAYE,OUTPUT);

//와이파이 접속
  delay(10);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
//  while (WiFi.status() != WL_CONNECTED) {
//    delay(500);
//   Serial.print(".");
//  }
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
//시간
  timeClient.begin();
}

void loop() {
  
  if(digitalRead(swPin) == HIGH){
  button=1;
}
else{
  button=0;
}

  /*콜백함수*/
  delay(5000);
  ++value;
// Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
}
  
  String url = "/";
//  url += streamId;
//  url += "?private_key=";
//  url += privateKey;
//  url += "&value=";
//  url += value;

  // This will send the request to the server
client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
int timeout = millis() + 5000;
while (client.available() == 0) {
  if (timeout - millis() < 0) {
    Serial.println(">>> Client Timeout !");
    client.stop();
    return;
  }
}

  // Read all the lines of the reply from server and print them to Serial
while(client.available()){
 String actdata = client.readStringUntil('\r');
 actdata.substring(303,306).toCharArray(ac,4);
 if(ac[0]=' '){
  q =atoi(ac);
  }
}


if(digitalRead(swPin) == HIGH){
  button=1;
}
else{
  button=0;
}


   
  Serial.println(q);
  /*NTP 시간*/
  timeClient.update();
  String k=timeClient.getFormattedTime();
    k.substring(0,2).toCharArray(hourchar,3);
    k.substring(3,5).toCharArray(minchar,3);
    k.substring(6,8).toCharArray(secchar,3);
    hour=atoi(hourchar);
    mini=atoi(minchar);
    sec=atoi(secchar);
    hour= hour + 9;
    if (hour>24){
      dis=hour-24;
      hour=dis;
    }
       Serial.printf("%d\t",hour);
       Serial.printf("%d\t",mini);
       Serial.printf("%d\t",sec);
       Serial.println();
       
  if (((hour==13)&&(mini==0)&&(sec>=0)&&(sec<10)) || ((hour==18)&&(mini==0)&&(sec>=0)&&(sec<10))){ //13시와 18시에 활동량 체크    
    Serial.println('check');
    if (q < goal){
      play=1;
    }
  String url = "/1";
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
  int timeout = millis() + 5000;
  while (client.available() == 0) {
    if (timeout - millis() < 0) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }
  }

if(digitalRead(swPin) == HIGH){
  button=1;
}
else{
  button=0;
}



Serial.println(play);
Serial.println(button);
Serial.println(digitalRead(swPin));


if (button==1){
  play=1;
}

if (play==1){
  digitalWrite (Lazor_PIN, HIGH);
  delay(10);
  digitalWrite(PLAYE,HIGH);
  delay(10);
  digitalWrite(PLAYE,LOW);
        
  while(1){
  pantilt();
  if (dogactive==1){
  break;
  }
}
  
  /// 활동량값 초기화
  String url = "/1";
  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
  int timeout = millis() + 5000;
  while (client.available() == 0) {
    if (timeout - millis() < 0) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }
play=0;
servo1.write(30);
delay(50);
servo2.write(90);
delay(50);
}
}


void NEW_DIR(){
 /*최종적으로 이 함수에서 나오는 값은 그 위치에서의 x,y 좌표이다*/

for (v=0;v<3;v++){
  if((ave[v]&&ave[v+1])!=0){
    R1=ave[v]+15;
    R2=ave[v+1]+15;
    Deg1=(36*(v+1));
    Deg2=(36*(v+2));
    X1=R1*cos(Deg1*rad);  Y1=R1*sin(Deg1*rad);
    X2=R2*cos(Deg2*rad);  Y2=R2*sin(Deg2*rad);

    Deltax=(X2)-(X1);   Deltay=(Y2)-(Y1);

    x2=X1+(R1/(R1+R2))*Deltax;
    y2=Y1+(R1/(R1+R2))*Deltay;  //이 값이 두개 겹쳤을때 구한 x,y 좌표
    
  kk=2;
  }
  }


if (kk!=2){
kk=1;
for (v=0;v<4;v++){
  if (ave[v] != 0){
  r=ave[v];
  Deg=36*(v+1);
  }
r2=r+15;
deg2=Deg;
x2=r2*cos(deg2*rad);  y2=r2*sin(deg2*rad); //위치 한개만 있을때 나오는 각도
}
////
}
else
kk=0;
}


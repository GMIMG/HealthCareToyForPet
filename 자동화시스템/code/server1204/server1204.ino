#include "I2Cdev.h"
#include "MPU6050.h"
#include <math.h>
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
MPU6050 accelgyro;
#define OUTPUT_READABLE_ACCELGYRO
bool blinkState = false;
#include<EthernetClient.h> //Uncomment this library to work with ESP8266
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
WiFiClient client;

//그래프 변수
float oldy[41];
int graph[41];
//가속도센서
int16_t ax, ay, az, gx, gy, gz;
float i=0;
float j=0;
float k=0;
float l=0;
float re=0;
float ypr[3];      
float old_ypr[3]={0,0,0};
float oy=0;
int q=0;
int n=0;
int h=0;


//const char* ssid = "AndroidHotspot8192";      
//const char* password = "yeeun1212";


const char* ssid = "ktEgg_413";
const char* password = "info04813";

//const char* ssid = "AndroidHotspot9360";
//const char* password = "godvoice";

//const char* ssid = "Sound_2.4GHz";      
//const char* password = "dmagidtlf";

ESP8266WebServer server ( 80 );
int status = WL_IDLE_STATUS;
char server2[] = "api.thingspeak.com";
String apiKey="HU81CWJ8U9PR5Q74";
const int led = 13;



void setup ( void ) {
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

  for(h=0;h<40;h++){
  oldy[h]= 0;
  }

  pinMode ( led, OUTPUT );
  digitalWrite ( led, 0 );
  Serial.begin ( 115200 );
  accelgyro.initialize();

  WiFi.begin ( ssid, password );
  Serial.println ( "" );

  // Wait for connection
  while ( WiFi.status() != WL_CONNECTED ) {
    delay ( 1000 );
    Serial.print ( "." );
  }
  Serial.println ( "" );
  Serial.print ( "Connected to " );
  Serial.println ( ssid );
  Serial.print ( "IP address: " );
  Serial.println ( WiFi.localIP() );

  if ( MDNS.begin ( "esp8266" ) ) {
    Serial.println ( "MDNS responder started" );
  }
  server.on ( "/", handleRoot );
  server.on ( "/1", handle1 );
  server.on ( "/test.svg", drawGraph );
  server.on ( "/inline", []() {
  server.send ( 200, "text/plain", "this works as well" );
  } );
  server.onNotFound ( handleNotFound );
  server.begin();
  Serial.println ( "HTTP server started" );
}









void loop ( void ) {
  
 accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
   
  oldy[40]=abs((abs(ax-old_ypr[0])+abs(ay-old_ypr[1])+abs(az-old_ypr[2]))*140/3/16384-40);
  
   ax= 0.09*old_ypr[0]+ 0.01*ax;
   ay= 0.09*old_ypr[1]+ 0.01*ay;
   az= 0.09*old_ypr[2]+ 0.01*az;
   
 i=i+abs(ax-old_ypr[0]);
 j=j+abs(ay-old_ypr[1]);
 k=k+abs(az-old_ypr[2]);
 l=0.001*sqrt((i*i)+(j*j)+(k*k));

  old_ypr[0]=ax;
  old_ypr[1]=ay;
  old_ypr[2]=az;


  for(h=0;h<=39;h++){
    oldy[h]= oldy[h+1];
  }





 
    #ifdef OUTPUT_READABLE_ACCELGYRO
        // display tab-separated accel/gyro x/y/z values
    /*  Serial.print("a/g:\t");
        Serial.print(ax); Serial.print("\t");
        Serial.print(ay); Serial.print("\t");
        Serial.print(az); Serial.print("\t");
        Serial.print(gx); Serial.print("\t");
        Serial.print(gy); Serial.print("\t");
        Serial.println(gz);
            Serial.println(i);        
            Serial.print("\t");
            Serial.println(j);       
            Serial.print("\t");
            Serial.println(k);
            Serial.print("\t");
         */
            Serial.println(l);
            delay(500);
            
            q++;


            if(q==80){
              q=0;
            



              

            if (client.connect(server2, 80)) {
          Serial.println("connected to server2");
          
          client.print(F("POST "));
          client.print("/update?key=apiKey&field1=" 
          +               (String) l
          +  "&field2=" +(String) oldy[40]
          );
                                      
          String tsData = "field1="   //need the length to give to ThingSpeak
          +             (String)  l;
          +  "&field2=" +(String) oldy[40] ; 
          client.print("POST /update HTTP/1.1\n");  
          client.print("Host: api.thingspeak.com\n");
          client.print("Connection: close\n");
          client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
          client.print("Content-Type: application/x-www-form-urlencoded\n");
          client.print("Content-Length: ");
          client.print(tsData.length());  //send out data string legth to ts
          client.print("\n\n");
          client.print(tsData);
          client.stop();
          delay(500);
          re=0;
          
    } }
    #endif
    blinkState = !blinkState;
    digitalWrite(led, blinkState);
  server.handleClient();

}













void drawGraph() {  //그래프

  for(int x=0;x<=40;x++){
    graph[x]=(int)oldy[x];
  Serial.print(oldy[x]);
  Serial.print("\t");
  }
  Serial.println();
  
  String a = "";
  String out = "";
  char temp[100];
  out += "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"400\" height=\"200\">\n";
  out += "<rect width=\"400\" height=\"200\" fill=\"rgb(250, 230, 210)\" stroke-width=\"1\" stroke=\"rgb(0, 0, 0)\" />\n";
  out += "<g stroke=\"black\">\n";
  int y = (int) l;
  for (int x = 10; x < 390; x+= 10) {
    sprintf(temp, "<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke-width=\"1\" />\n", x, 200-graph[x/10], x + 10, 200-graph[x/10+1]);
    out += temp;
  }
  out += "</g>\n</svg>\n";

  server.send ( 200, "image/svg+xml", out);

}



void handle1() {  //초기화
 i=0;
 j=0;
 k=0;
 old_ypr[0]=0;
 old_ypr[1]=0;
 old_ypr[2]=0;
}


void handleRoot() { 
  digitalWrite ( led, 1 );
  char temp[400];
  int sec = millis() / 1000;
  int min = sec / 60;
  int hr = min / 60;
  int c= (int)l;
  snprintf ( temp, 400,
"<html>\
  <head>\
    <meta http-equiv='refresh' content='5'/>\
    <title>ESP8266 Demo</title>\
    <style>\
      body { background-color: #cccccc; font-family: Arial, Helvetica, Sans-Serif; Color: #000088; }\
    </style>\
  </head>\
  <body>\
    <h1>Hello yeeun's Dog!</h1>\
    <p>Uptime: %02d:%02d:%02d</p>\
        <h2>ac: %d          </h2>\
    <img src=\"/test.svg\" />\
  </body>\
</html>",

    hr, min % 60, sec % 60 , c
  );
  server.send ( 200, "text/html", temp );
  digitalWrite ( led, 0 );
}




void handleNotFound() {
  digitalWrite ( led, 1 );
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += ( server.method() == HTTP_GET ) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for ( uint8_t i = 0; i < server.args(); i++ ) {
    message += " " + server.argName ( i ) + ": " + server.arg ( i ) + "\n";
  }
  server.send ( 404, "text/plain", message );
  digitalWrite ( led, 0 );
}

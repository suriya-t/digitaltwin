#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>


int counter = 0;
int aState;
int aLastState;  
int mapp=0, i;
int prevValue;
String n;
String a;
WiFiClient client;

const uint16_t port = 8585;
const char *host = "192.168.225.204";


void setup()
{
  Serial.begin(115200);

  Serial.println("Connecting...\n");
  WiFi.mode(WIFI_STA);

  WiFi.begin("JioFi3_6A29C5", "33jawvj79w"); // change it to your USSID and PASSWORD
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  if (!client.connect(host, port))
  {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }

  Serial.println("Connected to server successful!");
  delay(250);
  

}

void loop()
{ 
     for(i=0; i<34;++i){
      if(i<10)
      {
        a= '0'+String(i);
      }
      else
      {
        a=String(i);
      }
      Serial.println(a);
      client.print(a);
      delay(100);
     }
   // Reads the "current" state of the outputA
   // If the previous and the current state of the outputA are different, that means a Pulse has occured
     for(i=34; i>0;--i){
      if(i<10)
      {
        a= '0'+String(i);
      }
      else
      {
        a=String(i);
      }
      Serial.println(a);
      client.print(a);
      delay(100);
     }

}

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

#define outputA D3
#define outputB D4

int counter = 0;
int aState;
int aLastState;  
int mapp=0;
int prevValue;
String n;
String a;
WiFiClient client;

const uint16_t port = 8585;
const char *host = "192.168.10.63";


void setup()
{
  Serial.begin(115200);

  Serial.println("Connecting...\n");
  WiFi.mode(WIFI_STA);

  WiFi.begin("Airtel_9940095045", "air22581"); // change it to your USSID and PASSWORD
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
  
  pinMode (outputA,INPUT);
  pinMode (outputB,INPUT);

  // Reads the initial state of the outputA
  aLastState = digitalRead(outputA);

}

void loop()
{ 
   

  aState = digitalRead(outputA); // Reads the "current" state of the outputA
   // If the previous and the current state of the outputA are different, that means a Pulse has occured
  if (aState != aLastState){

    // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
    if (digitalRead(outputB) != aState)
    {++counter;}
    else
    {--counter;}

    mapp=map(counter,0,50,0,34);
    if(counter<0)
    {counter=0;}
    else if(counter>50)
    {counter=50;}

    if(mapp != prevValue){
      if(mapp<10)
      {
        a= '0'+String(mapp);
      }
      else
      {
        a=String(mapp);
      }
      Serial.println(a);
      client.print(a);
      prevValue = mapp;
    }
  }
  aLastState = aState;

}

#include <CapacitiveSensor.h>  //declare library
CapacitiveSensor capSensor1 = CapacitiveSensor(12,13); //pin sensor connection
CapacitiveSensor capSensor2 = CapacitiveSensor(10, 11);
CapacitiveSensor capSensor3 = CapacitiveSensor(9, 8);
CapacitiveSensor capSensor4 = CapacitiveSensor(6, 7);

int red=4;
int blue=5;
int green=6;
int readr = 0;
int readg = 0;
int readb = 0;
int reade = 0;
long readp = 0;
String string="00000";
int t = 200;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  /*digitalWrite(red, HIGH); 
  digitalWrite(blue, HIGH); 
  digitalWrite(green, HIGH);*/
}

void loop() {
  // put your main code here, to run repeatedly:
  readr = capSensor1.capacitiveSensor(30);
  readg = capSensor2.capacitiveSensor(30);
  readb = capSensor3.capacitiveSensor(30);
  reade = capSensor4.capacitiveSensor(30);
  //Serial.println(readr);
  //Serial.println(readg);
  //Serial.println(readb);
  //Serial.println(reade);
  //readp = capSensor.capacitiveSensor(30);
  if(readr > t){
    if(string[2] == '0'){
      string[2] = '1';
      //digitalWrite(red, LOW);
    }
    else{
      string[2] = '0';
      //digitalWrite(red, HIGH);
    }
  }
  if(readg > t){
    if(string[3] == '0'){
      string[3] = '1';
      //digitalWrite(blue, LOW);
    }
    else{
      string[3] = '0';
      //digitalWrite(blue, HIGH);
    }
  }
  if(readb > t){
    if(string[4] == '0'){
      string[4] = '1';
      //digitalWrite(green, LOW);
    }
    else{
      string[4] = '0';
      //digitalWrite(green, HIGH);
    }
  }
  /*if(readp > 600){
    string[0] = '1';
  }
  else{
    string[0] = '0';
  }*/
  
  if(reade > t){
    if(string[1] == '0'){
      string[1] = '1';
    }
    else{
      string[1] = '0';
    }
  }
  Serial.println(string);
  delay(50);
}

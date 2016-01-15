/*
  lm35 sketch
 prints the temperature to the Serial Monitor
 */

const int inPin = 0; // analog pin


void setup()
{
  pinMode(13, OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(9600);
  Serial.println("Dati da LM35");
}


void loop()
{
  float value_media;
  int value=0;
  int value_somma=0;
 
 //Legge 10 valori ogni secondo
  for (int i=0; i<10; i++)
 { 
  value = analogRead(inPin);
  //Serial.println(value);
  value_somma=value_somma + value;
  delay(1000);
  }
  //Calcola la media
  value_media=value_somma/10;
  
  //Serial.print(value_media); Serial.print(" > ");
  float millivolts = (value_media / 1024.0) * 5000;
  float celsius = millivolts / 10;  // sensor output is 10mV per degree Celsius
  Serial.print("T");
Serial.println(celsius);
}
      
    

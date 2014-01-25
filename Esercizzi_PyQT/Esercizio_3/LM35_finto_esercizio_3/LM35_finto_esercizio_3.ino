/*
  lm35 sketch
 prints the temperature to the Serial Monitor
 */

void setup()
{
  pinMode(13, OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(9600);
  Serial.println("Dati da LM35");
}


void loop()
{
Serial.println("T20.15");
delay(1000);
}
      
    

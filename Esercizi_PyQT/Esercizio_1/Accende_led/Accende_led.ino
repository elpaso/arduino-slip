int dato;


void setup()
{
     // Inicializamos puerto serie a 9600 bps
     Serial.begin(9600);
     pinMode(13, OUTPUT);
     // Enviamos "Hello World" con salto de línea al final
     
     Serial.println("Conectado con el Arduino. Hello world!");
     //arduino manda esta cadena al PC
}
 
void loop()
{
     //¿Existen datos por el puerto serie?
     if (Serial.available()) {
          //Guardamos el dato por la variable dato
          dato=Serial.read();
         // Serial.println(dato);
          switch (dato) {
               case 49:
                    // escribo 1 en el PC y lo envio
                    //Apagamos el led 13
                    digitalWrite(13,LOW);
                     Serial.println("Arduino: He apagado el led 13");
               break;
               case 48:
                     // escribo 0 en el PC y lo envio al arduino
                    //Encendemos el led 13
                    digitalWrite(13,HIGH);
                    Serial.println("Arduino: He encendido el led 13");
               break;
          }
     }
}

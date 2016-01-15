/*
  Clock Calendar con il chip DS1307.
  

  Visualizzazione su Serial Monitor e su 
                     LCD alfanumerico I2c
  ....................................................................
  Comandi inviabili da un Serial monitor  
  --------------------------------------------------------------------
  Aggiornamento Clock Calendar da Terminale
  Inserire: #, ore, minuti, secondi, giorno, mese, anno, /
  Esempio: #14130516052013/
           #=controllo, 14=ore,   13=minuti, 05=secondi, 
          16=giorno,    05=mese,  2013=anno, /=controllo
  --------------------------------------------------------------------
  Aggiornamento intervallo letture termometri
  Inserire: * + un numero da 1 a 59 (minuti)
            il numero verrà messo in EEPROM interna.
  Esempio: *02/ (intervallo letture = 2 minuti)      
  --------------------------------------------------------------------
  Lettura EEprom e visualizzazione su Serial Port
  Inserire: ?
  Esempio: ?/
  --------------------------------------------------------------------
  Visualizzazione nome programma, parametri:
  Inserire: v
*/

char Sketch[]="Sketch: Python_Carlo_GB_00";

char ricevuto;     //Un byte ricevuto dalla porta seriale.
int scelta;

const int N_dati=100;
int led = 13;
int ore=1;
int minuti=1;
int secondi=1;
int giorno=1;
int mese=1;
int anno=2000;


//---Prototipi delle funzioni---------------------------------------------------

//---Predisposizione------------------------------------------------------
void setup(){
  Serial.begin(9600);
Serial.println(Sketch);
pinMode(led, OUTPUT); 
digitalWrite(led, LOW);
}
//---Ciclo principale-----------------------------------------------------
void loop(){
  if(Serial.available()>0){      //Se ci sono caratteri in arrivo.
    ricevuto=Serial.read();      //Legge un byte dalla seriale.
    scelta = ricevuto;
    switch (scelta) {
      case 76: // Carattere L
        Invia_dati();
        break;
      case 80: // Carattere P
        Serial.println(ricevuto);
        break;
      default: 
        Serial.println("nulla da fare!");
}
}
}

 void Invia_dati(void){ 
   digitalWrite(led, HIGH);
   Serial.println("S");
   for (int i=0; i<N_dati; i++){
    Serial.print("D");
    Serial.print(";");  
    Serial.print(ore);
    ore ++;
    Serial.print(";");
    Serial.print(minuti);
    minuti ++;
    Serial.print(";");
    Serial.print(secondi);
    secondi ++;
    Serial.print(";");
    Serial.print(giorno);
    giorno ++;
    Serial.print(";");
    Serial.print(mese);
    mese ++;
    Serial.print(";");
    Serial.println(anno);
    anno ++;
  }
 Serial.println("E");
 digitalWrite(led, LOW); 
}

//---Invio EEprom I2c al terminale--------------------------------------------

//---Scrive su EEprom I2C la temperatura rilevata-----------------------------

//---Legge da EEprom I2C la temperaura----------------------------------------

//---Ricerca sonde inserite-----------------------------------------------------

//---Lettura termometri---------------------------------------

//---Stampa indirizzo sul monitor -----------------------------------

//---Controlla indirizzo---------------------------------------------

//---Visualizza Orario-------------------------------------------------

//---Aggiorna Orologio-------------------------------------------------

//---Vusualizza stringhe-----------------------------------------------

//---Visualizzazione mesaggi--------------------------------------------------


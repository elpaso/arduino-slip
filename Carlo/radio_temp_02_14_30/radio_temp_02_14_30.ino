/*
  Data Logger
  Visualizzazione su Serial Monitor e su 
                     LCD alfanumerico I2c
  ....................................................................
  Comandi inviabili da un Serial monitor  
  --------------------------------------------------------------------
  Aggiornamento Clock Calendar da Terminale
  Inserire: #, ore, minuti, secondi, giorno, mese, anno, /
  Esempio: #141305160214/
           #=controllo, 14=ore,   13=minuti, 05=secondi, 
          16=giorno,    02=mese,  14=anno, /=controllo
  --------------------------------------------------------------------
  Aggiornamento intervallo letture termometri
  Inserire: * + un numero da 1 a 59 (minuti)
            il numero verrà messo in EEPROM interna.
  Esempio: *02/ (intervallo letture = 2 minuti) 
  --------------------------------------------------------------------
  Lettura  intervallo letture e invia alla Serial Port
  Inserire: % + invio
  --------------------------------------------------------------------
  Lettura EEprom letture e visualizza "tipo tabella" su Serial Port
  Inserire: ? + invio
  --------------------------------------------------------------------
  Lettura EEprom e invia alla Serial Port
  Inserire: @ + invio
  --------------------------------------------------------------------
  Visualizzazione nome programma, parametri:
  Inserire: v
*/
#include <SPI.h>
#include <Wire.h>       //Libreria I2c. 
#include "I2C_Ind_1B.h" //Per Clock Calendar.
#include "I2C_Ind_2B.h" //Per EEprom I2C.
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include<EEPROM.h>
char Sketch[]="  Sketch: radio:temp_02_14_30.ino 14314 byte, data: 02-03-2014";
byte num=1;
byte G_addr[10][8]; //Indirizzi dei termometri inseriti nel BUS.
byte G_Devices;     //variabile usata per tenere traccia dei sensori riconosciuti.
OneWire ow(5);      //Porta dove sono collegati i sensori.
float temperatura;
float temp_eccess;  //Variabile controllo soglia impostata.
byte LED1=7;
byte abil_vis=1;   //Abilita visualizzazione.
byte ricevuto;     //Un byte ricevuto dalla porta seriale.
byte orario[15];   //Array contenente il messaggio da visualizzare.
byte n_ric=0;      //Numero caratteri ricevuto dalla porta seriale.
byte ric_piu=0;    //Abilita ricezione dal secondo carattere.
char primo;
char ultimo;       //Ultimo carattere ricevuto.
byte interv[3];
byte intervallo;
byte lett_prossima;
int Ind_EE;          //Indirizzo interno EEprom I2c.
int ind=10;
byte vmin;           //Minuti.
byte minu_pre;
byte minu_att;
byte v_sonde=0;
byte abil_invio=0;
byte chip_EE=0x50;   //Indirizzo chip EEprom I2c.
byte Ind_OR=0x51;    //    "     clock calendar PCF8563, PCF8583,   
unsigned long t_prec;
unsigned long t_passo=1000;
//---Prototipi delle funzioni---------------------------------------------------
float GetTemp(OneWire *,byte *);  //Funzione rilevamento temperatura.
void PrintAddress(byte *);        //Stampa indirizzo sonde.
void lookUpSensors();             //Ricerca di tutte le sonde collegate. 
int CheckSensor(byte *);          //Controlla indirizzi.  
LiquidCrystal_I2C lcd(0x38,20,4); // set the LCD address to 0x20 for a 16 chars and 2 line display
//---Predisposizione------------------------------------------------------
void setup(){
  Serial.begin(57600);
    lcd.init();
    lcd.clear();            //Pulisce lo schermo.
    vmin=EsaDec(I2c_Legge_1B(Ind_OR,0x03)&127); //Orologio minuti.
    lett_prossima=vmin+intervallo;
    if(lett_prossima>59){lett_prossima-=60;}
    pinMode(LED1,OUTPUT),
    G_Devices=0;     //Imposta a 0 il numero di sensori attualmente riconosciuti.
    lookUpSensors(); //Avvia la ricerca delle sonde.
    //EEPROM.write(0,0);
    //delay(20);
    //EEPROM.write(1,10);
    //delay(20);
    Ind_EE=EEPROM.read(0)*256;
    Ind_EE=EEPROM.read(1)+Ind_EE;
    intervallo=EEPROM.read(2);
    delay(10);
    digitalWrite(LED1,HIGH);
    t_prec=millis();
}
//---Ciclo principale-----------------------------------------------------
void loop(){
  if(Serial.available()>0){       //Se ci sono caratteri in arrivo.
    ricevuto=Serial.read();       //Legge un byte dalla seriale.
    delay(1);
    ultimo=(char) ricevuto;     //Ultimo carattere ricevuto.
    if(ric_piu==1){               //Ricezioni più di un byte. 
      if(primo=='#'){             //Modifica Clock/Calendar.  
        ricevuto-=48;             //Converte in decimale.
        orario[n_ric]=ricevuto;   //Orario.
        n_ric++;
      }
      if(primo=='*'){             //Modifica intervallo letture.
        ricevuto-=48;
        if(n_ric<2){
          interv[n_ric]=ricevuto; //Array con numero di 2 cifre = intervallo letture.
          n_ric++;
        }
      }
    }
    if(ricevuto=='#'){ //Modifica Clock/Calendar. 
        primo='#';
        abil_vis=0;    //Disabilita visualizzazione.
        ric_piu=1;     //Abilita ricezione dal secondo carattere.
        n_ric=0;       //Azzera variabile numero caratteri ricevuti.
    }
    if(ricevuto=='*'){ //Modifica intervallo letture.
      primo='*';
      abil_vis=0;
      ric_piu=1;
      n_ric=0;         //Azzera variabile numero caratteri ricevuti.
    }
  } //Fine Serial.available()>0
  if(primo=='#'&&ultimo=='/'){ //Aggiorna Clock Calendar.
    primo=' ';
    n_ric=0;
    ric_piu=0;                 //Fine ciclo ricezione.
    Aggiorna_Oro();
    abil_vis=1;                //Riabbilita visualizzazione orario.
  } 
  if(primo=='*'&&ultimo=='/'){ //Modifica intervallo letture.
    primo=' ';
    n_ric=0;
    byte decine=interv[0];
    byte unita=interv[1];
    intervallo=decine*10+unita;
    lcd.setCursor(6,1);
    lcd.print("Lett:");
    lcd.print(intervallo);
    lcd.print("min");  
    lcd.setCursor(0,2);
    lcd.print(decine);
    lcd.print(unita);
    if(intervallo>99){intervallo=99;}
    EEPROM.write(2,intervallo);
    delay(6);
    abil_vis=1;
  }
  if(ricevuto=='v'){   //Visualizza alcuni messaggi.
    ricevuto=' ';
    abil_vis=0;
    Vis_messaggi();
    abil_vis=1;
  }  
  if(ricevuto=='@'){ //Invio al terminale il contenuto della EEprom I2c.
    ricevuto=' ';
    abil_vis=0;
    Invio_term(); 
    abil_vis=1;
  }
  if(ricevuto=='%'){ //Invio al terminale intervallo letture.
    ricevuto=' ';
    abil_vis=0;
    intervallo=EEPROM.read(2);
    Serial.println(intervallo);
    abil_vis=1;
  } 
  if(ricevuto=='?'){ //Lettura EEprom I2C e vis. tipo tabella.
    ricevuto=' ';
    LeggeEE();
    abil_vis=1;
  }
  if(abil_vis==1){       //Ciclico.
    if(millis()>t_prec+t_passo){
      t_prec=millis();
      VisualizzaLCD_Orario(); //Visualizza data e orario.
      minu_att=EsaDec(I2c_Legge_1B(Ind_OR,0x03)&127); //Minuti attuali. 
      if(minu_att!=minu_pre){
        if(minu_att>=lett_prossima){  //Legge minuti. Abil lettura.
          for(int num=0;num<G_Devices;num++){
            temperatura= GetTemp(&G_addr[num][0]); //Legge temperatura.
            ScriveEE(temperatura);  //
            lcd.setCursor(0,1);
            lcd.print(temperatura);
          }
          minu_pre=minu_att;
          lett_prossima=minu_att+intervallo;
          if(lett_prossima>59){
            lett_prossima-=60;
          }
        }
      }  
    }
  }  
}
//---Invio EEprom I2c al terminale---------------------------------------------
void Invio_term(void){
  byte v1;
  float v2=0;
  int ind;
  byte campo=0;
  for(ind=10;ind<Ind_EE;ind++){
    v1=I2c_Legge_2B(chip_EE,ind);
    switch(campo){
      case 0:  //Sonda
        if(v1<10){Serial.print("0");}
        Serial.println(v1);        
        break;
      case 1:  //Ore
        if(v1<10){Serial.print("0");}
        Serial.println(v1);        
        break;  
      case 2:  //Minuti 
        if(v1<10){Serial.print("0");}
        Serial.println(v1);        
        break;
      case 3:  //Giorno
        if(v1<10){Serial.print("0");}
        Serial.println(v1);        
        break;  
      case 4:   //Mese.
        if(v1<10){Serial.print("0");}
        Serial.println(v1);
        break;
      case 5:  //Anno.
        Serial.println(v1);
        break;  
      case 6:   //Temperatura intero.
        v2=float(v1)*100;
        break;
      case 7:   //Temperatura decimale.
        v2=v2+float(v1);
        v2=v2/100;
        Serial.println(v2);
        break;
      default:
        break;   
    }
    campo++;
    if(campo>7){campo=0;}
  }
  Serial.println('/'); //Fine trasmissione.
  abil_vis=1;
}  
//---Scrive su EEprom I2C la temperatura rilevata-----------------------------
void ScriveEE(float temp_f){
  temp_f*=100;                     //Sposta la virgola oltre i decimali.        
  word temp=(word)temp_f;          //Converte float in word.
  byte temp_hi=temp/100;           //Gradi.
  byte temp_lo=temp-temp_hi*100;   //Decimali.
  byte Ind_hi=EEPROM.read(0);      //Indirizzo attuale, byte alto.
  byte Ind_lo=EEPROM.read(1);      //    "        "       "  basso. 
  Ind_EE=Ind_hi*256+Ind_lo;        //Indirizzo attuale.
  if(Ind_EE>4095){Ind_EE=10;}       //Controllo indirizzo massimo (512)
  I2c_Scrive_2B(chip_EE,Ind_EE++,65);            //Slave A.
  delay(20);                                     //Tempo scrittura.
  I2c_Scrive_2B(chip_EE,Ind_EE++,EsaDec(I2c_Legge_1B(Ind_OR,0x04)&63)); //Scrive ore su EEprom I2c.
  delay(20);
  I2c_Scrive_2B(chip_EE,Ind_EE++,EsaDec(I2c_Legge_1B(Ind_OR,0x03)&127)); //Scrive minuti su EEprom I2c.
  delay(20);
  I2c_Scrive_2B(chip_EE,Ind_EE++,EsaDec(I2c_Legge_1B(Ind_OR,0x05)&63)); //Scrive giorno su EEprom I2c.
  delay(20);
  I2c_Scrive_2B(chip_EE,Ind_EE++,EsaDec(I2c_Legge_1B(Ind_OR,0x07)&31)); //Scrive mese su EEprom I2c.
  delay(20);
  I2c_Scrive_2B(chip_EE,Ind_EE++,EsaDec(I2c_Legge_1B(Ind_OR,0x08)));    //Scrive anno su EEprom I2c.
  delay(20);
  I2c_Scrive_2B(chip_EE,Ind_EE++,temp_hi);       //Scrive byte alto temp.
  delay(20);
  I2c_Scrive_2B(chip_EE,Ind_EE++,temp_lo);       //Scrive byte alto temp.
  delay(20);
  Ind_hi=Ind_EE/256;
  Ind_lo=Ind_EE-Ind_hi*256;
  EEPROM.write(0,Ind_hi);
  delay(6);
  EEPROM.write(1,Ind_lo);
  delay(6);
}
//---Legge da EEprom I2C la temperaura----------------------------------------
void LeggeEE(void){
  int i=0;
  int ind=10;
  Serial.println("---------------Lettura EEprom------------------");
  byte v1;
  for(ind=10;ind<Ind_EE;ind++){
    switch(i){
      case 0: //Slave.
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1==65)Serial.print("A ");
        break;
      case 1: //Ora.
        Serial.print("Ore: ");
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1<10){Serial.print('0');}
        Serial.print(v1);
        Serial.print(':');
        break;
      case 2: //Minuti.
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1<10){Serial.print('0');}
        Serial.print(v1);
        Serial.print(' ');
        break;
      case 3: //Giorno.
        Serial.print("Giorno: ");
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1<10){Serial.print('0');}
        Serial.print(v1);
        Serial.print('-');
        break;
      case 4: //Mese.
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1<10){Serial.print('0');}
        Serial.print(v1);
        Serial.print('-');
        break;
      case 5: //Anno.
        v1=I2c_Legge_2B(chip_EE,ind);
        Serial.print(v1);
        Serial.print(" T: ");
        break;
      case 6: //Temperatura (intero).
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1<10){Serial.print('0');}
        Serial.print(v1);
        Serial.print('.');
        break;
      case 7: //Temperatura (decimale).
        v1=I2c_Legge_2B(chip_EE,ind);
        if(v1<10){Serial.print('0');}
        Serial.print(v1);
        break;  
    }  
    i++;
    if(i>7){
      i=0;
      Serial.println();
    }  
  }
  Serial.println();
  Serial.println("-----------Fine lettura EEprom------------------");
  Serial.println();
  Serial.println("Indirizzi EEprom I2c da 10 a 4095: ");
  Serial.print("Indice attuale: ");
  Serial.println(Ind_EE);
} 
//---Ricerca sonde inserite-----------------------------------------------------
void lookUpSensors(){
  byte address[8];          //Indirizzo locale dei sensori
//  Serial.print("--Ricerca avviata--");
  while (ow.search(address)){ //loop finchè trova nuovi dispositivi
    //Se il primo byte è 0x10, si tratta di una sonda DS18S20.
    //"   "   "     "    0x28        "            "   DS18B20.
    if(address[0]==0x10||address[0]==0x28){
      if(CheckSensor(address)==1){  //crc ok
        if(v_sonde==1){
          v_sonde=0;
          Serial.println("");
          if(address[0]==0x10){
            Serial.print(num);
            Serial.print(") ");
            Serial.print("Sonsa DS18S20 : "); 
          }else if(address[0] == 0x28){
            Serial.print(num);
            Serial.print(") ");
            Serial.print("Sonda DS18B20 : ");
          }
          PrintAddress(address);     //Numero indirizzo 
        }else{
          for(int aa=0;aa<8;aa++) G_addr[G_Devices][aa]=address[aa]; 
          G_Devices++; //Numero dei termometri memorizzati.
        }
      }
    }
    num++;
  }
}
//---Lettura termometri---------------------------------------
float GetTemp(byte * addr){
  byte present = 0;
  byte data[12];
  int i;
  byte address[8];
  for(i=0;i<8;i++) address[i]=*(addr+i); //copia l'indirizzo nella stringa locale.
  ow.reset();
  ow.select(addr);
  ow.write(0x44,1); //start conversion, with parasite power on at the end.
  delay(750);       //maybe 750ms is enough, maybe not
  //we might do a ds.depower() here, but the reset will take care of it.
  ow.depower();
  present = ow.reset();
  ow.select(addr);
  ow.write(0xBE); // Read Scratchpad
  for(i=0;i<9;i++) data[i] = ow.read(); //we need 9 bytes
  int HighByte, LowByte, TReading, SignBit, Tc_100, Whole, Fract;
  double result;
  LowByte = data[0];
  HighByte = data[1];
  TReading = (HighByte << 8) + LowByte;
  SignBit = TReading & 0x8000; // test most sig bit
  if(SignBit) TReading=(TReading ^ 0xffff) + 1; // 2's comp //negative
  Tc_100=(6*TReading)+TReading/4; //multiply by (100 * 0.0625) or 6.25
  Whole=Tc_100/100; //separate off the whole and fractional portions
  Fract=Tc_100%100;
  result=Whole;
  result+=((double)Fract/100);
  if(SignBit)result*=-1;
    return result;
}
//---Stampa indirizzo sul monitor -----------------------------------
void PrintAddress(byte * address){
  for(byte i=0;i<8;i++){
    if(address[i]<9)Serial.print("0");
      Serial.print(address[i],HEX);
      if(i<7)Serial.print("-");
  }
}
//---Controlla indirizzo---------------------------------------------
int CheckSensor(byte * address){
  if(OneWire::crc8(address,7)!=*(address+7))return(-1);//
    //faccio il controllo del CRC8, se fallito ritorno -1
  else return(1); // cr8 OK, ritorno 1
}
//---Visualizza Orario-------------------------------------------------
void VisualizzaLCD_Orario(void){
  lcd.setCursor(0,0);            //Posiziona il cursore a Home.  
  lcd.print("D ");
  byte ore=EsaDec(I2c_Legge_1B(Ind_OR,0x04)&63);
  if(ore<10){ //Se ore è inferiore a 10 aggiunge uno 0.
    lcd.print("0");              
    lcd.print(ore); //Visualizza le ore su LCD alfanumerico.
  }else{
    lcd.print(ore); //Visualizza le ore su LCD alfanumerico.
  }
  lcd.print(":");
  byte minuti=EsaDec(I2c_Legge_1B(Ind_OR,0x03)&127);
  if(minuti<10){                  
    lcd.print("0");
    lcd.print(minuti);
  }else{
    lcd.print(minuti);
  }
  lcd.print(".");
  byte secondi=EsaDec(I2c_Legge_1B(Ind_OR,0x02)&127);
  if(secondi<10){ //Se secondi è inferiore a 10 aggiunge uno 0.
    lcd.print("0");
    lcd.print(secondi);
  }else{
    lcd.print(secondi);
  }
  lcd.print(" ");
  byte giorno=EsaDec(I2c_Legge_1B(Ind_OR,0x05)&63);
  if(giorno<10){
    lcd.print("0");
    lcd.print(giorno);
  }else{
    lcd.print(giorno);
  }
  lcd.print("-");
  byte mese=EsaDec(I2c_Legge_1B(Ind_OR,0x07)&31);
  if(mese<10){                   
    lcd.print("0");
    lcd.print(mese);
  }else{
    lcd.print(mese);
  }
}
//---Aggiorna Orologio-------------------------------------------------
void Aggiorna_Oro(void){
  byte minuti,ore,secondi,giorno,mese;
  word anno;
  ore    =orario[0]*10+orario[1]; //Estrae dall'array le ore.
  minuti =orario[2]*10+orario[3];
  secondi=orario[4]*10+orario[5];
  giorno =orario[6]*10+orario[7];
  mese   =orario[8]*10+orario[9];
  anno   =orario[10]*10+orario[11];
  //anno   =orario[10]*1000+orario[11]*100+orario[12]*10+orario[13];
  I2c_Scrive_1B(Ind_OR,0x04,DecEsa(ore)); //Imposta ora.
  I2c_Scrive_1B(Ind_OR,0x03,DecEsa(minuti)); //Imposta minuti.
  I2c_Scrive_1B(Ind_OR,0x02,DecEsa(secondi)); //Imposta secondi.
  I2c_Scrive_1B(Ind_OR,0x05,DecEsa(giorno)); //Imposta giorno.
  I2c_Scrive_1B(Ind_OR,0x07,DecEsa(mese)); //Imposta mese.
  I2c_Scrive_1B(Ind_OR,0x08,DecEsa(anno)); //Imposta anno.
}  
//---Vusualizza stringhe-----------------------------------------------
void Vis_stringhe(char *prog){
  while(*prog!='\0'){Serial.print(*prog++);}
}
//---Visualizzazione mesaggi--------------------------------------------------
void Vis_messaggi(void){
  Vis_stringhe(Sketch);   //Visualizza sul Serial Monitor il nome dello sketch.
  Serial.println();
  byte ore=EsaDec(I2c_Legge_1B(Ind_OR,0x04)&63);
  Serial.print(" Ore:");
  if(ore<10){ //Se ore è inferiore a 10 aggiunge uno 0.
    Serial.print("0");              
    Serial.print(ore); //Visualizza le ore su LCD alfanumerico.
  }else{
    Serial.print(ore); //Visualizza le ore su LCD alfanumerico.
  }
  Serial.print(":");
  byte minuti=EsaDec(I2c_Legge_1B(Ind_OR,0x03)&127);
  if(minuti<10){                  
    Serial.print("0");
    Serial.print(minuti);
  }else{
    Serial.print(minuti);
  }
  Serial.print(":");
  byte secondi=EsaDec(I2c_Legge_1B(Ind_OR,0x02)&127);
  if(secondi<10){ //Se secondi è inferiore a 10 aggiunge uno 0.
    Serial.print("0");
    Serial.println(secondi);
  }else{
    Serial.println(secondi);
  }
  Serial.print("Data:");
  byte giorno=EsaDec(I2c_Legge_1B(Ind_OR,0x05)&63);
  if(giorno<10){
    Serial.print("0");
    Serial.print(giorno);
  }else{
    Serial.print(giorno);
  }
  Serial.print("-");
  byte mese=EsaDec(I2c_Legge_1B(Ind_OR,0x07)&31);
  if(mese<10){                   
    Serial.print("0");
    Serial.print(mese);
  }else{
    Serial.print(mese);
  }
  Serial.print("-");
  byte anno=EsaDec(I2c_Legge_1B(Ind_OR,0x08)&31);
  Serial.println(anno);
  Serial.print("Intervallo letture ogni: ");
  Serial.print(intervallo);
  Serial.println(" minuti");
  Serial.print("Ind_EE: ");
  Serial.println(Ind_EE);
}  

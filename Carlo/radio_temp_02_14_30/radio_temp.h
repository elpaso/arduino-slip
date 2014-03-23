Funzioni:
  /*.......Imposta il Clock Calendar.................................
  
  Descrizione
  
  RTC.stopClock();         //Arresta il Clock Calendar.
  RTC.fillByYMD(2013,5,1); //Imposta anno, mese  , giorno.
  RTC.fillByHMS(14,15,0);  //   "    ore , minuti, secondi.
  RTC.setTime();           //Inserisce i parametri impostati.  
  .......Avvia il Clock Calendar...................................
  RTC.startClock();        //Avvio. In setup().
  .......Lettura Clock Calendar....................................
  RTC-getTime();           //Legge il Clock Calendar.
  RTC.hour;                //Restituisce le ore.
  RTC.minute;              //     "        minuti.
  RTC.second;              //     "        secondi.
  RTC.day;                 //     "        giorno.
  RTC.month;               //     "        mese.
  RTC.year;                //     "        anno.
  RTC.dow;                 //     "        giorno della settimana.
  .......Impostazione onda quadra in uscita sul pin 7..............
  RTC.ctrl=0x00;           //SQW/OUT pin 7 disabilitato.
           0x10;           //   "          Onda quadra      1 Hz. 
           0x11;           //   "            "     "     4096 Hz.
           0x12;           //   "            "     "     8192 Hz.
           0x13;           //   "            "     "    32768 Hz.
  RTC.setCTRL();           //Inserisce impostazioni.
  
*/  

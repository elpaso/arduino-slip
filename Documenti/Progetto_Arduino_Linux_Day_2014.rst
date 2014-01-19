========================================
Progetto Slip Arduino per Linux Day 2014
========================================

------------
Introduzione
------------

Si propone di realizzare un sistema di automazione remota (sensori e relè) wireless (nRF24) gestito dagli Arduino o Atiny e da un pc con interfaccia in PyQT

---------------------
Requisiti del sistema
---------------------

1. Il sistema è composto da un PC che ha la funzione di archiviare i dati e gestire il sistema di automazione tramite un'interfaccia grafica

	1.1 L'interfaccia grafica ha le funzioni di uno SCADA
	
	1.2 L'interfaccia grafica è sviluppata in Python 2.7
	
	1.3 
	
2. Un Arduino con modulo nRF24 è collegato al PC tramite la porta USB

	2.1 Questo Arduino si occupa di dialogare con il PC e funge da Server

		2.1.1 Riceve i comandi dal PC

		2.1.2 Comunica con gli altri moduli slave tramite la connessione a 2.4 GHz

		2.1.3 

3. Le unità slave sono degli Arduino o Atiny 

	3.1 Sono dotate di connessione a 2.4 GHz tramite nRF24

	3.2 Sono collegati dei sensori

		3.2.1 DHT11 Temperatura e Umidità

		3.2.2 DS18S20 Temperatura

	3.3 Sono collegati dei relay

		3.3.1 A 24 Volt

		3.3.2 A 220 Volt AC

	3.4 Hanno un RTC per avere un orologio

	3.5 Sono datate di eeprom 24FC1025 da 1Mbit per immagazzinare i dati salvati

	3.6 Alimentazione a batteria da 9V e regolatore di tensione 5V e 3.3V

		



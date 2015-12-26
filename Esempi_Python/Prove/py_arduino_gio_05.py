#!/usr/bin/env python
# py_arduino_gio_05.py

import sys
from PyQt4 import QtGui, QtCore, uic
import serial
import time

lista=	[['Sonda','Ore','Min','Gio','Mese','Anno','Tem','p'], #Colonne tabella.
		 [50,35,35,35,45,45,35,30]]                 #Larghezza colonne.

#---Form Principale----------------------------------------------------
class Principale(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_feb_A_01.ui', self) #Carica form.
		#Posizione e dimensione della finestra.
		self.ui.setGeometry(50, 50, 600, 600)#pos O,V dim O,V
		self.connect(self.ui.pFine, QtCore.SIGNAL("clicked()"),
			fine_sessione)
		self.connect(self.ui.pApre_p, QtCore.SIGNAL("clicked()"),
			Apre_param)
		self.connect(self.ui.pLegge_EE, QtCore.SIGNAL("clicked()"),
			Legge_Arduino)		
		self.timer=QtCore.QTimer()
		self.tabella.setRowCount(500)     #Numero righe
		self.tabella.setColumnCount(8)    #Numero colonne
		self.tabella.setHorizontalHeaderLabels([lista[0][0],
			lista[0][1],lista[0][2],lista[0][3],lista[0][4],
			lista[0][5],lista[0][6],lista[0][7]]) #Intestazione colonne.
			
		for i, va in enumerate(lista[0]):
			self.tabella.setColumnWidth(i,lista[1][i]) #Largh. col
			#valore=lista[0][i]
		self.pLegge_EE.BackgroundColor = 5,12,122	
#---Form Parametri-----------------------------------------------------
class Parametri(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_feb_B_01.ui', self) #Carica form.
		#Posizione e dimensioni della finestra.
		self.ui.setGeometry(130, 60, 250, 300) #pos O,V dim O,V
		self.connect(self.ui.pOK_2, QtCore.SIGNAL("clicked()"),
		Chiude_param)
#---Form Terminale-----------------------------------------------------
class Terminale_Ser(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_terminal_00.ui', self) #Carica form.


#---Legge da Arduino-----------------------------------------
def Legge_Arduino():
	window_a.ui.messaggi.setText("Ricezione in corso")
	app.processEvents()
	window_a.ui.update

	conn.write("L")	 #Richiesta dati dalla seriale 
	time.sleep(0.5)
	
	i=0
	dati_arduino=[]
	while 1:
		try:
			linea=conn.readline() #Lettura linea
			if len(linea) != 0:
				if linea[0] == "D":
					window_c.ui.textEdit.append(linea)
					app.processEvents()
					linea_ok=list(linea.rstrip())
					dati_arduino.append(linea_ok)
					i=i+1
				if linea[0] == "E":
					break
		
		except serial.serialutil.SerialException:
		 	print "Errore di comunicazione"
		 	break
	
	window_a.ui.messaggi.setText("Ricezione terminata")
	app.processEvents()
	
	len_da_ar=len(dati_arduino)
	
	for riga in range (0,len_da_ar):
		dato_str=''.join(dati_arduino[riga])
		dati_dato_str=dato_str.split(';')
		
		for col in range(0,7):
			dato_col=dati_dato_str[col]
			window_a.tabella.setItem(riga,col,QtGui.QTableWidgetItem(dato_col))
			
#---Chiude il form dei parametri---------------------------------------
def Chiude_param():
	window_b.hide()
	window_a.ui.imPorta.setText(window_b.ui.n_porta.currentText()+','+
		window_b.ui.v_porta.currentText())
	window_a.show()
	window_a.ui.pLegge_EE.show()
	window_a.ui.messaggi.show()
	# Apre connesione seriale con Arduino
	global conn
	try:
		A_ser_port=str(window_b.ui.n_porta.currentText())
		A_ser_vel=int(str(window_b.ui.v_porta.currentText()))
		conn=serial.Serial(A_ser_port, A_ser_vel,timeout=0.5)
	except serial.serialutil.SerialException:
		print "Controllare le connessioni con Arduino"
		window_c.ui.textEdit.append("Controllare le connessioni con Arduino")
	for i in range(1,2):
		linea=conn.readline()
#---Apre il form dei parametri-----------------------------------------
def Apre_param():
	window_b.ui.show()
	window_b.ui.n_porta.addItem("/dev/ttyACM0")
	window_b.ui.n_porta.addItem("/dev/ttyACM1")
	window_b.ui.n_porta.addItem("/dev/ttyUSB0")
	window_b.ui.n_porta.addItem("/dev/ttyUSB1")
	window_b.ui.v_porta.addItem("9600")
	window_b.ui.v_porta.addItem("19200")
	window_b.ui.v_porta.addItem("38400")
	window_b.ui.v_porta.addItem("57600")
	window_b.ui.v_porta.addItem("115200")
#---Fine lavoro, chiude tutto------------------------------------------
def fine_sessione():
	conn.close()
	quit()
#---Funzione principale------------------------------------------------
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window_a = Principale()
	window_b = Parametri()
	window_c = Terminale_Ser()
	window_a.ui.pLegge_EE.hide()
	window_a.ui.messaggi.hide()
	window_a.show()
	window_c.show()
	sys.exit(app.exec_())

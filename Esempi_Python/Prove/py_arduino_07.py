#!/usr/bin/env python
# py_arduino_07.py
# 08-01-2014
# netbeans
# Carica lo schema della tabella all' avvio.
# Imposta i parametri della porta.
# gps
# Larghezza colonne OK.
# Importa le librerie necessarie.
import sys
from PyQt4 import QtGui, QtCore, uic
import serial
global arduino
lista=	[['Sonda','Data','Ora','Temp'], #Colonne tabella.
		 [50,70,70,50]]                 #Larghezza colonne.
dati=[['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9'],   #Sonda
	  ['01-01-14','02-01-14','03-01-14','04-01-14','05-01-14', #Data
	   '06-01-14','07-01-14','08-01-15','09-01-14','10-01-14'],
	  ['08,30','08,30','10,30','12,30','15,30', #Ora
	   '07,30','09,30','12,10','15,25','18,30'], 
	  ['19,35','20,10','21,65','22,10','22,35', #Temperatura
	   '18,12','19,26','22,25','20,12','25,10']]
#---Form Principale----------------------------------------------------
class Principale(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_02a.ui', self) #Carica form.
		#self.ui.show()
		#Assegnazione eventi->azioni
		self.connect(self.ui.pFine, QtCore.SIGNAL("clicked()"),
			fine_sessione)
		self.connect(self.ui.pApre_p, QtCore.SIGNAL("clicked()"),
			Apre_param)
		self.connect(self.ui.pCarica, QtCore.SIGNAL("clicked()"),
			carica_tabella)	
		self.connect(self.ui.pAp_Porta, QtCore.SIGNAL("clicked()"),
			apertura_porta)	
		self.timer=QtCore.QTimer()
		self.tabella.setRowCount(15)      #Numero righe
		self.tabella.setColumnCount(4)    #Numero colonne
		self.tabella.setHorizontalHeaderLabels([lista[0][0],
			lista[0][1],lista[0][2],lista[0][3]]) #Intestazione colonne.
		for i, va in enumerate(lista[0]):
			self.tabella.setColumnWidth(i,lista[1][i]) #Largh. col
			valore=lista[0][i]
#---Form Parametri-----------------------------------------------------
class Parametri(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_02b.ui', self) #Carica form.
		#self.ui.show()
		#Assegnazione eventi->azioni
		self.connect(self.ui.pOK_2, QtCore.SIGNAL("clicked()"),
			Chiude_param)
#---Lettura EEprom dell' Arduino---------------------------------------
def carica_tabella():
	for i, va in enumerate(dati[0]):	
		valore = QtGui.QLineEdit(dati[0][i])
		window_a.tabella.setItem(i,0,QtGui.QTableWidgetItem #Sonda.
			(valore.text()))
		valore = QtGui.QLineEdit(dati[1][i])
		window_a.tabella.setItem(i,1,QtGui.QTableWidgetItem #Data.
			(valore.text()))
		valore = QtGui.QLineEdit(dati[2][i])
		window_a.tabella.setItem(i,2,QtGui.QTableWidgetItem #Ora.
			(valore.text()))
		valore = QtGui.QLineEdit(dati[3][i])
		window_a.tabella.setItem(i,3,QtGui.QTableWidgetItem #Temperatura
		(valore.text()))
#---Chiude il form dei parametri---------------------------------------
def Chiude_param():
	window_b.hide()
	window_a.ui.imPorta.setText(window_b.ui.n_porta.currentText()+','+
		window_b.ui.v_porta.currentText())
	window_a.show()
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
	#window_b.show()

#Apertura porta seriale
def apertura_porta():
	print window_a.ui.imPorta.text() 
	print
	print
	A_ser_port=str(window_b.ui.n_porta.currentText())
	A_ser_vel=int(str(window_b.ui.v_porta.currentText()))
	#A_ser_vel=9600
	print A_ser_port
	print A_ser_vel
	
	
	arduino=serial.Serial(A_ser_port, A_ser_vel)

	#arduino=serial.Serial("/dev/ttyACM0",9600)  #OK

#---Fine lavoro, chiude tutto------------------------------------------
def fine_sessione():
	quit()
#---Funzione principale------------------------------------------------
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window_a = Principale()
	window_b = Parametri()
	window_a.ui.show()
	sys.exit(app.exec_())

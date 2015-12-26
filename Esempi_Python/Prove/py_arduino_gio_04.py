#!/usr/bin/env python
# py_arduino_feb_03.py
# 02-02-2014
#
# Carica lo schema della tabella all' avvio.
# Imposta i parametri della porta.
# 
# Larghezza colonne OK.
# Importa le librerie necessarie.
import sys
from PyQt4 import QtGui, QtCore, uic
import serial
import time

lista=	[['Sonda','Ore','Min','Gio','Mese','Anno','Tem','p'], #Colonne tabella.
		 [50,35,35,35,45,45,35,30]]                 #Larghezza colonne.
dati=[[],[],[],[],[],[],[],[]]
dato=[]
#---Form Principale----------------------------------------------------
class Principale(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_feb_A_01.ui', self) #Carica form.
		#Posizione e dimensione della finestra.
		self.ui.setGeometry(150, 200, 500, 530) #pos O,V dim O,V
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
			valore=lista[0][i]
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
		#Posizione e dimensioni della finestra.
		#self.ui.setGeometry(130, 60, 250, 300) #pos O,V dim O,V
		#self.connect(self.ui.pOK_2, QtCore.SIGNAL("clicked()"), Chiude_param)
#---Legge la EEprom di Arduino-----------------------------------------
def Legge_EE():
	window_a.ui.messaggi.setText("Ricezione in corso")
	window_a.update
	#global conn
	try:
		A_ser_port=str(window_b.ui.n_porta.currentText())
		A_ser_vel=int(str(window_b.ui.v_porta.currentText()))
		conn=serial.Serial(A_ser_port, A_ser_vel,timeout=1)
		conn.flushInput() #Svuota il buffer della seriale ?.
		                                  
	except:
		print "Controllare le connessioni con Arduino"
	
	while True:
		try:
			conn.write('L')	 #Richiesta dati dalla seriale 	
			linea=conn.read(2).rstrip() #Lettura 2 byte senza spazi.
			if linea=="/":  #Fine ricezione.
				conn.flushInput() #Svuota il buffer della seriale ?.
				print "Fine ricezione"
				window_a.ui.messaggi.setText("Ricezione terminata")
				riga=0
				col=0
				i=0
				for i in range(0,2000):
					elem=dato[i]
					#print "i:",i,"Col:",col," Riga:",riga," Eleme:",elem	
					window_a.tabella.setItem(riga,col,QtGui.QTableWidgetItem(elem))
					col+=1
					if col>7:
						col=0
						riga=riga+1
				break	
			print linea
			dato.append(linea)
		except:
		 	print "Errore di comunicazione"
			break

#---Legge da Arduino-----------------------------------------
def Legge_Arduino():
	window_a.ui.messaggi.setText("Ricezione in corso")
	app.processEvents()
	window_a.ui.update
	#time.sleep(1)
	#conn.flushInput() #Svuota il buffer della seriale ?.
	#conn.flushOutput()
	#print linea
	#sleep(2)
	#conn.readline()
	#print conn.isOpen()
	#conn.flushInput()
	conn.write("L")	 #Richiesta dati dalla seriale 
	time.sleep(0.5)
	#print conn.inWaiting()
	i=0
	dati_arduino=[]
	while 1:
		try:
			#conn.write("")	
			linea=conn.readline() #Lettura 2 byte senza spazi.
			#linea=conn.read(5)
			#print conn.inWaiting()
			if len(linea) != 0:
				if linea[0] == "D":
				#print i
					print linea
					window_c.ui.textEdit.append(linea)
					app.processEvents()
					linea_ok=list(linea.rstrip())
					dati_arduino.append(linea_ok)
					
					#print (linea.split(';'))
					i=i+1
				if linea[0] == "E":
					break
		
		except:
		 	print "Errore di comunicazione"
	#conn.flushInput() #Svuota il buffer della seriale ?.
	#conn.flushOutput()
	
	
	#print "Fine ricezione"
	window_a.ui.messaggi.setText("Ricezione terminata")
	app.processEvents()
	#print len(dati_arduino)
	#print ''.join(dati_arduino[1])
	len_da_ar=len(dati_arduino)
	
	for riga in range (0,len_da_ar):
		dato_str=''.join(dati_arduino[riga])
		dati_dato_str=dato_str.split(';')
		#print dati_dato_str
		for col in range(0,7):
			dato_col=dati_dato_str[col]
			#print dato_col
			#window_a.tabella.setItem(riga,col,QtGui.QTableWidgetItem(dati_arduino[riga] [col+1]))
			window_a.tabella.setItem(riga,col,QtGui.QTableWidgetItem(dato_col))
			
	#
#---Chiude il form dei parametri---------------------------------------
def Chiude_param():
	window_b.hide()
	window_a.ui.imPorta.setText(window_b.ui.n_porta.currentText()+','+
		window_b.ui.v_porta.currentText())
	window_a.show()
	window_a.ui.pLegge_EE.show()
	window_a.ui.messaggi.show()
	global conn
	try:
		A_ser_port=str(window_b.ui.n_porta.currentText())
		A_ser_vel=int(str(window_b.ui.v_porta.currentText()))
		conn=serial.Serial(A_ser_port, A_ser_vel,timeout=0.5)
		#conn.flushInput() #Svuota il buffer della seriale ?.
		#print conn.isOpen()
	except:
		print "Controllare le connessioni con Arduino"
	for i in range(1,5):
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

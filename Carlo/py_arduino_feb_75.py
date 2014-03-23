#!/usr/bin/env python
# py_arduino_feb_74.py
# 21-03-2014



# Importa le librerie necessarie.
import sys
from PyQt4 import QtGui, QtCore, uic
import numpy as np 
import serial
import datetime
import sqlite3
import os

miadir=os.getenv("HOME")
nome_db=miadir+"/dati_db/py_arduino_temp.db" #Nome del database
lista=	[['Sonda','Ore','Data','Temp'], 
		 [50,50,70,45]]                 #Larghezza colonne.
dati=[]
elem=0
aStampa=[]
orologio=0
	 
#---Form Principale----------------------------------------------------
class Principale(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_feb_A_13.ui', self) #Carica form
		#Posizione e dimensione della finestra.
		self.ui.setGeometry(120, 120, 650, 600) #pos O,V dim O,V
		self.connect(self.ui.pFine, QtCore.SIGNAL("clicked()"),
			fine_sessione)
		self.connect(self.ui.pApre_p, QtCore.SIGNAL("clicked()"),
			Apre_param)
		self.connect(self.ui.pLegge_EE, QtCore.SIGNAL("clicked()"),
			Legge_EE)
		self.connect(self.ui.p_S_freq, QtCore.SIGNAL("clicked()"),
			Scrive_freq)
		self.connect(self.ui.p_L_freq, QtCore.SIGNAL("clicked()"),
			Legge_freq)
		self.connect(self.ui.pSeleziona, QtCore.SIGNAL("clicked()"),
			Seleziona)
		self.connect(self.ui.pStampa, QtCore.SIGNAL("clicked()"),
			Stampa)
#---Form Parametri-----------------------------------------------------
class Parametri(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('py_arduino_feb_B_01.ui', self) #Carica form
		#Posizione e dimensioni della finestra.
		self.ui.setGeometry(130, 60, 250, 300) #pos O,V dim O,V
		self.connect(self.ui.pOK_2, QtCore.SIGNAL("clicked()"),
		Chiude_param)
#---Imposta tabella----------------------------------------------------
def Imposta_tabella():
	wa.tabella.setRowCount(10)     #Numero righe
	wa.tabella.setColumnCount(4)   #Numero colonne
	wa.tabella.setHorizontalHeaderLabels([lista[0][0],\
		lista[0][1],lista[0][2],lista[0][3]]) #Intestazione colonne.
	for i, va in enumerate(lista[0]):
		wa.tabella.setColumnWidth(i,lista[1][i]) #Largh. col
		valore=lista[0][i]		
#---Imposta data e ora iniziale----------------------------------------
def Impostazioni_iniziali():
	Imposta_tabella()
	orologio = datetime.datetime.now()
	wa.vSonda_basso.setText('1')     #Sonda.
	wa.vSonda_alto.setText('99')     #Sonda.
	vore=QtCore.QTime.fromString("00:00","hh:mm")
	wa.vOre_basso.setTime(vore)      #Ora inizio.
	vore=QtCore.QTime.fromString("23:59","hh:mm")
	wa.vOre_alto.setTime(vore)       #Ora fine.
	wa.vTemp_basso.setText('01.00')  #Temperatura minima.
	wa.vTemp_alto.setText('30.00')   #Temperatura massima.
	mese=orologio.month
	if mese <10:
		mese='0'+str(mese)
	else:
		mese=str(mese)	
	anno=str(orologio.year-2000)
	vdata=anno+'-'+mese+'-'+"01"
	vdata1=QtCore.QDate.fromString(vdata,"yy-MM-dd")
	wa.ui.vData_basso.setDate(vdata1) #Data inizio. 
	vOggi=QtCore.QDate.currentDate() 
	wa.vData_alto.setDate(vOggi)      #Data fine.
	Seleziona()
#---Seleziona i record-------------------------------------------------
def Seleziona():
	s_min=wa.vSonda_basso.text()
	s_max=wa.vSonda_alto.text()
	o_min=wa.vOre_basso.text()
	o_max=wa.vOre_alto.text()
	d_min=wa.vData_basso.text()
	d_max=wa.vData_alto.text()
	t_min=wa.vTemp_basso.text()
	t_max=wa.vTemp_alto.text()
	vParam='WHERE sonda>="%s" AND sonda<="%s" AND\
				  ore>="%s"   AND ore<="%s" AND\
				  data>="%s"  AND data<="%s" AND\
				  temp>="%s"  AND temp<="%s"\
				  '%(s_min,s_max,o_min,o_max,d_min,d_max,t_min,t_max)              
	Carica_tabella(vParam)
#---Carica il database sulla tabella-----------------------------------
def Carica_tabella(vParam):
	riga=0;col=0;n_rec=0;righe=''	
	if os.path.isfile(nome_db):
		dati_db=sqlite3.connect(nome_db) #Connessione
		cursore=dati_db.cursor() #Cursore
	else:
		wa.ui.Messaggi.append("Database inesistente")
		return
	ordina=wa.cIndici.currentText()	
	i_A_D=wa.cInd_A_D.currentText()
	wa.tabella.clear()               #Svuota la tabella.
	Imposta_tabella()
	cursore.execute('SELECT COUNT(*) FROM temp_log '+vParam) #Conta record.
	conta=cursore.fetchall()
	if i_A_D=='ASC':
		cursore.execute('SELECT * FROM temp_log '+vParam+'ORDER BY "%s"'%(ordina))
	else:
		cursore.execute('SELECT * FROM temp_log '+vParam+'ORDER BY "%s" DESC'%(ordina))
	righe=cursore.fetchall()
	dati_db.commit() #Memorizza database.
	n_rec=conta[0][0]   
	wa.ui.record.setText(str(n_rec)) #Numero record.
	wa.ui.tabella.setRowCount(n_rec) #Numero righe della tabella.
	v_a=1
	ind_a=0
	del aStampa[:]
	for a_t in righe:
		vSonda_a=righe[riga][col]            #Sonda.
		wa.tabella.setItem(riga,col,QtGui.\
			QTableWidgetItem(vSonda_a))
		aStampa.append(str(vSonda_a))        #Array stampa.
		col+=1	
		vOre_a=righe[riga][col]              #Ore. 
		wa.tabella.setItem(riga,col,QtGui.\
			QTableWidgetItem(vOre_a))
		aStampa.append(str(vOre_a))	         #Array stampa.
		col+=1
		vData_a=righe[riga][col]	         #Data.
		wa.tabella.setItem(riga,col,QtGui.
			QTableWidgetItem(vData_a))
		aStampa.append(str(vData_a))	     #Array stampa.
		col+=1
		vTemp_a=righe[riga][col]             #Temperatura.
		wa.tabella.setItem(riga,col,QtGui.
			QTableWidgetItem(vTemp_a))
		aStampa.append(str(vTemp_a))         #Array stampa.
		col=0;riga+=1
		ind=0
		v_a+=1
#---Impota frequenza letture dal microcontrollore---------------------
def Scrive_freq():
	vfreq=' '
	try:
		A_ser_port=str(wb.ui.n_porta.currentText())
		A_ser_vel=int(str(wb.ui.v_porta.currentText()))
		conn=arduino=serial.Serial(A_ser_port, A_ser_vel,timeout=1)
		conn.read();conn.read();
		vfreq='*'+str(wa.ui.l_freq.text())+'/'
		print vfreq
		conn.write(vfreq)
		conn.close() #Chiusura porta.
	except:		
		print "Errore di comnunicazione"
#---Legge frequenza letture dal microcontrollore-----------------------
def Legge_freq():
	freq=0
	try:
		A_ser_port=str(wb.ui.n_porta.currentText())
		A_ser_vel=int(str(wb.ui.v_porta.currentText()))
		conn=arduino=serial.Serial(A_ser_port, A_ser_vel,timeout=1)
		conn.read();conn.read();conn.read();conn.read();conn.read();
		conn.write('%')	 #Richiesta dati dalla seriale
		freq=conn.read(2).rstrip() #rstrip() senza spazi.
		wa.ui.l_freq.setText(freq)
		conn.close() #Chiusura porta.
	except:		
		print "Errore di comnunicazione"	
#---Legge la EEprom di Arduino-----------------------------------------
def Legge_EE():
	a=0
	campi=[]
	print "Inizio lettura EEprom"
	if os.path.isfile(nome_db):
		dati_db=sqlite3.connect(nome_db) #Connessione
		cursore=dati_db.cursor() #Cursore
	else:
		wa.ui.Messaggi.append("Database inesistente")
		return
	try:
		A_ser_port=str(wb.ui.n_porta.currentText())
		A_ser_vel=int(str(wb.ui.v_porta.currentText()))
		conn=arduino=serial.Serial(A_ser_port, A_ser_vel,timeout=1)
		conn.read();conn.read();conn.read() #Svuota il buffer seriale.
		conta=0;a_t=0;col=0;riga=0;linea=0;fine=0;indice=0;record=0
		conn.write('@')	 #Richiesta dati dalla seriale
		wa.ui.Messaggi.append("Ricezione in corso")
		app.processEvents()
		cursore.execute("DELETE FROM temp_log")
		dati_db.commit() 
		del dati[:] #Svuota l'array.
	except serial.serialutil.SerialException:
		wa.ui.Messaggi.append("Controllare le connessioni con Arduino")
		return
	while True:
		try:
			linea=conn.readline().rstrip() #senza spazi.
			print "Lettura linea", a
			a+=1
			if linea=='/':         #Carattere di fine ricezione.
				wa.ui.Messaggi.append("Ricezione terminata")
				fine=1
			else:
				conta+=1           #Numeri ricevuti.
				dati.append(linea) #Carica l'array con i dati ricevuti
			if fine==1:
				record=conta/7     #Numero dei record ricevuti.
				a_t=0	
				indice=0
				for a_t in range(record):
					v_so=dati[indice];indice+=1       #Sonda.
					v_or=dati[indice];indice+=1
					v_or=v_or+':'
					v_or=v_or+dati[indice];indice+=1  #Ore.
					v_gi=dati[indice];indice+=1
					v_me=dati[indice];indice+=1
					v_an=dati[indice];indice+=1
					v_da=v_an+'-'+v_me+'-'+v_gi	      #anno-mese-giorno 
					v_te=dati[indice];indice+=1       
					cursore.execute("INSERT INTO temp_log(sonda,ore,\
					data,temp)VALUES(?,?,?,?)"\
					,(v_so,v_or,v_da,v_te))
				break		
		except:
			print "Errore di comunicazione"
			break
	print "Fine lettura EEprom"		
	dati_db.commit() #Memorizza database.	
	conn.close()     #Chiusura porta.
	cursore.close()  #Chiusura cusore.
	dati_db.close()  #Chiusura database.
	wa.ui.record.setText(str(record))
	Seleziona()
	wa.ui.update()
#---Chiude il form dei parametri---------------------------------------
def Chiude_param():
	wa.ui.imPorta.setText(wb.ui.n_porta.currentText()+','+\
		wb.ui.v_porta.currentText())
	wa.show()
	wa.ui.pLegge_EE.show() #Mostra pulsante, Lettura EEprom. 
	wa.ui.Messaggi.show()  #Mostra il TextEdit messagi.
	wb.hide()              #Nasconde form parametri.
#---Apre il form dei parametri-----------------------------------------
def Apre_param():
	wb.ui.show()
#---Carica l'array porta-----------------------------------------------	
def Carica_array_porta():	
	wb.ui.n_porta.addItem("/dev/ttyACM0")
	wb.ui.n_porta.addItem("/dev/ttyACM1")
	wb.ui.n_porta.addItem("/dev/ttyUSB0")
	wb.ui.n_porta.addItem("/dev/ttyUSB1")
	wb.ui.v_porta.addItem("9600")
	wb.ui.v_porta.addItem("19200")
	wb.ui.v_porta.addItem("38400")
	wb.ui.v_porta.addItem("57600")
	wb.ui.v_porta.addItem("115200")
#---Carica combo box indici--------------------------------------------
def Carica_Indici():
	wa.cIndici.addItem("sonda")
	wa.cIndici.addItem("data")
	wa.cIndici.addItem("ore")
	wa.cIndici.addItem("temp")
	wa.cInd_A_D.addItem('ASC')
	wa.cInd_A_D.addItem('DESC')
#---Prove array--------------------------------------------------------
def Sarray():
	print "Stampa"
	v_rec=len(aStampa)
	for i in range(0,v_rec):
		print aStampa[i]
#---Stampa su file pdf-------------------------------------------------
def Stampa():
	orologio = datetime.datetime.now()
	anno=(orologio.year)-2000
	mese=orologio.month
	giorno=orologio.day
	ora=orologio.hour
	minuti=orologio.minute
	fStampa=str(giorno)+'-'+str(mese)+'-'+\
	      str(anno)+' '+str(ora)+':'+str(minuti)
	wa.ui.Messaggi.append("Creazione file .pdf in corso")
	doc=QtGui.QTextDocument()
	text1=('''
		<h3><center>Report Dati Selezionati</center></h3>
		<P>
		<table align="center" width="75%" border="1">
		<tr align="center">
		<th width="15%">Sonda</th>
		<th width="15%">Ora</th>
		<th width="15%">Data</th>
		<th width="15%">Temp</th>
	''')
	text2=('''
		<P>
		<table align="center" width="75%" border="1">
		<tr align="center">
		<th width="15%">Sonda</th>
		<th width="15%">Ora</th>
		<th width="15%">Data</th>
		<th width="15%">Temp</th>
	''')
	i0=42 #Righe per pagina.
	i2=1
	v_ind=0
	text_tab=text1
	v_righe=int(wa.record.text())
	print "inizio stampa .pdf"
	for i in range(0,v_righe):
		ar_a=aStampa[v_ind];v_ind+=1
		ar_b=aStampa[v_ind];v_ind+=1
		ar_c=aStampa[v_ind];v_ind+=1
		ar_d=aStampa[v_ind];v_ind+=1
		text_tab += ("<tr><td >"+str(ar_a)+"</td>"+\
					     "<td >"+str(ar_b)+"</td>"+\
	                     "<td >"+str(ar_c)+"</td>"+\
	                     "<td >"+str(ar_d)+"</td>"+\
	                 "</tr>")
		i2+=1
		if i2>=i0:text_tab+=text2;i2=0
	text2 = text_tab + "</table><center> <P>Stampato il:  "+fStampa+"</center>"
	s_min=wa.vSonda_basso.text()
	s_max=wa.vSonda_alto.text()
	o_min=wa.vOre_basso.text()
	o_max=wa.vOre_alto.text()
	d_min=wa.vData_basso.text()
	d_max=wa.vData_alto.text()
	t_min=wa.vTemp_basso.text()
	t_max=wa.vTemp_alto.text()
	print s_min
	print s_max
	text2+='  '+s_min+' '+s_min+' '+o_min+' '+o_max+' '+d_min+' '+d_max+' '+t_min+' '+t_max   
	doc.setHtml(text2)
	printer=QtGui.QPrinter()
	printer.setOutputFileName("Stampa"+fStampa+".pdf")
	printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
	doc.print_(printer)
	printer.newPage()
	doc.print_(printer)
	wa.ui.Messaggi.append("Creazione file .pdf terminata")
	print "salvato pdf"
#---Fine lavoro, chiude tutto------------------------------------------
def fine_sessione():
	quit()
#---Funzione principale------------------------------------------------
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	wa = Principale()
	wb = Parametri()
	wa.ui.pLegge_EE.hide()
	#wa.ui.Messaggi.hide()
	Impostazioni_iniziali()
	Carica_array_porta()
	Carica_Indici()
	wa.show()
	sys.exit(app.exec_())

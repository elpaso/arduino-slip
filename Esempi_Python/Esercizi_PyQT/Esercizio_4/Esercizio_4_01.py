#!/usr/bin/python
import sys
from PyQt4 import QtGui, QtCore, uic
import serial
SERIALPORT =  '/dev/ttyACM0'

class MyWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui =uic.loadUi('Esercizio_4_00.ui', self)
		self.ui.show()
		self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), invia_arduino_on)
		self.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), invia_arduino_off)
		self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), quit_gui)


def invia_arduino_on():
	testo_arduino = "0"
	arduino.write(testo_arduino)
	msg="Acceso Led 13"
	window.ui.lineEdit.setText(msg)
	window.ui.textEdit.append(str(msg))

def invia_arduino_off():
	testo_arduino = "1"
	arduino.write(testo_arduino)
	msg="Spento Led 13"
	window.ui.lineEdit.setText(msg)
	window.ui.textEdit.append(str(msg))
	
def quit_gui():
	quit()

if __name__ == '__main__':
	arduino = serial.Serial(SERIALPORT, 9600, timeout=1)
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	sys.exit(app.exec_())

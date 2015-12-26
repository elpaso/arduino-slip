#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import serial
import sys, time
SERIALPORT =  '/dev/ttyACM0'
ritardo = 2 #second

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 290, 251, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 510, 85, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(60, 140, 561, 94))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(60, 50, 461, 23))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 370, 251, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(520, 320, 161, 71))
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setProperty("value", 0.0)
        self.lcdNumber.setProperty("intValue", 0)
        self.lcdNumber.setObjectName("lcdNumber")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtGui.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        #QtCore.QObject.connect(MainWindow, QtCore.SIGNAL("destroyed()"), MainWindow.deleteLater)
        
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), invia_arduino_on)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), invia_arduino_off)
        
        #QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), leggi_arduino)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), quit_gui)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), leggi_arduino)
        self.timer.start(2000)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Python QT e Arduino Esercizio 1", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Led 13 On", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        
        self.lineEdit.setText(QtGui.QApplication.translate("MainWindow", "Prova Scrittura Programma Python Qt4", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Led 13 Off", None, QtGui.QApplication.UnicodeUTF8))
        
        self.menuMenu.setTitle(QtGui.QApplication.translate("MainWindow", "Menu", None, QtGui.QApplication.UnicodeUTF8))


def invia_arduino_on():
	testo_arduino = "0"
	arduino.write(testo_arduino)
	msg="Acceso Led 13"
	ui.lineEdit.setText(msg)
	ui.textEdit.append(str(msg))
	#time.sleep(ritardo)

def invia_arduino_off():
	testo_arduino = "1"
	arduino.write(testo_arduino)
	msg="Spento Led 13"
	ui.lineEdit.setText(msg)
	ui.textEdit.append(str(msg))
	#time.sleep(ritardo)
	
def quit_gui():
	quit()

def leggi_arduino():
	da_arduino = str(arduino.readline().rstrip())
	#da_arduino = "Pippo"
	#print(str(da_arduino))
	if (da_arduino):
		ui.textEdit.append(da_arduino)
		if da_arduino[0] == "T":
			ui.lcdNumber.display(da_arduino[1:])
			#ui.lcdNumber.display(1)


if __name__ == "__main__":
    arduino = serial.Serial(SERIALPORT, 9600, timeout=1)
    time.sleep(ritardo)
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    arduino.close()


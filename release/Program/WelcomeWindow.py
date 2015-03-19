from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import sys
import os
import ClickableLabel
from Utility import *

import WelcomeImage
import base64
import Version

from RegWindow import RegWindow

class WelcomeWindow(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setup()
        self.bindSignal()
    
    def bindSignal(self):
        self.connect(self.label, SIGNAL('clicked()'), self.buttonClicked)
           
    def setup(self):
        self.resize(1024,800)

        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
               
        self.label = ClickableLabel.ClickableLabel(self)
        welcome_image_str = base64.b64decode(WelcomeImage.welcome_image_b64)

        # Get data from a Pixmap
        myPixmap = QtGui.QPixmap()
        myPixmap.loadFromData(welcome_image_str)
        self.label.setPixmap(myPixmap)
        
        # Get data from a image file
#         myPixmap = QtGui.QPixmap('welcome.png')
#         self.label.setPixmap(myPixmap)
        
        self.label.setScaledContents(True)
        
        self.verticalLayout.addWidget(self.label)
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle('Seagate Product Registration V%s'%(Version.version))
    
    def buttonClicked(self):
#         self.show_message('SWITCH_WINDOW signal received')
        self.emit(QtCore.SIGNAL("SWITCH_WINDOW"), True)
#         self.show_message('SWITCH_WINDOW end')

    def show_message(self, message):
        QtGui.QMessageBox.warning(self, 'Warning', message, QtGui.QMessageBox.Yes)
       
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show() 
    reg_window = RegWindow()
    reg_window.accessRegPage()
    
    @pyqtSlot()
    def switchWindow():
#         welcome_window.close()
#         reg_window.show_message('SWITCH_WINDOW starts')
        
#         welcome_window.deleteLater()
        welcome_window.close()
        
#         reg_window.show_message('SWITCH_WINDOW complete!')
        
        reg_window.show()     
        

    
    QObject.connect(welcome_window, SIGNAL("SWITCH_WINDOW"), switchWindow)
    
    sys.exit(app.exec_())
    
    
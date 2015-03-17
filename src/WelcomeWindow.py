from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import sys
import os
import ClickableLabel
import Utility
import WelcomeImage
import base64

from RegWindow import RegWindow

RUNNING_DIR = Utility.pathProgram()
print 'RUNNING_DIR', RUNNING_DIR

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

#         self.frame = QtGui.QFrame(self.centralwidget)        
#         self.centralwidget.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Seagate Product Registration')
    
    def buttonClicked(self):
        print('Button Clicked')

        self.emit(QtCore.SIGNAL("SWITCH_WINDOW"), True)
        
if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     main_window = WelcomeWinodw()
#     main_window.show()
#     sys.exit(app.exec_())
     
#     reg_window = RegWindow()
#     reg_window.show()

    app = QtGui.QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show() 
    reg_window = RegWindow()
    
    @pyqtSlot()
    def switchWindow():
        welcome_window.close()
        welcome_window.deleteLater()
        reg_window.show()     
    
    QObject.connect(welcome_window, SIGNAL("SWITCH_WINDOW"), switchWindow)
    
    sys.exit(app.exec_())
    
    
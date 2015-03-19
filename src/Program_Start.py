import sys
import os

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from Program.WelcomeWindow import WelcomeWindow
from Program.RegWindow import RegWindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    reg_window = RegWindow()
    welcome_window.show() 
    
    @pyqtSlot()
    def switchWindow():
#         welcome_window.close()
        global reg_window
        global welcome_window
        
#         welcome_window.deleteLater()
        welcome_window.close()        
        
        reg_window.show_message('SWITCH_WINDOW starts')
        reg_window = RegWindow()
        reg_window.accessRegPage()
        reg_window.show()     
#         reg_window.show_message('SWITCH_WINDOW complete!')
        
    QObject.connect(welcome_window, SIGNAL("SWITCH_WINDOW"), switchWindow)
    
    sys.exit(app.exec_())
    
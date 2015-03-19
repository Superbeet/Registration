import sys
import os

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from Utility import *

import Version

LOG_FILE = os.path.join(pathProgram(), 'log.txt')
print LOG_FILE

class RegWindow(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setup()
        self.variable()
    
    def variable(self):
#         self.basic_url = "http://127.0.0.1:8000/"
        self.basic_url = "http://www.google.com/"        
    
    def setup(self):
        self.resize(1024,800)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.verticalLayout.addWidget(self.webView)
        self.setCentralWidget(self.centralwidget)

        self.setWindowTitle('Seagate Product Registration V%s'%(Version.version))
            
    def accessRegPage(self):
        if not check_connectivity(self.basic_url):
            self.show_message("The Internet is unreachable. Please check network connection.")
            QtCore.QCoreApplication.instance().quit()
        else:
            serial_num = self.getSerialNum(os.path.join('Seagate','SerialNum'), 'SerialNumber.xml')
            
            if serial_num:
                MyPrint("--> Get Serial# - %s" %(serial_num))
                full_url = "%s%s" %(self.basic_url, serial_num)
                MyPrint("--> Access URL - %s" %(full_url))
                self.accessPage(full_url)
                
                return True
            else:
                self.show_message('Please connect Seagate Product to this computer.')
                
                return False
                
    def getSerialNum(self, target_dir , file_name):
        full_path = None
        driveList =  listDrives()
        
        for driveID in driveList:
            if findFolder(driveID, target_dir):
                full_path = os.path.join(driveID, target_dir, file_name)
                MyPrint("--> Find XML File - %s" %(full_path))
                        
        if full_path:         
            drive_info_dict = parseXML(full_path)
            
            return drive_info_dict['SERIAL_NUM']
        else:
            return False

    def accessPage(self, url):
        self.webView.load(QtCore.QUrl(url))
        self.webView.show()

    def show_message(self, message):
        reply = QtGui.QMessageBox.warning(self, 'Warning', message, QtGui.QMessageBox.Yes)
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = RegWindow()
    main_window.show()
    
    sys.exit(app.exec_())
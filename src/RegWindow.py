'''
Created on Mar 10, 2015

@author: 507061
'''

import sys
import os

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from Utility import *

class RegWindow(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setup()
        self.variable()
    
    def variable(self):
        self.basic_url = "http://127.0.0.1:8000/"
    
    def setup(self):
        self.resize(1024,800)
        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.verticalLayout.addWidget(self.webView)
        self.setCentralWidget(self.centralwidget)
    
    def accessRegPage(self):
        if not check_connectivity(self.basic_url):
            self.__show_warning_message("The Internet is unreachable. Please check network connection.")
            QtCore.QCoreApplication.instance().quit()
        else:
            serial_num = self.getSerialNum('Seagate\\SerialNum', 'SerialNumber.xml')
            print "--> Get Serial# - %s" %(serial_num)
            full_url = "%s%s" %(self.basic_url, serial_num)
            print "--> Access URL - %s" %(full_url)
            self.accessPage(full_url)
        
    def getSerialNum(self, target_dir , file_name):
        full_path = None
        
        driveLines =  listDrives()
        for line in driveLines:
            if len(line):   # Avoid search for empty strings
                drive_letter = searchDriveLetter(line)
                if drive_letter: 
                    if findFolder(drive_letter, target_dir):
                        drive_id = drive_letter + ':\\'
                        full_path = os.path.join(drive_id, target_dir, file_name)
                        print full_path
                        
        if full_path:         
            drive_info_dict = parseXML(full_path)
            return drive_info_dict['SERIAL_NUM']
        else:
            return False

    def accessPage(self, url):
        self.webView.load(QtCore.QUrl(url))
        self.webView.show()
   
    def __show_warning_message(self, message):
        reply = QtGui.QMessageBox.warning(self, 'Warning', message, QtGui.QMessageBox.Yes)
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = RegWindow()
    main_window.show()
    
    sys.exit(app.exec_())
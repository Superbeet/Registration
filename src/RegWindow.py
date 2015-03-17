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

import Utility

class RegWindow(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setup()
        
    def setup(self):
        self.resize(1024,800)

        self.centralwidget = QtGui.QWidget(self)
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.verticalLayout.addWidget(self.webView)
        self.setCentralWidget(self.centralwidget)
        
#         self.frame = QtGui.QFrame(self.centralwidget)

        self.default_url = "https://registration.seagate.com/"
        
        self.browse(self.default_url)
        
    def browse(self, url):
        """
            Make a web browse on a specific url and show the page on the
            Webview widget.
        """
        self.webView.load(QtCore.QUrl(url))
#         print self.html
        self.webView.show()
   
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = RegWindow()
    main_window.show()
    sys.exit(app.exec_())
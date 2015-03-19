from PyQt4.QtGui import *
from PyQt4.QtCore import *
 
class ClickableLabel(QLabel):
 
    def __init__(self, parent):
        QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, event):
#         self.__show_message('Label clicked')
        self.emit(SIGNAL('clicked()'))
        
    def __show_message(self, message):
        reply = QMessageBox.warning(self, 'Warning', message, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            print "YES"
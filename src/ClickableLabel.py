from PyQt4.QtGui import *
from PyQt4.QtCore import *
 
class ClickableLabel(QLabel):
 
    def __init__(self, parent):
        QLabel.__init__(self, parent)
 
    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))
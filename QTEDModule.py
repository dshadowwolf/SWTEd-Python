from PyQt4 import QtCore
from PyQt4 import QtGui
import sys


class QTEDModule( QtCore.QObject ):
    def __init__(self, parent=None,loaded_as=None):
        QtCore.QObject.__init__(self,parent)
        self.name = None
        self.module_type = None
        self.loadname = loaded_as
        self.__parent_link__ = parent
        
    def register(self):
        k = QtGui.QMessageBox.critical( self.__parent_link__, "QTEDModule", "QTEDModule Base register method called - this might be an error in your code.\nExiting anyway - this code should not have been reached." )
        sys.exit()

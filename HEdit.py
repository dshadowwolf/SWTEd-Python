from PyQt4 import QtCore
from PyQt4 import QtGui

class HEditor(QtGui.QTextEdit):
    def __init__(self,parent=None):
        QtGui.QTextEdit.__init__(self,parent)
        self.setAcceptRichText(False)
        self.__highlightMods__ = { 'HTML': ('html_highlight','HTML_H') }
        self.__hl__ = None
        
        self.setHighlighter('HTML')
        self.setFontFamily( 'Arial' )
    def setHighlighter(self,name):
        z = self.__highlightMods__[name]
        exec "from %s import %s" % (z[0], z[1])
        self.__hl__ = eval("%s(self.document())" % z[1])
        

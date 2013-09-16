from PyQt4 import QtCore
from PyQt4 import QtGui
from QTEDModule import *

class AboutBox( QtGui.QDialog ):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.initLayout()
        
    def initLayout(self):
        self.__tab_bar__ = QtGui.QTabWidget(self)
        data = "WolfTech Extensible Editor v1.0\nCopyright (C) 2008 Daniel Hazelton"
        basic_tab = QtGui.QLabel( data, self.__tab_bar__ )
        self.__tab_bar__.addTab( basic_tab, "About" )
        lfile = file( "LICENSE", "r" )
        ltab = QtGui.QTextEdit( self.__tab_bar__ )
        ltab.append( lfile.read() )
        ltab.setReadOnly( True )
        lfile.close()
        self.__tab_bar__.addTab( ltab, "License" )
        layout = QtGui.QVBoxLayout(self)
        self.__close_button__ = QtGui.QPushButton("Close")
        self.connect(self.__close_button__,QtCore.SIGNAL("clicked()"),QtCore.SLOT("accept()"))
        layout.addWidget(self.__tab_bar__)
        layout.addWidget(self.__close_button__)
        self.setLayout( layout )
        
class AboutSystem( QTEDModule ):
    def __init__(self, parent=None,loaded_as=None):
        QTEDModule.__init__(self,parent,loaded_as)
        self.name = "QTED Base Help->About system"
        self.module_type = "Basic"
        self.__aboutBox__ = AboutBox( self.__parent_link__ )
        self.__actions__ = {
           'HELP_ABOUT': [ self.loadname, 'about', 'SHIFT+F1', "About QTED", "&About", None ],
           'HELP_ABOUT_QT': [ 'QtApp', 'aboutQt', 'CTRL+SHIFT+F1', "About Qt4", "About Qt4", None ] }
        self.__menu__ = [{ 'name': 'Help',
                           'display': '&Help',
                           'data': [('STD', 'HELP_ABOUT'), ('STD', 'HELP_ABOUT_QT')] } ]
        
    def register(self):
        pl = self.__parent_link__
        pl.addActions( self.__actions__ )
        pl.addMenus( self.__menu__ )
        
    def about(self):
        self.__aboutBox__.show()

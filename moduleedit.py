from PyQt4 import QtCore
from PyQt4 import QtGui
from QTEDModule import *

class FindDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, self)
        self.rval = [ False, False, False ]
        self.phrase = None
        self.initLayout()
        
    def initLayout(self):
        self.controls = []
        
        # setup the "search terms" item
        box = QtGui.QHBoxLayout()
        lab = QtGui.QLabel("Search Terms",self)
        self.words = QtGui.QLineEdit(self)
        box.addWidget(lab)
        box.addWidget(self.words)
        self.layout.addLayout(box)
        
        # setup the "search modifiers" stuff
        frm = QtGui.QHBoxLayout()
        checkCaseSensitive = QtGui.QCheckBox( "Match Case", self)
        checkBackwards = QtGui.QCheckBox( "Search Backwards", self)
        checkWholeWords = QtGui.QCheckBox( "Match Whole Words Only", self)
        frm.addWidget( checkCaseSensitive )
        frm.addWidget( checkBackwards )
        frm.addWidget( checkWholeWords )
        self.connect( checkCaseSensitive, QtCore.SIGNAL("stateChanged(int)"), self.slotCSense )
        self.connect( checkBackwards, QtCore.SIGNAL("stateChanged(int)"), self.slotBWords )
        self.connect( checkWholeWords, QtCore.SIGNAL("stateChanged(int)"), self.slotWWords )
        self.layout.addLayout( frm )
        
        # setup the buttons
        buttons = QtGui.QHBoxLayout()
        ok = QtGui.QPushButton( "Search" )
        cn = QtGui.QPushButton( "Cancel" )
        buttons.addWidget(ok)
        buttons.addWidget(cn)
        self.layout.addLayout(buttons)
        self.connect( ok, QtCore.SIGNAL("clicked()"), self.accept )
        self.connect( cn, QtCore.SIGNAL("clicked()"), self.reject )
        
    def slotCSense(self):
        if self.rval[0]:
            self.rval[0] = False
        else:
            self.rval[0] = True
            
    def slotBWords(self):
        if self.rval[1]:
            self.rval[1] = False
        else:
            self.rval[1] = True
            
    def slotWWords(self):
        if self.rval[2]:
            self.rval[2] = False
        else:
            self.rval[2] = True
            
    def exec_(self):
        kx = QtGui.QDialog.exec_(self)
        return (self.rval, self.phrase)
    
    def accept(self):
        QtGui.QDialog.accept(self)
        self.phrase = self.words.text()
        
    def reject(self):
        QtGui.QDialog.reject(self)
        self.phrase = None
        self.rval = -1
        
class EditSys( QTEDModule ):
    def __init__(self,parent=None,loaded_as=None):
        QTEDModule.__init__(self,parent,loaded_as)
        self.name = "QTED Base Edit/Search Menu/Toolbar System"
        self.module_type = "Basic"
        self.previous = None
        self.find = FindDialog( self.__parent_link__ )
        self.__actions__ = {
            'EDIT_COPY': [ self.loadname, 'edit_copy', 'CTRL+C', "Copy marked block", "&Copy", "icons/copy.png" ],
            'EDIT_CUT': [ self.loadname, 'edit_cut', 'CTRL+X', "Cut marked text", "Cut", "icons/cut.png" ],
            'EDIT_PASTE': [ self.loadname, 'edit_paste', 'CTRL+V', "Paste Text From Buffer", "Paste", "icons/paste.png" ],
            'EDIT_FIND': [ self.loadname, 'edit_find', 'CTRL+F', "Search for Text", "&Find", "icons/find_normal.png" ],
            'EDIT_REGEX_FIND': [ self.loadname, 'edit_regex_find', 'CTRL+R', "Search using a Regex", "Regex Search", "icons/find_regex.png" ],
            'EDIT_FIND_REPEAT': [ self.loadname, 'edit_find_repeat', 'F3', "Repeat your last search", "Repeat Find", None ],
            'EDIT_UNDO': [ self.loadname, 'edit_undo', 'CTRL+Z', "Undo your last edit", "Undo", 'icons/undo.png' ],
            'EDIT_REDO': [ self.loadname, 'edit_redo', 'SHIFT+CTRL+Z', "Redo your last edit", "Redo", 'icons/redo.png' ] } 
        self.__menus__ = [
           { 'name': 'EDIT',
             'display': '&Edit',
             'data': [('STD', 'EDIT_UNDO'), ('STD', 'EDIT_REDO'),
                      ('STD', 'EDIT_COPY'), ('STD', 'EDIT_CUT'), 
                      ('STD', 'EDIT_PASTE'), ('STD', None),
                      ('STD', 'EDIT_FIND'), ('STD', 'EDIT_REGEX_FIND'), 
                      ('STD', 'EDIT_FIND_REPEAT')] } ]
        self.__tools__ = [
            { 'name': 'EDIT',
              'symbolic': 'Editing',
              'data': ['EDIT_UNDO', 'EDIT_REDO', 'EDIT_CUT','EDIT_COPY','EDIT_PASTE'] },
            { 'name': 'SEARCH',
              'symbolic': 'Search',
              'data': ['EDIT_FIND','EDIT_REGEX_FIND'] } ]
              
    def register(self):
        pl = self.__parent_link__
        pl.addActions( self.__actions__ )
        pl.addMenus( self.__menus__ )
        pl.addTools( self.__tools__ )

    def edit_copy(self):
        self.__parent_link__.copy()
        
    def edit_paste(self):
        self.__parent_link__.paste()
        
    def edit_cut(self):
        self.__parent_link__.cut()
        
    def edit_find(self):
        (rval, phrase) = self.find.exec_()
        if phrase != None:
            rf = QtGui.QTextDocument.FindFlags()
        if rval[0]:
            rf |= QtGui.QTextDocument.FindCaseSensitively
        if rval[1]:
            rf |= QtGui.QTextDocument.FindBackwards
        if rval[2]:
            rf |= QtGui.QTextDocument.FindWholeWords
            
        rv = self.__parent_link__.find( phrase, rf )
        if rv is None:
            QtGui.QMessageBox.information( self.__parent_link__, "QTED", "Nothing Found!" )
        self.previous = [ rf, phrase ]
        
    def edit_regex_find(self):
        QtGui.QMessageBox.warning( self.__parent_link__, "QTED", "Feature Not Yet Implemented" )
        
    def edit_find_repeat(self):
        if self.previous is None:
            self.slotFind()
        else:
            self.__parent_link__.find( self.previous[1], self.previous[0] )
                                    
    def edit_undo(self):
        self.__parent_link__.undo()
        
    def edit_redo(self):
        self.__parent_link__.redo()

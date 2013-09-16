from PyQt4 import QtCore
from PyQt4 import QtGui
from QTEDModule import *
import posixfile

class FileSys( QTEDModule ):
    def __init__(self,parent=None,loaded_as=None):
        QTEDModule.__init__(self,parent,loaded_as)
        self.name = "QTED Base File Menu/Toolbar System"
        self.module_type = "Basic"
        self.__actions__ = {
            'FILE_NEW': [ self.loadname, 'file_new', 'CTRL+N', "New File", "&New", "icons/new.png" ],
            'FILE_OPEN': [ self.loadname, 'file_open', 'CTRL+O', "Open File", "&Open", "icons/open.png" ],
            'FILE_SAVE': [ self.loadname, 'file_save', 'CTRL+S', "Save File", "&Save", "icons/save.png" ],
            'FILE_SAVE_AS': [ self.loadname, 'file_save_as', 'CTRL+A', "Save File As...", "Save &As", "icons/saveas.png" ],
            'FILE_EXIT': [ 'QtApp', 'quit', 'CTRL+X', "Exit this Program", "E&xit", None ] }
        self.__menus__ = [
            { 'name': 'FILE',
              'display': '&File',
              'data': [('STD', 'FILE_NEW'), ('STD', 'FILE_OPEN'), 
                       ('STD', 'FILE_SAVE'), ('STD', 'FILE_SAVE_AS'), 
                       ('STD', None), ('STD', 'FILE_EXIT')] } ]
        self.__tools__ = [
            { 'name': 'FILE',
              'symbolic': 'File Interaction',
              'data': ['FILE_NEW','FILE_OPEN','FILE_SAVE','FILE_SAVE_AS'] } ]
        self.__filename__ = None
        
    def register(self):
        self.setRecentFiles()
        pl = self.__parent_link__
        pl.addActions( self.__actions__ )
        pl.addMenus( self.__menus__ )
        pl.addTools( self.__tools__ )
        
    def setRecentFiles(self):
        self.__rcu__ = [ 'qted.py', 'notes', 'LICENSE', 'qted.py.original' ]
        slots = self.__actions__
        t = 0
        slot_names = []
        mnu = { 'name': 'RECENT_FILES',
                'display': '&Recent Files',
                'data': [] }
                
        for file in self.__rcu__:
            slot_name = "RECENT_FILE_%i" % t
            slots[slot_name] = ( 'FILE', 'recent_file_%i' % t, None, "Recent File %i (%s)" % (t, file), "%i) %s" % ( t+1, file), None )
            slot_names.append(slot_name)
            t += 1
            if t >= 4:
                break
            
        c = 0;
        for entry in self.__menus__[0]['data']:
            if entry[1] == 'FILE_EXIT':
                target = c
            else:
                c += 1
                
        for name in slot_names:
            mnu['data'].append( ('STD', name) )
        self.__menus__[0]['data'].insert(c, ('STD', None) )
        self.__menus__[0]['data'].insert(c, ('SUB_MENU', mnu) )
        
    def file_open(self):
        pl = self.__parent_link__
        fileName = str( QtGui.QFileDialog.getOpenFileName( pl, "Open File", "","", "") )
        self.__filename__ = fileName
        self.loadFile()
        
    def loadFile(self):
        pl = self.__parent_link__
        fl = QtCore.QFile( self.__filename__ )
        fl.open( QtCore.QIODevice.ReadOnly )
        fl.setTextModeEnabled( True )
        pl.editor.setPlainText(fl.read(fl.size()))
        fl.close()
        
    def file_new(self):
        self.__parent_link__.__class__().show()
    
    def file_save(self):
        pl = self.__parent_link__
        if self.__filename__ is None:
            return self.file_save_as()
        else:
            return self.__saveFile__()
    
    def file_save_as(self):
        pl = self.__parent_link__
        fn = QtGui.QFileDialog.getSaveFileName(pl)
        if fn is None or fn == '':
            return False
        else:
            self.__filename__ = fn
            return self.__saveFile__()
  
    def __saveFile__(self):
        f = QtCore.QFile(self.__filename__)
        if not f.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text ):
            self.__parent_link__.error( "Unable to open file %s for writing!" % self.__filename__.toUtf8().data() )
        else:
            f.writeData( self.__parent_link__.Text() )
        self.xstatusBar( "File Saved!", 3000 )
        f.close()
        return True
    
    def __maybeSave__(self):
        pl = self.__parent_link__
        if pl.modified():
            ret = QtGui.QMessageBox.warning( pl, "QTED", "The document has been modified.\nAre you sure you wish to quit without saving?", QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel )
            if ret == QtGui.QMessageBox.Save:
                if self.__filename__ is None:
                    self.file_save_as()
                else:
                    self.__saveFile__()
            elif ret == QtGui.QMessageBox.Discard:
                return True
            else:
                return False
    
    def open_recent_file(self,num):
        self.__filename__ = self.__rcu__[num]
        self.loadFile()
        
    def recent_file_0(self):
        self.open_recent_file(0)
    
    def recent_file_1(self):
        self.open_recent_file(1)
    
    def recent_file_2(self):
        self.open_recent_file(2)
    
    def recent_file_3(self):
        self.open_recent_file(3)
    

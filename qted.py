#!/usr/bin/env python

from PyQt4 import QtCore
from PyQt4 import QtGui
from HEdit import HEditor
import sys
import string
        
class EditorWindow( QtGui.QMainWindow ):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.__modules__ = { 'self': self, 'QtApp': QtGui.qApp }
        self.__loadModules__ = [ ('FILE','modulefile','FileSys'),
                                 ('EDIT','moduleedit','EditSys'),
                                 ('ABOUT','moduleabout','AboutSystem')]
        self.__setup_data__ = {
          'slots': { },
          'menu': [ ],
          'toolbar': [ ] }
        self.__processing__ = None
        
        self.loadModuleConfig()
        self.loadModules()
        self.initInterface()
        self.buildActions()
        self.buildMenus()
        self.buildToolBar()
        self.statusBar().showMessage("QTED v. 1.0 alpha", 5000)

    def loadModuleConfig(self):
        f = open( "qted_modules.rc", 'r' )
        for l in f.readlines():
            if len(l.lstrip().rstrip()) > 0:
                (loadName,modName,className) = string.split(l.lstrip().rstrip(),"|")
                self.__loadModules__.append( (loadName,modName,className) )
        f.close()
        
    def addActions(self,acts):
        for name in acts:
            self.__setup_data__['slots'][name] = acts[name]
            
    def addMenus(self,menus):
        for menu in menus:
            self.__setup_data__['menu'].append(menu)
            
    def addTools(self,tools):
        for tool in tools:
            self.__setup_data__['toolbar'].append(tool)
            
    def loadModules(self):
        modules = self.__loadModules__
        for module in modules:
            mname = module[0]
            self.__processing__ = mname
            mod_file = module[1]
            mod_class = module[2]
            print "Loading Module %s" % mname
            exec "from %s import %s" % (mod_file, mod_class)
            mod_handle = eval( "%s(self, '%s')" % (mod_class, mname) )
            self.__modules__[mname] = mod_handle
            mod_handle.register()
        self.__processing__ = None
    
    def initInterface(self):
        self.editor = HEditor(self)
        self.setCentralWidget( self.editor )
        
    def buildActions(self):
        self.__actions__ = {}
        
        slots = self.__setup_data__['slots']
        for slot in slots:
            slot_data = slots[slot]
            slot_name = slot_data[4]
            if slot_data[5] is not None:
                act_image = self.__loadPixmap__( slot_data[5] )
                action = QtGui.QAction( act_image, slot_name, self )
            else:
                action = QtGui.QAction( slot_name, self )
                
            if slot_data[2] is not None:
                action.setShortcut( QtGui.QKeySequence( slot_data[2] ) )
                
            if slot_data[3] is not None:
                action.setToolTip( slot_data[3] )
                
            self.connect( action, QtCore.SIGNAL("triggered()"), self.__modules__[slot_data[0]].__getattribute__(slot_data[1]) )
            
            self.__actions__[slot] = action
                
            
    def buildMenu(self,data):
        dname = data['display']
        menu = QtGui.QMenu( dname, self )
        idata = data['data']
        for item in idata:
            if item[0] == 'SUB_MENU':
                menu.addMenu( self.buildMenu( item[1] ) )
            else:
                action = item[1]
                if action is None:
                    menu.addSeparator()
                else:
                    menu.addAction( self.__actions__[action] )
        return menu
        
    def buildMenus(self):
        menudata = self.__setup_data__['menu']
        for menu in menudata:
            n_menu = self.buildMenu( menu )
            self.menuBar().addMenu( n_menu )
        
    def buildToolBar(self):
        toolbars = self.__setup_data__['toolbar']
        for toolbar in toolbars:
            bar_name = toolbar['symbolic']
            bar_data = toolbar['data']
            ntb = self.addToolBar( bar_name )
            for tool in bar_data:
                tool_act = self.__actions__[tool]
                ntb.addAction( tool_act )
    
    def __loadPixmap__(self,name):
        i = QtGui.QImage( name )
        j = QtGui.QPixmap().fromImage( i.scaled( QtCore.QSize(22, 22), 
                                   QtCore.Qt.IgnoreAspectRatio, 
                                   QtCore.Qt.SmoothTransformation ) )
        return QtGui.QIcon(j)

    def setText(self,text):
        self.editor.setText( text )
        
    def xstatusBar(self,text,time):
        self.statusBar().showMessage(text,time)
        
    def errorPopup(self,text):
        QtGui.QMessageBox.warning( self, "QTED", text )
        
    def Text(self):
        return self.editor.toPlainText()
    
    def textEmpty(self):
        if self.editor.toPlainText().isEmpty():
            return True
        else:
            return False
    def undo(self):
        self.editor.undo()
    def redo(self):
        self.editor.redo()
    def find(self, text, flags):
        self.editor.find( text, flags )
    def copy(self):
        self.editor.copy()
    def cut(self):
        self.editor.cut()
    def paste(self):
        self.editor.paste()
        
def main():
    app = QtGui.QApplication(sys.argv)
    mwin = EditorWindow()
    mwin.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
            

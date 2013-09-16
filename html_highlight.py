from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

class HTML_H(QtGui.QSyntaxHighlighter):
    def __init__(self,parent=None):
        QtGui.QSyntaxHighlighter.__init__(self,parent)
        self.__baseRules__ = {
          'COMMENT': (Qt.Qt.cyan, ('italic', None)),
          'TAG': (Qt.Qt.magenta, ('mono', None)),
          'ENTITY': (Qt.Qt.black, ('bold','underline')),
          'DOCTYPE': (Qt.Qt.blue, ('mono', 'italic')),
          'TEXT': (Qt.Qt.black, None ),
          'JS': (Qt.Qt.lightGray, ('mono', 'italic')),
          'JSCOM': (Qt.Qt.blue, ('mono', 'italic')),
          'JSKEY': (Qt.Qt.gray, ('mono', None)) }
        self.__jscrap__ = [
          'NaN','infinity', 'undefined', 'object', 'function', 'Array',
          'String', 'Boolean', 'Number', 'Math', 'Date', 'RegExp', 'Error',
          'break', 'else', 'new', 'var', 'case', 'finally', 'return', 'void',
          'catch', 'for', 'switch', 'while','continue', 'this', 'with',
          'default', 'if', 'throw', 'delete', 'in', 'try', 'do', 'instanceof',
          'typeof', 'abstract', 'enum', 'int', 'short', 'boolean', 'export', 
          'interface', 'static', 'byte', 'extends', 'long', 'super', 'char', 
          'final', 'native', 'synchronized', 'class', 'float', 'package', 
          'throws', 'const', 'goto', 'private', 'transient', 'debugger', 
          'implements', 'protected', 'volatile', 'double', 'import', 'public' ]
        self.__inJS__ = 0
        self.__rules__ = {}
        self.buildRules()
        self.setCurrentBlockState(-1)
        
    def buildRules(self):
        for r in self.__baseRules__:
            rr = self.__baseRules__[r]
            rule = QtGui.QTextCharFormat()
            rule.setForeground( QtGui.QBrush(rr[0] ) )
            if rr[1] is not None:
                for x in rr[1]:
                    if x == 'italic':
                        rule.setFontItalic(True)
                    elif x == 'bold':
                        rule.setFontWeight( QtGui.QFont.Bold )
                    elif x == 'underline':
                        rule.setFontUnderline( True )
                    elif x == 'strike':
                        rule.setFontStrikeOut( True )
                    elif x == 'mono':
                        rule.setFontFixedPitch( True )
                    elif x == 'light-bold':
                        rule.setFontWeight( QtGui.QFont.DemiBold )
                    elif x is not None and QtCore.QString(x).left(5) == 'font:':
                        rule.setFontFamily( QtCore.QString(x).right(5) )
                    else:
                        if x is not None:
                            raise ValueError( "Unknown rule specifier %s" % x )
            self.__rules__[r] = rule
           
    def highlightBlock(self, text):
        st = self.previousBlockState()
        l = text.length()
        s = 0
        p = 0
        while p < l:
            ch = text.at(p).toAscii()
                if st == -1:
                    if ch == '<' and self.__inJS__ == 0:
                        if text.mid(p,4) == '<!--':
                            self.setCurrentBlockState(1)
                            st = 1
                        elif text.mid(p,9) == '<![CDATA[':
                            self.setCurrentBlockState(2)
                            st = 2
                        elif text.mid(p,9) == '<!DOCTYPE':
                            self.setCurrentBlockState(3)
                            st = 3
                        else:
                            self.setCurrentBlockState(4)
                            st = 4
                    elif ch == '&' and self.__inJS__ == 0:
                        i = p
                        while text.at(i).toAscii() != ';':
                            i += 1
                            self.setFormat(p,i - p,self.__rules__['ENTITY'])
                            p = i
                    elif self.__inJS__ == 1:
                        if text.mid(p,2) == '/*':
                            self.setCurrentBlockState(5)
                        elif text.mid(p,2) == '//':
                            self.setCurrentBlockState(6)
                        elif text.mid(p,2) == '</':
                            self.__inJS__ = 0
                            self.setCurrentBlockState(4)
                        else:
                            self.setCurrentBlockState(7)
                    else:
                        p += 1
                elif st == 1:
                    i = p
                    c = 1
                    while i < l and c == 1:
                        if text.mid(i,3) == '-->':
                            c = 0
                        else:
                            i += 1
                        
                    if c == 0:
                        i += 3
                        self.setCurrentBlockState(-1)
                        st = -1
                    i += 1
                    self.setFormat( p, i - p, self.__rules__['COMMENT'] )
                    p = i
                elif st == 2:
                    i = p
                    c = 1
                    while i < l and c == 1:
                        if text.mid(i,3) == ']]>':
                            c = 0
                        else:
                            i += 1
                        
                    if c == 0:
                        i += 3
                        self.setCurrentBlockState(-1)
                        st = -1
                    i += 1
                    self.setFormat( p, i - p, self.__rules__['COMMENT'] )
                    p = i
                elif st == 3:
                    i = p
                    c = 1
                    while i < l and c == 1:
                        if text.at(i).toAscii() == '>':
                            c = 0
                        else:
                            i += 1
                    i += 1
                    if c == 0:
                        self.setCurrentBlockState(-1)
                        st = -1
                    self.setFormat( p, i - p, self.__rules__['DOCTYPE'] )
                    p = i
                elif st == 4:
                    i = p
                    c = 1
                    inString = 0
                    while i < l and c == 1:
                        if text.at(i).toAscii() == '>' and inString == 0:
                            c = 0
                            i += 1
                        elif text.at(i).toAscii() == '"':
                            if inString == 0:
                                inString = 1
                            else:
                                inString = 0
                                i += 1
                        else:
                            i += 1
                    if c == 0:
                        self.setCurrentBlockState(-1)
                        st = -1
                        self.setCurrentBlockState( -1 )
                        z = text.toLower().mid(p,6)
                        print z
                        if z == 'script':
                            self.__inJS__ = 1
                        elif z == '<scrip':
                            self.__inJS__ = 1
                        elif z == 'cript>':
                            self.__inJS__ = 1
                    self.setFormat( p, i - p, self.__rules__['TAG'] )
                    p = i
                elif st == 5:
                    self.setCurrentBlockState(-1)
                elif st == 6:
                    self.setCurrentBlockState(-1)
                elif st == 7:
                    self.setCurrentBlockState(-1)
                else:
                    raise ValueError( "Unknown state while applying format (%i)!" % st )
                    

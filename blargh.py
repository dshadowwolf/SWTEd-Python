class mException(Exception):
    def __init__(self,code,msg):
        Exception.__init__(self)
        self.__code__ = code
        self.__message__ = msg
    
    def __getitem__(self,it):
        if it == 0:
            return self.__code__
        elif it == 1:
            return self.__message__
        else:
            return Exception.__getitem__(self,it)

z = mException(0,"None")
l = mException(1,"IO Error")

print dir(z)
print dir(l)
print dir(Exception(1,"blargh"))
(c,m) = z
(d,n,v) = l

print c+"-"+m
print d+"-"+n+"-"+v

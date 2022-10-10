

class Proxy(object):
    def __init__(self,host,port,score=0) -> None:
        self.host = host
        self.port = port
        self.score = score
    
    def __str__(self) -> str:
        return self.host + ':' + str(self.port)

    def string(self) -> str:
        return self.__str__()

    def tostring_wscore(self):
        return self.tostring() + ' ' + str(self.score)
    
if __name__ == '__main__':
    p = Proxy('111','2',10)
    print(p)
    print(type(p))
    print(p.tostring())
    print(p.tostring_wscore())

    

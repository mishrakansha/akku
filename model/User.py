import random

class User: 

    username = ''                                                                                                                                                                                                                                                                 
    idLength = 8
    admin = False
    Banned = False
    banReason = None
    terminated = False
    userid = ''.join([chr(random.randint(65,90)) for i in range(idLength)])
    socketBind = []
    clientFD = [] #socket.bind(())

    def __init__(self, ip, port, username) -> None:
        if(username == ''):        
            self.username = self.userid
        else:
            self.username = username
        self.socketBind.append(ip)
        self.socketBind.append(port)

    def getID(self):
        return self.username
    
    def setAdmin(self) -> None:
        self.admin = True
    
    def getFD(self):
        return self.clientFD

    def setBanned(self):
        self.Banned = True

    def setReason(self, r):
        self.banReason = r
    
    def getReason(self):
        return self.banReason

    def getBanned(self):
        return self.Banned 

    def setTerminated(self):
        self.terminated = True
    
    def getTerminated(self):
        return self.terminated
    

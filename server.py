import socket
from py_console import console
import sys
from _thread import *
import threading 
import filter 
from model.User import User
import _logging
from time import gmtime, strftime

class Base:

    print_lock = threading.Lock()
    port = 1234
    host = '0.0.0.0'
    maxConnections = 10
    count = 0
    cliArr = dict() # username:socketfd
    usersArr = []
    BannedUsersArr = []

    def __init__(self) -> None:
        console.log('starting...')
        if(len(sys.argv) >= 2):
            self.port = int(sys.argv[1])
            console.warn('port: '+str(self.port))
        else:
            console.log("port 1234...")
    
    def keepitLocked(self, name): # keep the username banned
      for username in self.BannedUsersArr:
        if(name == username):
          console.log("keepitLocked:=>"+username)
          return True
      return False

    def broadcastMessages(self, cliArr, username, clientBuffer):
        stringToSend = username.encode()+b','+clientBuffer #+ b'\n' # modification needed
        for tempUsername, val in cliArr.items():
            if(tempUsername == username):
                continue
            cli = val
            try:
                cli.send(stringToSend)
            except Exception as e:
                console.error(str(e))

    def reqHandler(self, cli, addr):
        time_str = None
        self.print_lock.release()
        username = cli.recv(1024).strip()
        if(False):#self.keepitLocked(username.decode())):
           console.warn('Host disconnected!')
           cli.send(b'HORSE EXIT')
           # have to remove the Sockfd from Userbuffer
           cli.close()
           return
        if(username == b''):
            threadUser = User(addr[0], addr[1], '')
            self.usersArr.append(threadUser)
            
        else:
            threadUser = User(addr[0], addr[1], username.decode())
            self.usersArr.append(threadUser)
        username = threadUser.getID().encode()
        print("username:", username.decode())
        self.cliArr[username.decode()] = cli
        while True:
            if(threadUser.getBanned()):
                bannedStr = username + b', is Banned!'
                cli.send(bannedStr)
                _logging.save(username.decode(), threadUser.getReason(), time_str)
                cli.close()
                self.cliArr.pop(username.decode()) # remove the banned socketFD
                exit()
            clientBuffer = cli.recv(2024)
            # check from filter.py
            filterObj = filter.Filter(1, clientBuffer)
            isCurse = filterObj.api_filter(clientBuffer.decode())
            if(isCurse):
                console.warn(threadUser.getID()+" abused!")
                time_str = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                threadUser.setBanned()
                threadUser.setReason(isCurse)
                self.BannedUsersArr.append(threadUser.getID())
                continue
            if(clientBuffer.decode().strip() == 'bye'):
                console.warn('Host disconnected!')
                cli.send(b'HORSE EXIT')
                self.cliArr.pop(username.decode())
                # have to remove the Sockfd from Userbuffer
                cli.close()
                exit()
            self.broadcastMessages(self.cliArr, username.decode(), clientBuffer)
            console.log(clientBuffer.decode().strip())

    def socketAddrCreate(self):
        host = self.host
        port = self.port
        socketfd = socket.socket()
        socketfd.bind((host, port))
        socketfd.listen(self.maxConnections)
        while True:
            cli, addr = socketfd.accept()
            self.print_lock.acquire()
            console.log('connected to '+addr[0])
            start_new_thread(self.reqHandler, (cli, addr,))

if __name__ == "__main__":
    base = Base()
    base.socketAddrCreate()




    

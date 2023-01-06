#!/bin/bash
import socket
from py_console import console
import sys
from model.User import User
from cmd import Cmd
import threading
import time
import argparse
from keyboard import press

user = None
HOST = '127.0.0.1'
PORT = 1234
username = ''
parser = argparse.ArgumentParser(prog= "gugu",
                                 description = "client script of gugu to connect",
                                 epilog = "@luckythandel")
parser.add_argument('--port', '-p', type=int)
parser.add_argument('--username', '-u', type=str, required=True)

args = parser.parse_args()
if(args.username):
    username = args.username
if(args.port):
  PORT = args.port
user = User(HOST, PORT, username)

console.log('Welcome!')
console.log('Entering with the name: '+username)

def connection_create(HOST, PORT):
    try:
        socketfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketfd.connect((HOST, PORT))
        socketfd.send(username.encode())
        return socketfd
    except Exception as e:
        console.error('Can\'t connect to the port: '+str(PORT))
        exit()

class Client(Cmd):
    clientfd = None
    user = None
    file = None
    fds = []
    intro = '''
    Basic Chat Channel
    But Dont you dare curse anyone here!
    '''
    prompt  = '('+username+') '
    
    def __init__(self, clientfd, user):
        Cmd.__init__(self)
        self.clientfd = clientfd
        self.user = user
    class fdThread:
        def __init__(self):
            self._running = True

        def recvThread(self):
            while True:
               try:
                   tempRecv = clientfd.recv(1024)
                   if(tempRecv == b'HORSE EXIT'):
                       exit()
                   if(tempRecv == username.encode()+b', is Banned!'):
                       clientfd.close()
                   t = tempRecv.decode().find(',')
                   user = tempRecv.decode()[:t]; msg = tempRecv.decode()[t+1:]
                   print("\r" + user + ': '+ msg)
               except Exception as e:
                       return

        def terminate(self):
            pass

        def run(self, n):
            while self._running and n > 0:
                self.recvThread()
                sys.stdout.flush()
                self._running = False
                n -= 1
                time.sleep(n)

    def preloop(self):
        try:
            tempThreadObj = self.fdThread()
            tempThreadObj = threading.Thread(target=tempThreadObj.run, args=(3,))
            #tempThreadObj.deamon = True
            tempThreadObj.start()
            tempThreadObj.terminate()
            tempThreadObj.join()
            print("[+]main: ", threading.get_ident())
        except Exception as e:
            pass


    def postloop(self):
        try:
            print("[+] Status:", self.fds[0])
        except:
            pass
    
    def do_info(self, arg):
        print("[+] Username:", username)
        print("[+] IP:", HOST)
        print("[+] Port: ", PORT)
    
    def emptyline(self):
        pass

    def default(self, line):
        try:
            self.clientfd.send(line.encode())
        except Exception as e:
            console.error('you are disconnected')
    
    def do_bye(self, arg):
        try:
            print("[-] Closing...")
            self.clientfd.send(b'bye')
            return True
        except Exception as e:
            print("socket is already closed")
            return True

if __name__ == "__main__":
    clientfd = connection_create(HOST, PORT)
    clientShell = Client(clientfd, user)
    clientShell.cmdloop()

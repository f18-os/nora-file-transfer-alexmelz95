#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import params
from framedSock import FramedStreamSock
from threading import Thread
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)

       print([f for f in listdir(os.getcwd())])
       command = ""
       while not command:
           command = input("Enter a file name or change a directory: ")
           args = command.split()
           if args[0] == "cd":
               dir = ""
               newdir = ""
               dir = os.getcwd()
               dir = dir.split("/")
               if(args[1] == ".."):
                   for i in range(len(dir)-1):
                       newdir += dir[i]
                       if i != len(dir)-2:
                           newdir += "/"
               else:
                   newdir = args[1]
               os.chdir(newdir)
               onlyfiles = [f for f in listdir(os.getcwd())]
               print(onlyfiles)
               command = ""

           try:
               inputFile = open(command, "r")
           except FileNotFoundError:
               print("File Not Found Error")
               command = ""

           inputText = inputFile.read()
           if not inputText:
               print("File is empty. Please use a file with contents.")
               command = ""

       #View #1 on Collaboration Report
       input = bytearray(inputFile, 'utf-8')
       fs.sendmsg(input)
       line = f.read(100)
       while(line):
           fs.sendmsg(bytearray(line))
           line = f.read(100)


       try:
           print("Received: ", fs.receivemsg())

       except:
           print('Error Receiving')


       ClientThread(serverHost, serverPort, debug)

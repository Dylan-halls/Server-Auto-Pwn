#!/usr/bin/env python3

import threading
import random
import socket
import queue

class Scanner(threading.Thread):
    def __init__(self, args, in_q, out_q):
        threading.Thread.__init__(self)
        self.args = args
        self.in_q = in_q
        self.out_q = out_q
        self.services = []
    def run(self):
        try:
            while True:
                port = self.in_q.get(0)
                try:
                    s = socket.socket()
                    s.settimeout(self.args.timeout)
                    s.connect((self.args.target, port))
                    try:
                        recv = s.recv(65535)
                    except socket.timeout:
                        recv = b''
                    self.out_q.put((port, recv))
                    if len(recv) > 0:
                        print("    * %s:%d - %s" % (self.args.target, port, str(recv[:20])+"..."))
                    else:
                        print("    * %s:%d" % (self.args.target, port))
                except (socket.timeout, ConnectionRefusedError, OSError):
                    pass
                s.close()
        except queue.Empty:
            pass

def run(args, data, reverse_handler):
    print("\033[1;34m[*]\033[00m Begining Reconnaissance...")
    q1 = queue.Queue()
    q2 = queue.Queue()
    ports = list(range(1, 9999))
    random.shuffle(ports)
    for port in ports:
        q1.put(port)
    threads = []
    for i in range(args.threads):
        scanner = Scanner(args, q1, q2)
        scanner.start()
        threads.append(scanner)
    for thread in threads:
        thread.join()
    try:
        while True:
            port, recv = q2.get(0)
            data['services'].append((port, recv))
    except queue.Empty:
        pass
    return data

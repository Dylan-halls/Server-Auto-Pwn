#!/usr/bin/env python3

import base64

def encoder(data):
    data = base64.b64encode(bytes(str(data).encode('utf-8')))
    return "bash -c \"$(echo '%s' | base64 -d)\" &" % (data.decode('utf-8'))

data = input()

#change recursion for real payload
for i in range(0, 1):
    data = encoder(data)
print("\n\n"+data)

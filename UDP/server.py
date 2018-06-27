#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

from socket import *

server = socket(AF_INET, SOCK_DGRAM)
server.bind(('127.0.0.1', 8080))

while True:
    data, client_addr =server.recvfrom(1024)   #针对UDP
    print(data)
    server.sendto(data.upper(), client_addr)

server.close()


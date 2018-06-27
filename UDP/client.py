#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

from socket import *

client = socket(AF_INET, SOCK_DGRAM)



while True:
    msg = input('>>:').strip()
    client.sendto(msg.encode('utf-8'), ('127.0.0.1', 8080))
    data,server_addr = client.recvfrom(1024)
    print(data,server_addr)
client.close()
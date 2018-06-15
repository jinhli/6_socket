#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import socket
#1,实例化

phone  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#2.打电话
phone.connect(('127.0.0.1', 8080)) #0~65535, 0~1024 给操作系统用的
while True:
    msg = input('input your message>>:').strip()
    if not msg: continue
#
    phone.send(msg.encode('utf-8'))

    data = phone.recv(1024)
    print(data)

phone.close()
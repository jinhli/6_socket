#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import socket

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.connect(('127.0.0.1', 8080)) #0~65535, 0~1024 给操作系统用的

while True:
    #1.命令
    cmd = input('input your message>>:').strip()
    if not cmd: continue
    phone.send(cmd.encode('utf-8'))
    # obj = phone.recv(1024)  # 坑2
    # while len(obj) >1024:
    #     obj =

    print('stout 1--->', obj.decode('utf-8'))

phone.close(）
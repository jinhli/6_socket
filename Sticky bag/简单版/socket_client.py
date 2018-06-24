#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import socket
import struct

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.connect(('127.0.0.1', 8080)) #0~65535, 0~1024 给操作系统用的

while True:
    #1.命令
    cmd = input('input your message>>:').strip()
    if not cmd: continue
    phone.send(cmd.encode('utf-8'))
    #第一步，先拿到数据的长度
    obj = phone.recv(4)
    total_size = struct.unpack('i',obj)[0]

    #第二部：接收真实的数据
    recv_size = 0
    recv_data=b''
    while recv_size < total_size:
        res = phone.recv(1024)
        recv_data+=res
        recv_size+=len(res)

    print('stout 1--->', recv_data.decode('utf-8'))

phone.close()
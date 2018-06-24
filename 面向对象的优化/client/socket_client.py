#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import socket
import struct
import json
download_dir = r'/home/bonnie/python_learning/pycharm_project/6_socket/文件传输简单版本/client/download'
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.connect(('127.0.0.1', 8080)) #0~65535, 0~1024 给操作系统用的

while True:
    #1.发命令
    cmd = input('input your message>>:').strip()
    if not cmd: continue
    phone.send(cmd.encode('utf-8'))

    #以写的方式打开一个新文件，把收到的内容复印到文件

    #第一步，先拿到数据的长度
    obj = phone.recv(4)
    head_len = struct.unpack('i',obj)[0]
    data = phone.recv(head_len).decode('utf-8')
    header_dict = json.loads(data)
    total_size = header_dict['total_size']
    filename = cmd.split()[1]

    filename1 = r'%s/%s' %(download_dir,filename)
    #第二部：接收真实的数据
    with open(filename1,'wb') as f:
        recv_size = 0
        while recv_size < total_size:
            line = phone.recv(1024)
            f.write(line)
            recv_size+=len(line)
            print('总大小：%s 已下载大小：%s' %(total_size,recv_size) )
    

phone.close()
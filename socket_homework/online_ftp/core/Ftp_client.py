#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/26/18



import os
from sys import path as sys_path
sys_path.insert(0,os.path.dirname(os.getcwd()))

import socket
import subprocess
import struct
import json
from core.md5_server import *


class Ftp_client():
    def __init__(self, address='127.0.0.1', port=8080):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lip = address
        self.port = port
        self.client.connect((self.lip, self.port))

    def send_cmd(self):
        while True:
            # 1.命令
            cmd = input('input your message>>:').strip()
            if not cmd: continue
            self.client.send(cmd.encode('utf-8'))
            obj = self.client.recv(4)
            total_size = struct.unpack('i', obj)[0]

            # 第二部：接收真实的数据
            recv_size = 0
            recv_data = b''
            while recv_size < total_size:
                res = self.client.recv(1024)
                recv_data += res
                recv_size += len(res)

            print('stout 1--->', recv_data.decode('utf-8'))

    def login_server(self):  #发报头过去
        cmd = input('input your message>>:').strip()  # login name password
        if not cmd: continue
        cmd = cmd.split()
        header_dic = {
            "name": cmd[1],
            'password': cmd[2],
            "cmd": cmd[0]
        }
        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')
        self.server.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
        self.server.send(header_bytes)  # 再发报头，告诉客户端数据长度


ftp_client = Ftp_client()
ftp_client.send_cmd()
ftp_client.close()
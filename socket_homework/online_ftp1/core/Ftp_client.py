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
# from core.md5_server import *



class Ftp_client():
    def __init__(self, address='127.0.0.1', port=8080):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lip = address
        self.port = port
        self.client.connect((self.lip, self.port))

    def send_header(self, **kwargs):  # 报头发布信息，防止粘包
        """
        发送报头
        :param kwargs: 字典
        :return:
        """
        header_dic = {}
        for key, value in kwargs.items():
            header_dic[key] = value
        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')
        self.client.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
        self.client.send(header_bytes)

    def recv_header(self):
        """
             接收报头，并把报头内容转换成字典
             :return:
             """
        obj = self.client.recv(4)
        head_len = struct.unpack('i', obj)[0]
        data = self.client.recv(head_len).decode('utf-8')
        header_dict = json.loads(data)
        return header_dict

    def recv_data(self,header_dict):
        """
        处理收到到数据，主要是命令行返回的数据
        :param header_dict:
        :return:
        """
        total_size = header_dict['size']
        recv_size = 0
        recv_data = b''
        while recv_size < total_size:
            res = self.client.recv(1024)
            recv_data += res
            recv_size += len(res)

        print('stout 1--->', recv_data.decode('utf-8')) # 优化下 就可以仿照登陆用户的组目录显示 [bonnie@bonnie]>>

    def login_server(self):  #发报头过去
        while True:
            cmd = input('input your message>>:').strip()  # login name password
            if not cmd: continue
            cmd = cmd.split()
            self.send_header(name=cmd[1], password=cmd[2], cmd=cmd[0])
            header_dict = self.recv_header()
            self.recv_data(header_dict)






ftp_client = Ftp_client()
ftp_client.login_server()

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
import configparser
from conf import *



class Ftp_server():
    def __init__(self,localip='127.0.0.1',port=8080):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lip = localip
        self.port = port
        self.server.bind((self.lip, self.port))
        self.server.listen(5)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        conn, addr = self.server.accept()
    def handle_accept(self):
        """
        处理系统命令， 比如 cd ,ls
        :return:
        """

        while True:  # 通信循环
            try:
                cmd = self.conn.recv(1024)  # 单位是bytes 最大是1024
                if not cmd: break  # 如果客户端停止，服务端会一直死循环，需要用break退出
                obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                stdout = obj.stdout.read()
                stderr = obj.stderr.read()
                data_size = len(stdout) + len(stderr)
                header = struct.pack('i', data_size)
                self.conn.send(header)
                self.conn.send(stdout)
                self.conn.send(stderr)  #
            except ConnectionError:  # 使用windows
                break
        self.conn.close()  # 考虑应该放那里？

    def recv_cmd(self):
        obj = self.conn.recv(4)
        head_len = struct.unpack('i', obj)[0]
        data = self.conn.recv(head_len).decode('utf-8')
        header_dict = json.loads(data)
        if header_dict['cmd'] == 'login':
            name = header_dict['name']
            password = header_dict['password']
            return name, password
        if header_dict['cmd'] == 'get':
            pass
        elif header_dict['cmd'] == 'upload':
            pass
        elif header_dict['cmd'] == 'q':
            exit()
        else:
            pass    #执行命令操作

    def login_auth(name, password):
        config = configparser.ConfigParser()  # 实例化一个对象
        config.read(account)  # 打开文件 account.ini，保存了用户信息
        res = config.sections()  # 获得section列表
        if name in res:
            if config[name]['password'] == password:
                home_dir = config[name]['home']
                msg = 'login successfully'
                return home_dir  # 登陆成功，直接cd 到home目录
            else:
                msg= 'password is not correct'
        else:
            msg = 'there is no the account here'
        return msg





ftp_server = Ftp_server()
ftp_server.handle_accept()
ftp_server.close()




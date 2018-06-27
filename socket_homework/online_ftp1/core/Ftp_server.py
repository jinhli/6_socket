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
import configparser
from conf import *


class Ftp_server():
    def __init__(self, localip='127.0.0.1', port=8080):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lip = localip
        self.port = port
        self.server.bind((self.lip, self.port))
        self.server.listen(5)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        conn, addr = self.server.accept()

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
        self.conn.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
        self.conn.send(header_bytes)

    def recv_header(self):
        """
        接收报头，并把报头内容转换成字典
        :return:
        """
        obj = self.conn.recv(4)
        head_len = struct.unpack('i', obj)[0]
        data = self.conn.recv(head_len).decode('utf-8')
        header_dict = json.loads(data)
        return header_dict

    def send_message(self, msg):
        """
        处理简单的信息反馈
        :param msg:
        :return:
        """
        self.send_header(self, size=len(msg))
        self.conn.send(msg)

    @staticmethod
    def login_verify(name, password):
        """
        从account里读取文件内容，并进行验证
        :param name:
        :param password:
        :return:
        """
        config = configparser.ConfigParser()  # 实例化一个对象
        config.read(account)  # 打开文件 account.ini，保存了用户信息
        res = config.sections()  # 获得section列表
        if name in res:
            if config[name]['password'] == password:
                home_dir = config[name]['home']
                msg = 'login successfully'
                return msg, home_dir  # 登陆成功，直接cd 到home目录
            else:
                msg = 'password is not correct'
        else:
            msg = 'there is no the account here'
        return msg

    def handle_cmd(self):
        """
        处理系统命令， 比如 cd ,ls
        :return:
        """
        while True:  # 通信循环
            try:
                cmd = self.conn.recv(1024)  # 单位是bytes 最大是1024
                if not cmd:
                    break  # 如果客户端停止，服务端会一直死循环，需要用break退出
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


ftp_server = Ftp_server()
header_dict = ftp_server.recv_header()
if header_dict['cmd'] == 'login':
    name = header_dict['name']
    password = header_dict['password']
    msg, home_dir = Ftp_server.login_verify(name, password)
    if home_dir:
        Ftp_server.send_message(msg)
        # 调用 cmd 处理命令，cd 到home 目录
    else:
        Ftp_server.send_message(msg)

if header_dict['cmd'] == 'get':
    pass
elif header_dict['cmd'] == 'upload':
    pass
elif header_dict['cmd'] == 'q':
    exit()
else:
    pass    #执行命令操作

ftp_server.close()





# ftp_server = Ftp_server()
# ftp_server.recv_cmd()





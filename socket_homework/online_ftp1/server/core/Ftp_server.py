#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/26/18


from os import path, getcwd
from sys import path as sys_path
sys_path.insert(0,path.dirname(getcwd()))


import socket
import subprocess
import struct
import json
import hashlib
import configparser
from conf import setting
from conf.md5_server import get_md5

class Ftp_server():
    STATUS_CODE ={
        200:'Account authentication',
        201:'wrong username or password',
        301: 'File does not exist',
        300:'File exists',
        400:'upload successfully',
        401:'upload file failed'

    }
    def __init__(self, management_instance):
        self.management_instance = management_instance
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((setting.ADDR,setting.PORT))
        self.server.listen(setting.MAX_SOCKET_LISTEN)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.accounts = self.load_accouts()

    def start_server(self):
        """
        启动ftp server
        :return:
        """
        print('start ftp server on %s:%s'.center(50, '-') %(setting.ADDR, setting.PORT))
        while True:
            self.conn, self.addr = self.server.accept()
            print('got a new connection from %s......' %(self.addr,))
            self.handle()

    def handle(self):
        """
        处理与用户的所有指令交互
        :return:
        """
        while True:
            data = self.recv_header()  # 传过来的数据
            print('--->',data)
            if not data:
                print('connection %s is lost ....' % (self.addr,))
                del self.addr
                break
            else:
                action_type = data.get('action_type')
                if action_type:
                    if hasattr(self, '_%s' % action_type):
                        func = getattr(self,'_%s' % action_type)
                        func(data)
                else:
                    print('invalid command')


    def send_message(self,status_code, *args, **kwargs):  # 报头发布信息，防止粘包
        """
        发送报头
        :param kwargs: 字典
        :return:
        """

        header_dic = kwargs
        header_dic['status_code'] = status_code
        header_dic['status_msg'] = self.STATUS_CODE[status_code]
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
        if obj:
            head_len = struct.unpack('i', obj)[0]
            data = self.conn.recv(head_len).decode('utf-8')
            header_dict = json.loads(data)
            return header_dict
        else:
            return False



    def load_accouts(self):
        """
        加载所有的账号信息
        :return:
        """
        config = configparser.ConfigParser()  # 实例化一个对象
        config.read(setting.account)  # 打开文件 account.ini，保存了用户信息
        return config # 获得section列表

    def authenticate(self,username, password):
        """
        用户认证方法
        :param username:
        :param password:
        :return:
        """
        if username in self.accounts:
            _password = self.accounts[username]['password']
            md5_obj = hashlib.md5()
            md5_obj.update(password.encode())
            md5_password = md5_obj.hexdigest()
            print('password', _password, md5_password)
            if md5_password == _password:
                home_dir = self.accounts[username]['home']
                home_dir = '%s/%s' % (setting.HOME_DIR, home_dir)
                # # msg = 'login successfully'
                # # cmd = 'ls %s' % home_dir
                # # self.handle_cmd(cmd)
                print(home_dir)
                return True
            else:
                msg = 'password is not correct'
                return False
        else:
            msg = 'there is no the account here'
            return False
        # self.send_message(msg)

    def _auth(self, data):  #
        """
        从account里读取文件内容，并进行验证
        :param name:
        :param password:
        :return:
        """
        if self.authenticate(data.get('username'),data.get('password')):

            print('auth pass')
            self.send_message(200)

        else:
            print('auth fail')
            self.send_message(201)

    def _get(self, data):
        """
        下载到客户端
        :param data:
        报头
        {
        status_code:
        status_msg:
        md5: md5 checksum
        size: 文件大小
        }
        :return:
        """
        _filename = data.get('filename')
        home_dir = r'%s/%s' %(setting.HOME_DIR, self.accounts.get('home'))
        filename_path = r'%s/%s' % (home_dir, _filename)
        if path.exists(filename_path):
            file_md5 = get_md5()
            file_size = path.getsize(filename_path)
            self.send_message(300,md5=file_md5,size=file_size)
            with open(filename_path, 'rb') as f:
                for line in f:
                    self.conn.send(line)
        else:
            self.send_message(301)


    def _put(self,data):
        """
              从客户端上传文件
              :return: MD5
              """
        _filename = data.get('filename')
        home_dir = r'%s/%s' % (setting.HOME_DIR, self.accounts.get('home'))
        filename_path = r'%s/%s' % (home_dir, _filename)
        _size = data.get('size')
        _md5 = data.get('md5')
        if path.exists(filename_path):
            filename2 = filename_path + '.bak'
            self.write_file(filename2, _size)
            file_md5 = get_md5
            if _md5 == file_md5:
                # 判断Md5
        else:
            self.write_file(filename_path, _size)

            #MD5 判断cd


    def write_file(self,filename, total_size):
        """
        写文件
        :param filename:
        :return:
        """
        with open(filename, 'wb') as f:
            recv_size = 0
            while recv_size < total_size:
                line = self.conn.recv(1024)
                f.write(line)
                recv_size += len(line)
                print('总大小：%s 已下载大小：%s' % (total_size, recv_size))
    def handle_cmd(self,cmd):
        """
        处理系统命令， 比如 cd ,ls
        :return:
        """
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = obj.stdout.read()
        stderr = obj.stderr.read()
        data_size = len(stdout) + len(stderr)
        self.send_header(size=data_size)
        self.conn.send(stdout)
        self.conn.send(stderr)

#
# def main():
#     ftp_server = Ftp_server()
#     while True:
#         header_dict = ftp_server.recv_header()
#         if header_dict['cmd'] == 'login':
#             name = header_dict['name']
#             password = header_dict['password']
#             ftp_server.login_verify(name, password)
#         if header_dict['cmd'] == 'get':
#             pass
#         elif header_dict['cmd'] == 'upload':
#             pass
#         elif header_dict['cmd'] == 'q':
#             exit()
#         else:
#             pass    #执行命令操作  res = subprocess.getstatusoutput('cd /home/bonnie/') ,res[0] = 0 则说明是一个命令行，返回命令行的结果lu
#





#
#
# main()


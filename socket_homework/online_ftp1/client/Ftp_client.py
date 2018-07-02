#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/26/18



import os
from sys import path as sys_path
sys_path.insert(0,os.path.dirname(os.getcwd()))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #整个程序的主目录
HOME_DIR = r'%s/client/home/' % BASE_DIR
import socket
import struct
import json
import optparse
from client.md5_client import *

""""
python ftp_client -h ip -P 8080 """ # 运行格式


class Ftp_client():
    def __init__(self):
        parse = optparse.OptionParser()
        parse.add_option('-s','--server', dest='server',help='ftp server ip_addr')
        parse.add_option('-P', '--port', type='int', dest='port', help='ftp server port')
        parse.add_option('-u', '--username', dest='username', help='username info')
        parse.add_option('-p', '--password', dest='password', help='password')
        self.options, self.args = parse.parse_args()
        # print(self.options,self.args)
        self.username = None

    def argv_verification(self):
        if not self.options.server or not self.options.port:
            exit('Error: must supply server and port parameters')

    def make_connection(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.options.server, self.options.port))

    def auth(self):
        count = 0
        while count < 3:
            username = input('username:').strip()
            if not username:continue
            password = input('password:').strip()
            # cmd = {
            #      'action_type': 'auth',
            #      'username': username,
            #      'password': password
            #  }
            self.send_header(username=username, password=password, action_type='auth')
            response = self.recv_message()
            if response.get('status_code') == 200:
                self.username = username
                return True
            else:
                print(response.get('status_msg'))
                count +=1


    def interactive(self):
        """处理与ftpserver的所有交互"""

        if self.auth():
            while True:
                user_input = input('[%s]>>:' % self.username).strip()
                if not user_input: continue
                cmd_list = user_input.split()
                if hasattr(self, '_%s' % cmd_list[0]):
                    func = getattr(self, '_%s' % cmd_list[0])
                    func(cmd_list[1:])


        else:
            print('auth fail')

    def parameter_check(self,args, min_args=None, max_args=None, exact_args=None ):
        """
        参数合法性检查
        :param args:
        :param min_args:
        :param max_args:
        :param exact_args:
        :return:
        """
        if min_args:
            if len(args) < min_args:
                print('require at least %s parameters but  %s received' %(min_args, len(args)))
                return False
        if max_args:
            if len(args) < max_args:
                print('require at most %s parameters but  %s received' % (min_args, len(args)))
                return False
        if exact_args:
            if exact_args != len(args):
                print('require % parameters but %s received' % (exact_args, len(args)))
                return False
        return True


    def _get(self,cmd_args):
        """
        下载文件到客户端
        :return: MD5
        """
        if self.parameter_check(cmd_args, exact_args=1):
            filename = cmd_args[0]
            action_type = 'get'
            self.send_header(action_type, filename=filename,)  # 把要下载的命令和文件发送到服务器
            response = self.recv_message()  # 接收服务器发过来的信息
            if response.get('status_code') == 300:  # 接收到状态码 300， 表明文件存在
                self.write_file(response, filename)
                original_md5 = response.get('md5')
                # home_dir = '%s%s' % (HOME_DIR, filename)  # 绝对路径
                self.verify_md5(filename, original_md5)

            else:
                print(response.get('status_msg'))

            # self.print_data()  #

    def _put(self,cmd_args):
        """
        上传文件到客户端
        :return:
        """

        if self.parameter_check(cmd_args, min_args=1):
            action_type = 'put'
            _filename = cmd_args[0]
            filename_path = _filename
            # filename_path = r'%s%s' % (HOME_DIR, _filename)
            if os.path.exists(filename_path):   # 扩展 如果输入的是个绝对路径，要取出文件名
                file_md5 = get_md5(filename_path)
                file_size = os.path.getsize(filename_path)
                self.send_header(action_type, filename=_filename, md5=file_md5, size=file_size)
                with open(filename_path, 'rb') as f:
                    for line in f:
                        self.client.send(line)
                response = self.recv_message()  # 接受上传成功的消息
                if response.get('status_code') == 400:  # 接受状态码400，表示上传成功
                    print(response.get('status_msg'))
                else:
                    print(response.get('status_msg'))
            else:
                print('%s does not exist, please check %s file_path is right' % (_filename,filename_path))

    def send_header(self, action_type, **kwargs):  # 报头发布信息，防止粘包
        """
        发送报头
        :param kwargs: 字典
        :return:
        """
        header_dic = {'action_type':action_type
        }
        header_dic.update(kwargs)
        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')
        self.client.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
        self.client.send(header_bytes)

    def recv_message(self):
        """
             接收报头，并把报头内容转换成字典
             :return:
             """
        obj = self.client.recv(4)
        head_len = struct.unpack('i', obj)[0]
        data = self.client.recv(head_len).decode('utf-8')
        header_dict = json.loads(data)
        return header_dict

    def write_file(self, header_dict, filename):
        """
        保存文件
        :param filename:
        :return:
        """

        total_size = header_dict.get('size')
        with open(filename, 'wb') as f:
            recv_size = 0
            while recv_size < total_size:
                line = self.client.recv(1024)
                f.write(line)
                recv_size += len(line)
                print('总大小：%s 已下载大小：%s' % (total_size, recv_size))

    def print_data(self, header_dict):
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

        print('[%s]>>: % self.username>>', '\n'+ recv_data.decode('utf-8')) # 优化下 就可以仿照登陆用户的组目录显示 [bonnie@bonnie]>>

    def verify_md5(self, file_path, original_md5):
        """
        上传文件MD5 验证
        :param file_path:
        :param original_md5:  # 客户端传过来的MD5
        :return:
        """
        new_md5 = get_md5(file_path)
        print(new_md5, original_md5)
        if new_md5 == original_md5:
            print('md5 check successfully for %s' % file_path)  # MD5 检测成功

        else:
            print('md5 check failed for %s' % file_path) # MD5 检测失败





if __name__ == '__main__':

    ftp_client = Ftp_client()
    ftp_client.make_connection()
    ftp_client.interactive()




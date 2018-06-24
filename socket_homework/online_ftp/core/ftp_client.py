#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/23/18

import os
from sys import path as sys_path
sys_path.insert(0,os.path.dirname(os.getcwd()))
import socket
import struct
import json
import time
from core.md5_client import *


client_dir = r'/home/bonnie/python_learning/pycharm_project/6_socket/socket_homework/online_ftp/conf/client/lili'
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.connect(('127.0.0.1', 8080))  # 0~65535, 0~1024 给操作系统用的


def write_file(filename,total_size):
    """

    :param filename:
    :return:
    """
    with open(filename, 'wb') as f:
        recv_size = 0
        while recv_size < total_size:
            line = phone.recv(1024)
            f.write(line)
            recv_size += len(line)
            print('总大小：%s 已下载大小：%s' % (total_size, recv_size))


def recv_handle():
    obj = phone.recv(4)
    head_len = struct.unpack('i', obj)[0]
    data = phone.recv(head_len).decode('utf-8')
    header_dict = json.loads(data)
    total_size = header_dict['total_size']
    return total_size


def downLoadfromServer(cmd):
    """

    :return: MD5
    """
    obj = phone.recv(4)
    head_len = struct.unpack('i', obj)[0]
    data = phone.recv(head_len).decode('utf-8')
    header_dict = json.loads(data)
    total_size = header_dict['total_size']
    filename = cmd[1]
    for key,val in header_dict.items():
        print(key,val)
    filename1 = r'%s/%s' % (client_dir, filename)
    # 第二部：接收真实的数据
    if os.path.exists(filename1):
        answer = input('%s is exits,do you want to override it,"yes", or "no" ? >>:' % filename1)
        if answer == 'yes':
           write_file(filename1,total_size)
        else:
            filename2 = filename1+'.bak'
            write_file(filename2, total_size)
    else:
        write_file(filename1, total_size)
    return header_dict['md5'],filename1



def uploadToServer(cmd):
    """

    :return:
    """
    filename = cmd[1]
    filename_path = r'%s/%s' % (client_dir, filename)  # file path in the server
    md5 = get_md5(filename_path)
    header_dic = {
        "filename": filename,
        'md5': md5,
        "total_size": os.path.getsize(filename_path)
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')
    phone.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
    phone.send(header_bytes)  # 再发报头，告诉客户端数据长度
    with open(filename_path, 'rb') as f:
        for line in f:
            phone.send(line)

while True:
    # 1.发命令
    cmd = input('input your message>>:').strip()
    if not cmd: continue
    phone.send(cmd.encode('utf-8'))
    cmd = cmd.split()
    if cmd[0] == 'get':
        original_md5,file_path = downLoadfromServer()
        new_md5 = get_md5(file_path)
        if new_md5 == original_md5:
            print('The file you download is the same as it in the server')
        else:
            print('The file has been changed during the trasfer')
    if cmd[0] == 'upload':
        uploadToServer(cmd)
        upload_status = False
        while not upload_status:
            total_size = recv_handle()
            msg = phone.recv(total_size)
            if msg.decode('utf-8') == 'done':
                upload_status = True
            else:
                print(msg.decode('utf-8'))
    if cmd[0] == 'q':
        exit()



phone.close()

# file_path = r'/home/bonnie/python_learning/pycharm_project/6_socket/socket_homework/online_ftp/conf/client/lili/1.jpeg'
# new_md5 = get_md5(file_path)
# print(type(new_md5))
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/23/18

import os
from sys import path as sys_path
sys_path.insert(0,os.path.dirname(os.getcwd()))

import socket
import subprocess
import struct
import json
from core.md5_server import *

server_dir = r'/home/bonnie/python_learning/pycharm_project/6_socket/socket_homework/online_ftp/conf/server/lili'
phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
phone.bind(('127.0.0.1', 8080))  # 0~65535, 0~1024 给操作系统用的
phone.listen(5)  # 正常写配置文件， 挂起5次



def write_file(filename,total_size):
    """

    :param filename:
    :return:
    """
    with open(filename, 'wb') as f:
        recv_size = 0
        while recv_size < total_size:
            line = conn.recv(1024)
            f.write(line)
            recv_size += len(line)
            print('总大小：%s 已下载大小：%s' % (total_size, recv_size))


def message_handle(msg):  # 报头发布信息，防止粘包

    header_dic = {
            "msg": msg,
            "total_size": len(msg)
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')
    conn.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
    conn.send(header_bytes)
    conn.send(msg.encode('utf-8'))

def uploadFromClient(cmd):
    """

    :param cmd:   # "upload file"  from client
    :return:
    """
    obj = conn.recv(4)
    head_len = struct.unpack('i', obj)[0]
    print(head_len)
    data = conn.recv(head_len).decode('utf-8')
    header_dict = json.loads(data)
    total_size = header_dict['total_size']
    filename = cmd[1]
    for key, val in header_dict.items():
        print(key, val)
    filename1 = r'%s/%s' % (server_dir, filename)
    # 第二部：接收真实的数据
    if os.path.exists(filename1):
        answer = '%s is exits,and the new uploading will save as *.bak' % filename1
        message_handle(answer)

        filename2 = filename1 + '.bak'
        write_file(filename2, total_size)
    else:
        write_file(filename1, total_size)
    return header_dict['md5'], filename1


def donwloadToClient(cmd):
    """

    :param cmd:  # "get file" from client
    :return:
    """
    filename = cmd[1]
    filename_path = r'%s/%s' % (server_dir, filename)  # file path in the server
    md5 = get_md5(filename_path)
    print(md5)
    header_dic = {
        "filename": filename,
        'md5': md5,
        "total_size": os.path.getsize(filename_path)
    }
    header_json = json.dumps(header_dic)
    header_bytes = header_json.encode('utf-8')
    conn.send(struct.pack('i', len(header_bytes)))  # 发一个报头长度
    conn.send(header_bytes)  # 再发报头，告诉客户端数据长度
    with open(filename_path, 'rb') as f:
        for line in f:
            conn.send(line)


while True:
    conn, client_addr = phone.accept()
    while True:  # 通信循环
        try:  # 收到命令
            cmd = conn.recv(1024)  # 单位是bytes 最大是1024 # b'get a.txt'
            if not cmd: break   # 如果客户端停止，服务端会一直死循环，需要用break退出
            cmd = cmd.decode('utf-8').split()
            if cmd[0] == 'get':
                donwloadToClient(cmd)
            if cmd[0] == 'upload':
                original_md5, file_path = uploadFromClient(cmd)
                new_md5 = get_md5(file_path)
                if new_md5 == original_md5:
                    msg = 'The file you download is the same as it in the server'
                else:
                    msg = 'The file has been changed during the trasfer'
                message_handle(msg)
                status = 'done'  # 结束标志
                message_handle(status)
        except ConnectionError:  #使用windows
            break


#
    conn.close()
phone.close()


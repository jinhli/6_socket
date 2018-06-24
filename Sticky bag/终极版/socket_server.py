#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import socket
import os
import subprocess
import struct
import json
import os
share_dir=r'/home/bonnie/python_learning/pycharm_project/6_socket/文件传输简单版本/server/share'
# res = struct.pack('i',128)
# print(res,type(res),len(res))
# obj =struct.unpack('i',res) #还有一个模式，“l”
# print(obj[0])



#1,实例化

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#.
phone.bind(('127.0.0.1', 8080))  #0~65535, 0~1024 给操作系统用的
#3.
phone.listen(5) # 正常写配置文件， 挂起5次

#4
while True:
    conn, client_addr = phone.accept()

    while True:  #通信循环
        try:
        #收到命令
            cmd = conn.recv(1024)  # 单位是bytes 最大是1024 # b'get a.txt'
            if not cmd: break   #如果客户端停止，服务端会一直死循环，需要用break退出
        #解析命令
            filename = cmd[1]
            filename1 = r'%s/%s' %(share_dir,filename)
            print(filename1)
        #以读的方式打开文件，读取内容发送到客户端


        #制作固定长度的报头
            header_dic = {
                "filename":filename1,
                'md5':'xxx',
                "total_size":os.path.getsize(filename1)
            }
            header_json= json.dumps(header_dic)

            header_bytes = header_json.encode('utf-8')
            print(len(header_bytes))

            #把报头发给客户端
            #第一步：把数据的长度发给客户端
            conn.send(struct.pack('i',len(header_bytes)))  #发一个报头长度
            conn.send(header_bytes) #再发报头，告诉客户端数据长度
            with open('%s/%s' %(share_dir,filename1),'rb') as f:
                for line in f:
                    conn.send(line)

        except ConnectionError:  #使用windows
            break


#
    conn.close()
phone.close()



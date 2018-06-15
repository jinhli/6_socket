#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import socket



#1,实例化

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#2.
phone.bind(('127.0.0.1', 8080))  #0~65535, 0~1024 给操作系统用的
#3.
phone.listen(5) # 正常写配置文件， 挂起5次

#4
print("start >>>>>>")
conn, client_addr = phone.accept()
print('++++++>')

#

#
while True:  #通信循环
    try:
        data = conn.recv(1024)  # 单位是bytes 最大是1024
        if not data: break   #如果客户端停止，服务端会一直死循环，需要用break退出
        print('客户端数据', data)
        conn.send(data.upper())
    except ConnectionError:  #使用windows
        break


#
conn.close()
phone.close()

#



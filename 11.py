#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/15/18
#
# def send_header(**kwargs):  # 报头发布信息，防止粘包
#     header_dic = {}
#     for key, value in kwargs.items():
#         header_dic[key] = value
#     return header_dic
#
#
#
# res = send_header(filename ='bonnie', size=10)
#
#
import configparser

config = configparser.ConfigParser()  # 实例化一个对象
config.read(r'/home/bonnie/python_learning/pycharm_project/6_socket/socket_homework/online_ftp1/conf/account.ini')  # 打开文件 account.ini，保存了用户信息
res = config.sections()  # 获得section列表
print(res)
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/23/2018

from os import getcwd,path
from sys import path as sys_path
sys_path.insert(0,path.dirname(getcwd()))

from conf.setting import account, BASE_DIR
import configparser


config = configparser.ConfigParser()  # 实例化一个对象
config.read(account)  # 打开文件
res =config.sections()  # 获得section列表

home_path = '%s/%s' %(BASE_DIR,config['lili']['home'])
print(home_path)  # 通过列表字典格式获取

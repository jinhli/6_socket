#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/23/18

from os import getcwd,path
from sys import path as sys_path
sys_path.insert(0,path.dirname(getcwd()))

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__))) #整个程序的主目录

account = r'%s/conf/account.ini' %BASE_DIR

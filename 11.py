#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/15/18

def send_header(**kwargs):  # 报头发布信息，防止粘包
    header_dic = {}
    for key, value in kwargs.items():
        header_dic[key] = value
    return header_dic



res = send_header(filename ='bonnie', size=10)



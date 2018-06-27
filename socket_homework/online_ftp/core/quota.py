#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/23/18

import os
import sys
rootdir=r'/home/bonnie/python_learning/'  # 到时候换成家目录 ？


def verify_quota():
    for dirname in  os.listdir(rootdir):  # 获取二级目录所有文件夹与文件
        Dir = os.path.join(rootdir, dirname)    # 路径补齐
        count = 0
        if (os.path.isdir(Dir)):           # 判断是否为目录
            for r, ds, files in os.walk(Dir):  # 遍历目录下所有文件根，目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名称】
                for file in files:      # 遍历所有文件
                    size = os.path.getsize(os.path.join(r, file))  # 获取文件大小
                    count += size

    count = count/ 1024.0 / 1024.0/1024.0  # 加入判断

    print('%s total size is %s' %(rootdir,'%.2f' % (count / 1024.0 / 1024.0/1024.0) + 'GB'))




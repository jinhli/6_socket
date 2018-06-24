#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/23/18


from os import getcwd, path
from sys import path as sys_path
sys_path.insert(0, path.dirname(getcwd()))
from core import main

if __name__ == '__main__':
    main.main()




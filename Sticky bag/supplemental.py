#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__="Bonnie"
# Date:2018/3/16

import os
import subprocess
#ls
#ifconfig
#ps aux

os.system('ls /etc')
obj = subprocess.Popen('xxls /', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(obj)
print('stout 1--->', obj.stdout.read().decode('utf-8'))

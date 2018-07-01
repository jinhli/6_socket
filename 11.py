#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Bonnie Li"
# Email: bonnie922713@126.com
# Date: 6/15/18

# import optparse
# # import socket
# #
# # class FtpClient():
# #     def __init__(self):
# #         parse = optparse.OptionParser()
# #         parse.add_option('-s','--server', dest='server',help='ftp server ip_addr')
# #         parse.add_option('-P', '--port', type='int', dest='port', help='ftp server port')
# #         parse.add_option('-u', '--username', dest='username', help='username info')
# #         parse.add_option('-p', '--password', dest='password', help='password')
# #         self.options, self.args = parse.parse_args()
# #         print(self.options,self.args)
# #
# #     def argv_verification(self):
# #         if not self.options.server or not self.options.port:
# #             exit('Error: must supply server and port parameters')
# #
# #     def make_connection(self):
# #         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #         self.client.connect((self.options.server,self.options.port))
# #
# #     def auth(self):
# #         count = 0
# #         while count < 3:
# #             username = input('username:').strip()
# #             if not username:continue
# #             password = input('password:').strip()
# #
# #     def interactive(self):
# #         """处理与ftpserver的所有交互"""
# #         if self.auth():
# #             pass
# #
# #
# #
# #
# #
# #
# #
# #
# # if __name__== '__main__':
# #     client = FtpClient()
# #     client.interactive() #交互

username = 'bonnie'
password = '13334'
cmd = {
    'action_type': 'auth',
    'username': username,
    'password': password
}


def send_header(**kwargs):  # 报头发布信息，防止粘包
    """
    发送报头
    :param kwargs: 字典
    :return:
    """
    header_dic = kwargs
    print(header_dic)

send_header(username=username, password=password, action_type='auth')

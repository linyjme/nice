# -*- coding:utf-8 -*-
"""
    chatroom project for server
    env:python3.5
    exc:for socket and Procrss 
"""
from socket import *
import sys, os
from threading import Thread
from config import *
from sql_db import *
from response import *
import json
import pymysql

# 服务器地址
ADDR = (SERVER_IP, PORT)

# 处理僵尸进程
# signal.signal(signal.SIGCHLD, signal.SIG_IGN)


# 初始化全局变量
# gl._init()

class Server(object):
    def __init__(self):
        self.address = ADDR
        self.create_socket()
        self.bind()
        # 运行main
        self.main()

    def create_socket(self):
        """
            创建tcp套接字
            设置端口复用
        """
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        """
            绑定地址
        """
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    def main(self):
        """
            启动服务
            数据库初始化
        """
        # 数据库初始化
        sql = MySql()
        sql.sql_init()
        self.sockfd.listen(5)
        print("Listen the port %d..." % self.port)
        while True:
            try:
                c, addr = self.sockfd.accept()
                print("Connect from ", addr)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit("服务器退出")
            except Exception as e:
                print(e)
                continue
            # 使用多线程
            client = Thread(target=do_request, args=(c, addr))
            client.setDaemon(True)
            client.start()

def do_request(c, addr):
    """
        服务端接收请求处理
    """
    # 实例化响应对象
    re = Response()
    while True:
        try:
            data = c.recv(4096).decode()
        except Exception as e:
            re.do_user_exit(c)
            return
        if not data:
            re.do_user_exit(c)
            return
        request = json.loads(data)
        # 区分请求类型
        if request['style'] == 'Q':
            # 处理用户退出
            re.do_user_exit(c)
            return
        elif request['style'] == 'L':
            # 登录请求
            re.do_login(c, request)
        elif request['style'] == 'R':
            # 注册请求
            re.do_register(c, request)
        elif request['style'] == 'S':
            # 登录后给客户端的初始化
            re.do_load_friend_list(c, request)
        elif request['style'] == 'A':
            # 处理登录后的离线消息跟加好友的消息
            re.do_off_line_msg(c, request)
        elif request['style'] == 'F':
            # 添加好友请求
            re.do_joinfriend(c, request)
        elif request['style'] == 'D':
            # 处理好友请求
            re.do_friends_reply(c, request)
        elif request['style'] == 'C':
            # 创建群聊房间
            re.do_create_room(c, request)
        elif request['style'] == 'N':
            # 私聊
            re.do_priv_chat(c, request)
        elif request['style'] == 'M':
            # 群聊
            re.do_group_chat(c, request)
        elif request['style'] == 'J':
            # 加群
            re.do_add_room(c,request)


if __name__ == '__main__':
    run = Server()



    # 使用多进程
    # client = Process(target = do_request,args =(c,addr))
    # client.daemon = True
    # client.start()

    # 使用多线程
    # client = Thread(target= do_request,args=(c,addr))
    # client.setDaemon(True)
    # client.start()

    # 创建子进程
    # pid = os.fork()
    # if pid == 0:
    #     self.sockfd.close()
    #     # 处理客户端请求
    #     do_request(c,addr)
    #     sys.exit()
    # else:
    #     c.close()

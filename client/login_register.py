# -*- coding:utf-8 -*-
"""
    chatroom project for client
    env:python3.5
    exc:for socket and Procrss and Thread
"""
from socket import *
from threading import Thread
from config import *
import sys
import re
import json
# import gevent
import time


class Client(object):
    """
    创建应用端类
    """

    def __init__(self):
        self.create_socket()
        self.__connect()

    def create_socket(self):
        self.sockfd = socket(AF_INET, SOCK_STREAM)

    def __connect(self):
        try:
            self.sockfd.connect(("176.140.7.173",8888))
        except Exception:
            sys.exit("网络异常,请检查后启动")

    def send(self,value):
        self.sockfd.send(value)

    def recv(self, number):
        return self.sockfd.recv(number)



class ClientManager():
    """
    实现client功能类
    """

    def __init__(self):
        self.clientor = Client()
        # self.clientor.start()

    def is_mobile(self, value):
        """
        we could judge that the value is a
        cell phone number or not
        :param value: argument
        :return: is for True/not for False
        """
        if not re.search("^1[0-9]{10}$", value):
            return False
        return True

    def is_email(self, value):
        """
        we could judge that the value is an
        email address or not
        :param value: argument
        :return: is for True/not for False
        """
        if not re.search("\w+([-+.]\w+)*@\w+([-.]\w+)*\.[a-z]{2,3}]", value):
            return False
        return True

    def is_password(self, value):
        """
        we could ues this method to judge the correct password
        :param value: your password
        :return: match for True else for False
        """
        if not re.search(r"\b\w{6,20}\b", value):
            return False
        return True

    def register(self,uid, upwd, upwd1, uname):
        """
        注册方法,可以判定账号,密码,昵称格式,并将其发送给服务端,
        接收服务端返回信息进行判定下步操作
        :param uid: 账号
        :param upwd: 密码
        :param upwd1: 重复输入密码
        :param uname: 昵称
        :return: 返回注册结果信息
        """
        if (" " in upwd) or (" " in uid):
            return "账号或密码不能有空格"
        if not (self.is_mobile(uid) or self.is_email(uid)):
            return "账号格式不对,请重新输入"
        if not self.is_password(upwd):
            return "密码格式不正确"
        if upwd != upwd1:
            return "两次输入密码不一致"

        data = {"style":"R", "uid":uid, "uname":uname, "upwd":upwd}
        print(data)
        request = json.dumps(data).encode()
        self.clientor.send(request)
        print("已发送")
        data = self.clientor.recv(128).decode()
        print(data)
        if data == "OK":
            # 注册结束后跳转登录界面还是直接进入交互界面
            return "注册成功"
        else:
            return data

    def login(self, uid, upwd):
        if (" " in upwd) or (" " in uid):
            return False
        if not (self.is_mobile(uid) or self.is_email(uid)):
            return False
        if not self.is_password(upwd):
            return False

        data = {"style":"L", "uid":uid, "upwd":upwd}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        msg = self.clientor.recv(128).decode()
        if msg == "OK":
            # 此时应该跳转好友界面
            return True
        else:
            # 验证不通过,返回登录界面
            return False

    def get_friends(self,uid):
        data = {"style":"S", "uid":uid}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        time.sleep(0.1)
        msg = json.loads(self.clientor.recv(2048).decode())
        if not msg:
            return None
        return msg

#
if __name__ == '__main__':
    user = ClientManager()
    user.register("12311111111", "123456", "123456", "123")




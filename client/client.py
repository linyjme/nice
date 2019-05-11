# -*- coding:utf-8 -*-
"""
    chatroom project for client
    env:python3.5
    exc:for socket and Procrss and Thread
"""
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
        return self.recv(number)


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
        while True:

            if (" " in upwd) or (" " in uid):
                print("账号或密码不能有空格")
                continue
            if not (self.is_mobile(uid) or self.is_email(uid)):
                print("账号格式不对,请重新输入")
                continue
            if not self.is_password(upwd):
                print("密码格式不正确")
            if upwd != upwd1:
                print("两次输入密码不一致")
                continue

            data = {"style":"R", "uid":uid, "uname":uname, "upwd":upwd}
            request = json.dumps(data).encode()
            self.clientor.send(request)
            data = self.clientor.recv(128).decode()
            if data == "OK":
                # 注册结束后跳转登录界面还是直接进入交互界面
                self.login(uid, uname)
            else:
                print(data)
                continue

    def login(self, uid, upwd):
        while True:
            if (" " in upwd) or (" " in uid):
                print("账号或密码不能有空格")
                continue
            if not (self.is_mobile(uid) or self.is_email(uid)):
                print("账号格式不对,请重新输入")
                continue
            if not self.is_password(upwd):
                print("密码格式不正确")

            data = {"style":"L", "uid":uid, "upwd":upwd}
            request = json.dumps(data).encode()
            self.clientor.send(request)
            msg = self.clientor.recv(128).decode()
            if msg == "OK":
                # 此时应该跳转好友界面
                self.get_fri(uid)
            else:
                print(msg)
                # 验证不通过,返回登录界面
                continue

    def get_fri(self,uid):
        data = {"style":"S", "uid":uid}
        request = json.dumps(data).encode()
        self.clientor.send(request)

        fd = open("friends.txt","w")
        while True:
            msg = self.clientor.recv(4096)
            if not msg:
                break
            fd.write(msg)
        fd.close()


    def touch_others(self, uid, msg):
        """
        we can get touch with others when we used this function;
        :param uid: the uid that you want to get touch with
        :param msg: the message you want to say
        """
        data = {"style":"T"}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        recv_msg = self.clientor.recv(128)
        if recv_msg == "OK":
            request = json.dumps(msg).encode()
            self.clientor.send(request)





if __name__ == '__main__':
    user = ClientManager()



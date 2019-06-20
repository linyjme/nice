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
from models import *
# msg = None
# friend_on_list = []  # 用户上线
# friend_off_list = []  # 用户离线
# add_friend_list = []  # 添加好友
# fri_re = []  # 好友请求结果
# chat_list = []  # 好友私聊信息
# is_friend = []
# disconnect = []  # 异常断开
# create_room = []  # 创建群聊


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
            # self.sockfd.connect(("139.159.132.247", 8888))
            self.sockfd.connect(("139.9.208.188", 8888))
            # self.sockfd.connect(("176.140.7.173", 8888))
        except Exception:
            sys.exit("网络异常,请检查后启动")

    def send(self, value):
        self.sockfd.send(value)

    def recv(self, number):
        return self.sockfd.recv(number)


class ClientSend:
    """
    实现client功能类
    """

    def __init__(self):
        self.clientor = Client()
        # self.clientor.start()

    def is_mobile(self, value):
        """
        判断账号格式是否正确(电话号码)
        we could judge that the value is a
        cell phone number or not
        :param value: argument
        :return: is for True/not for False
        """
        for i in value:
            if i not in "0123456789":
                return False
        return True
        # if not re.search("[0-9]", value):
        #     return False
        # return True

    def is_email(self, value):
        """
        判断账号格式是否正确(电子邮箱)
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
        判断密码格式是否正确
        we could ues this method to judge the correct password
        :param value: your password
        :return: match for True else for False
        """
        if not re.search(r"\b\w{6,20}\b", value):
            return False
        return True

    def register(self, uid, upwd, upwd1, uname):
        """
        注册方法,可以判定账号,密码,昵称格式,并将其发送给服务端,
        接收服务端返回信息进行判定下步操作
        :param uid: 账号
        :param upwd: 密码
        :param upwd1: 重复输入密码
        :param uname: 昵称
        :return: 返回注册结果信息
        """
        if len(uid) < 6 or len(uid) > 11:
            return "请输入6~11位数字账号"
        if (" " in upwd) or (" " in uid):
            return "账号或密码不能有空格"
        if not (self.is_mobile(uid)):
            return "请输入6~11位数字账号"
        if not self.is_password(upwd):
            return "密码格式不正确"
        if upwd != upwd1:
            return "两次输入密码不一致"

        data = {"style": "R", "uid": uid, "uname": uname, "upwd": upwd}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        data = self.clientor.recv(128).decode()

        if data == "OK":
            # 注册结束后跳转登录界面还是直接进入交互界面
            return "注册成功"
        else:
            return data

    def login(self, uid, upwd):
        """
            登录
        :param uid: 账号
        :param upwd: 密码
        :return: 返回结果
        """
        if (" " in upwd) or (" " in uid):
            return False
        if not (self.is_mobile(uid) or self.is_email(uid)):
            return False
        if not self.is_password(upwd):
            return False

        data = {"style": "L", "uid": uid, "upwd": upwd}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        msg = self.clientor.recv(128).decode()
        if msg == "OK":
            # 此时应该跳转好友界面

            return True
        else:
            # 验证不通过,返回登录界面
            return False

    def thread(self):
        # 创建新的线程
        t = Thread(target=self.recvmsg, )
        t.setDaemon(True)  # 分支线程会随主线程退出
        t.start()

    def recvmsg(self):  # 接收信息
        self.clientrecv = ClientRecv()
        while True:
            try:
                msg = json.loads(self.clientor.recv(4096).decode())
            except:
                disconnect.append('与服务器连接异常断开')
                return
            print("接收到的信息：", msg)
            if self.clientrecv.start(msg) == False:
                return

    def get_friends(self, uid):  # 获取在线好友列表
        data = {"style": "S", "uid": uid}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        time.sleep(0.1)
        msg = json.loads(self.clientor.recv(2048).decode())
        if not msg:
            return None
        return msg

    def get_off_msg(self, uid):  # 获取离线好友列表
        data = {"style": "A", "uid": uid}
        request = json.dumps(data).encode()
        self.clientor.send(request)
        time.sleep(0.1)
        msg = json.loads(self.clientor.recv(2048).decode())
        if not msg:
            return None
        return msg

    def add_friend(self, uid, fuid):  # 添加好友
        if uid == fuid:
            return "不能添加自己为好友"
        data = {"style": "F", "uid": uid, "fuid": fuid}
        request = json.dumps(data).encode()
        self.clientor.send(request)

    def friend_request_result(self, uid, fuid, re):  # 处理好友请求
        data = {"style": "D", "uid": uid, "fuid": fuid, "re": re}
        request = json.dumps(data).encode()
        self.clientor.send(request)

    def send_chat_msg(self, uid, fuid, msg, times):  # 发送聊天信息
        data = {"style": "N", "uid": uid, "fuid": fuid, 'msg': msg, "times": times}
        request = json.dumps(data).encode()
        self.clientor.send(request)

    def create_room(self, uid, rid, rname):  # 创建群聊
        if len(rid) > 5:
            return "请输入5位数字群号"
        for i in rid:
            if i not in "0123456789":
                return "请输入5位数字群号"
        data = {"style": "C", "uid": uid, "rid": rid, 'rname': rname}
        request = json.dumps(data).encode()
        self.clientor.send(request)

    def add_room(self, uid, rid):  # 加入群聊
        data = {"style": "R", "uid": uid, "rid": rid}
        request = json.dumps(data).encode()
        self.clientor.send(request)


class ClientRecv:
    # def __init__(self):
    #     self.msg = None
    #     self.friend_on_list = []  # 用户上线
    #     self.friend_off_list = []  # 用户离线
    #     self.add_friend_list = []  # 添加好友
    #     self.frr = []  # 好友请求结果
    #     self.chat_list = []  # 好友私聊信息

    def start(self, msg):
        self.msg = msg
        if msg["style"] == "E":  # 别处登录
            disconnect.append('账号在别处登录，被迫下线')
            return False
        elif msg["style"] == "O":  # 用户上线通知
            self.friend_on()
        elif msg["style"] == "Q":  # 用户离线通知
            self.friend_off()
        elif msg["style"] == "F":  # 添加好友请求信息
            self.friend_request()
        elif msg["style"] == "D":  # 好友请求结果
            self.friend_request_result()
        elif msg["style"] == "N":  # 好友私聊信息
            self.recv_chat_msg()
        elif msg["style"] == "B":  # 是否存在该好友
            self.isfriend()
        elif msg["style"] == "C":  # 创建群聊结果
            self.create_room_result()
        elif msg["style"] == "R":  # 加入群聊结果
            print(msg)
            pass

    def friend_on(self):  # 用户上线通知
        for key, value in self.msg.items():
            if key != "style":
                friend_on_list.append(key)

    def friend_off(self):  # 用户离线通知
        for key, value in self.msg.items():
            if key != "style":
                friend_off_list.append(key)

    def friend_request(self):  # 加好友请求信息
        for key, value in self.msg.items():
            if key != "style":
                add_fri_dict = {}
                add_fri_dict[key] = value
                add_friend_list.append(add_fri_dict)

    def friend_request_result(self):  # 好友请求结果
        fri_re.append(self.msg)

    def recv_chat_msg(self):  # 好友私聊信息
        chatMsgdict = {}
        fuid = self.msg["uid"]  # 好友的账号
        fmsg = self.msg["msg"]  # 好友发送的信息
        times = self.msg["times"]  # 信息时间
        dict1 = {}
        dict1[times] = fmsg
        for item in chat_list:
            for key, value in item.items():
                if key == fuid:
                    item[key].append(dict1)
                    return
        else:
            msg_list = []
            msg_list.append(dict1)
            chatMsgdict[fuid] = msg_list
            chat_list.append(chatMsgdict)  # 加到聊天列表
        # if not chat_list:
        #     msg_list = []
        #     msg_list.append(dict1)
        #     chatMsgdict[fuid] = msg_list
        #     chat_list.append(chatMsgdict)  # 加到聊天列表

    def isfriend(self):
        is_friend.append(self.msg["re"])

    def create_room_result(self):  # 创建群聊结果
        if self.msg["re"] == "no":
            create_room.append("群号:%s\n已被占用"% self.msg["rid"])
        else:
            create_room.append("群号:%s\n创建成功"% self.msg["rid"])


if __name__ == '__main__':
    user = ClientSend()
    user.register("12311111111", "123456", "123456", "123")

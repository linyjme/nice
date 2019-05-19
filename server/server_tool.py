"""
    服务端tool模块
    
"""
import re
import json
from sql_db import *
from sql_tool import *
from response import *
# from server_main import *
# import config as gl

# 存储临时加好友的信息 被添加方账号为键,主动方账号为值
dict_fri = {}

# 存储连接套接字与账号,账号为键，套接字为值
dict_conn = {}

# 存储临时确认好友信息



def get_conn_by_uid(uid):
    """
        调用连接套接字函数
    """
    for kuid in dict_conn:
        if kuid == uid:
            return dict_conn[kuid]


class Servertool(object):
    """
        服务端方法
    """
    def __init__(self):
        self.ser_tool = Sql_tool()


    def record_user_status(self,uid,c):
        """
            记录或更新已登录的用户
            通过测试
        """
        dict_conn[uid] = c



    def get_online_status_by_uid(self,uid):
        """
            通过用户账号获取在线状态
            通过测试
        """
        for i in dict_conn:
            if i == uid:
                return True
        else:
            return False

    def get_rid_repeat_users(self,uid):
        """
            踢掉用户
            待测试
        """
        c = get_conn_by_uid(uid)
        msg = "账号在别处登录，被迫下线"
        c.send(msg.encode())
        # 关闭套接字
        c.close()


    def send_add_fri_require(self,uid,fuid):
        """
            发送好友添加的请求到另外一个客户
            待测试
        """
        # 判断好友是否在线
        for fri in dict_conn:
            if fri == fuid:
                # 获取好友的连接套接字
                c = dict_conn[fri]
                msg = {'style':'F'}
                client_uname = self.ser_tool.get_uname_by_uid(uid)
                msg[uid] = client_uname
                c.send(msg.encode())
                return
        # 否则零时存储好友请求   
        else:
            dict_fri[fuid] = uid


    
    def get_add_fri_require(self,uid):
        """
            获取dict_fir加好友的请求
        """
        fri_list = []
        for fr_uid in dict_fri:
            if fr_uid == uid:
                fri_list.append(dict_fri[fr_uid])
        
        return fri_list

    def del_add_fri_require(self,uid):
        """
            删除零时存放的用户加好友请求
        """
        for key in list(dict_fri):
            if key == uid:
                del dict_fri[key]


    def del_user_status_by_c(self,c):
        """
            通过连接套接字删除用户在线状态
            如果删除成功，则返回用户账号
        """
        # for uid in dict_conn:
        #     if c == dict_conn[uid]:
        #         # dict_conn.pop(uid)
        #         del dict_conn[uid]
        #         return uid
        # else:
        #     return False
        for key in list(dict_conn):
            if c == dict_conn[key]:
                del dict_conn[key]
                return key
        else:
            return False

    
    def send_user_status_to_friend(self,uid,status):
        """
            用户上线或离线，将用户状态发送给好友
            获取用户的在线好友
            上线status O 
            离线status Q
        """
        # 通过用户uid查询好友
        fri_list = self.ser_tool.get_friens_list_by_uid(uid)
        # print("fri_list",fri_list)
        if len(fri_list) == 0:
            # 没有好友，直接退出
            return
        msg = {"status":status}
        uname = self.ser_tool.get_uname_by_uid(uid)
        msg[uid] = uname
        msg = json.dumps(msg)
        for on_uid in dict_conn:
            if on_uid in fri_list:
                # 获得在线好友的连接套接字
                c = dict_conn[on_uid]
                # 将用户状态消息发送给好友
                c.send(msg.encode())



if __name__ == "__main__":
    re = Servertool()
    result = re.get_online_status_by_uid('123')
    print(result)
        
        
        












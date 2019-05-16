"""
    服务端tool模块
    
"""
import re
from sql_db import *
from response import *


# 存储连接套接字与账号
dict_conn = {}

# 存储临时加好友的信息
dict_fri = {}

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
        pass


    def record_user_status(self,uid,c):
        """
            记录或更新已登录的用户
        """
        dict_conn['uid'] = c


    def query_user_status(self,uid):
        """
            查询用户是否在线
        """
        if uid in dict_conn:
            return True
        else:
            return False

    def get_rid_repeat_users(self,uid):
        """
            踢掉用户
        """
        c = get_conn_by_uid(uid)
        c.send(b'down')


    def send_add_fri_require(self,uid,fuid):
        """
            发送好友添加的请求到另外一个客户
        """
        # 判断好友是否在线
        for fri in dict_conn:
            if fri == fuid:
                # 获取好友的连接套接字
                c = dict_conn[fri]
                msg = uid
                c.send(msg.encode())
                return
        # 否则零时存储好友请求    
        else:
            dict_fri[uid] = fuid
    
    def get_add_fri_require(self,uid):
        """
            获取dict_fir加好友的请求
        """
        fri_list = []
        for fr_uid in dict_fri:
            if fr_uid == uid:
                fri_list.append(dict_fri[fr_uid])
        
        return fri_list



        

        
        
        












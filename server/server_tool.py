"""
    服务端tool模块
    
"""
import re
from sql_db import *

# 在线用户
# 键：用户账号
# 值：用户addr
online_user = {}

class Servertool(object):
    """
        服务端方法
    """
    def __init__(self):
        pass


    def record_user_status(self,uid,uaddr):
        """
            记录或更新已登录的用户
        """
        online_user['uid'] = uaddr


    def query_user_status(self,uid):
        """
            查询用户是否在线
        """
        if uid in online_user:
            return True
        else:
            return False

    def get_rid_repeat_users(self,uid,addr):
        """
            踢掉用户
        """
        pass









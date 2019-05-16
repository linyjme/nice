"""
    数据库tool模块
    对数据库的查找，写入，删除操作

"""
import pymysql
from sql_db import *

class Sql_tool():
    def __init__(self):
        self.sql_tool = MySql()
        

    def query_user_by_name(self,uid):
        """
            查询用户表
            返回用户名是否存在数据库
        """
        sql = "select * from user where uid = '%s'"%uid
        
        self.sql_tool.cur.execute(sql)
        r = self.sql_tool.cur.fetchone()
        if r != None:
            return False
        else:
            return True

    def verify_login(self,uid,upwd):
        """
            验证用户登录
            验证账号跟密码是否一致
        """
        sql = "select * from user where uid = '%s' and upwd = '%s'" %(uid,upwd)
        self.sql_tool.cur.execute(sql)
        r = self.sql_tool.cur.fetchone()
        if r != None:
            return True
        else:
            return False

    def insert_user(self,uid,uname,upwd):
        """
            创建用户
            用户信息写入到数据库
        """
        sql = "insert into user (uid ,uname,upwd) values ('%s','%s')"%(uid,uname,upwd)
        try:
            self.sql_tool.cur.execute(sql)
            self.sql_tool.db_conn.commit()
            return True
        except:
            self.sql_tool.db_conn.rollback()
            return False

        

    def save_add_fri_msg(self,uid,fuid):
        """
            存储添加好友信息
        """
        sql = "insert into friends (uid ,fuis) values ('%s','%s')"%(uid,fuid)
        try:
            self.sql_tool.cur.execute(sql)
            self.sql_tool.db_conn.commit()
            return True
        except:
            self.sql_tool.db_conn.rollback()
            return False


    def query_friens_by_uid(self,uid):
        """
            通过用户名查询所有好友
        """
        temp_list = []
        sql = "select  from user where uid = '%s' " % uid
        result = self.sql_tool.cur.execute(sql)
        print(result)
        if result == None:
            return []
        
        # for info in result:
        #     temp_dict = {}
        #     uid = info[0]
        #     fuid = info[1]
        #     temp_dict[uid] = fuid
        #     temp_list.append(temp_dict)
        # return temp_list
        # for info in result:
            

    def insert_friends(self,uid_01,uid_02):
        """
            插入好友信息表
        """
        pass


    def query_uname_by_uid(self,uid):
        """
            通过查询账号获得昵称
            返回好友昵称
        """
        sql = "select uname from user where uid = '%s' " % uid
        result = self.sql_tool.cur.execute(sql)
        return result


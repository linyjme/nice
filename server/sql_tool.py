"""
    数据库tool模块
    对数据库的查找，写入，删除操作

"""
import pymysql
from sql_db import *

class Sql_tool():
    def __init__(self):
        self.sql_tool = MySql()
        # 进入chat数据库
        self.sql_tool.cur.execute("use chat;")
        

    def query_user_by_uid(self,uid):
        """
            查询用户表
            返回用户名是否存在数据库
        """
        sql = "select * from user where uid = '%s'"%uid
        # sql = "select * from user where uid = " + uid
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
        sql = "insert into user (uid ,uname,upwd) values ('%s','%s',%s)"%(uid,uname,upwd)
        try:
            self.sql_tool.cur.execute(sql)
            self.sql_tool.db_conn.commit()
            return True
        except Exception as e:
            print(e)
            self.sql_tool.db_conn.rollback()
            return False


    def insert_friends(self,uid,fuid):
        """
            存储添加好友信息
        """
        sql = "insert into friends (user_id1 ,user_id2) values ('%s','%s')"%(uid,fuid)
        try:
            self.sql_tool.cur.execute(sql)
            self.sql_tool.db_conn.commit()
            return True
        except:
            self.sql_tool.db_conn.rollback()
            return False

    def insert_chat_history(self,uid,fuid,msg,re):
        """
            查询历史记录
        :param uid:
        :param fuid:
        :param msg:
        :return:
        """
        # sql = "insert into chat_history (user_id1 ,user_id2 ,msg) values ('%s','%s','%s')" % (uid, fuid, msg)
        print('进入')
        sql = "insert into chat_history values ('%s','%s','%s',now(),'%s')" % (uid, fuid, msg,re)
        try:
            self.sql_tool.cur.execute(sql)
            self.sql_tool.db_conn.commit()
            return True
        except Exception as e:
            print(e)
            self.sql_tool.db_conn.rollback()
            return False



    def get_friends_list_by_uid(self,uid):
        """
            通过用户名查询所有好友
        """
        temp_list = []
        sql = "select user_id2 from friends where user_id1 = '%s' " % uid
        result01 = self.sql_tool.cur.execute(sql)
        result01 = self.sql_tool.cur.fetchall()
        sql = "select user_id1 from friends where user_id2 = '%s' " % uid
        result02 = self.sql_tool.cur.execute(sql)
        result02 = self.sql_tool.cur.fetchall()
        result = result01 + result02
        if result == None:
            return []
        else:
            for i in result:
                temp_list.append(''.join(i))
        # 此时temp_list 为用户所有好友的账号
        return temp_list

    def query_is_friend(self,user_id1,user_id2):
        """
            查询是否是好友
        """
        sql = "select * from friends where user_id1 = '%s' and user_id2 = '%s'" % (user_id1,user_id2)
        result01 = self.sql_tool.cur.execute(sql)
        result01 = self.sql_tool.cur.fetchone()
        sql = "select * from friends where user_id2 = '%s' and user_id1 = '%s'" % (user_id2,user_id1)
        result02 = self.sql_tool.cur.execute(sql)
        result02 = self.sql_tool.cur.fetchone()
        if result01 or result02:
            return False
        else:
            return True



    def get_uname_by_uid(self,uid):
        """
            通过查询账号获得昵称
            返回用户昵称,字符串
        """
        sql = "select uname from user where uid = '%s' " % uid
        self.sql_tool.cur.execute(sql)
        result = self.sql_tool.cur.fetchone()
        # 结果是一个元组，需要将元组转换为字符串
        result = ''.join(result)
        return result



if __name__ == "__main__":
    re = Sql_tool()
    # re.insert_friends('13750050640','13750050642')
    # print(result)
    # result = re.verify_login("12311111111","123456")
    # print(result)

    # result = re.get_uname_by_uid("12311111111")
    # print(result)
    # print(type(result))

    # result = re.query_friens_by_uid("12345678")
    # print(result)
    # print(type(result))
    # result = re.insert_user("12345678","456","45678")
    # print(result)
    # print(type(result))
    result = re.insert_chat_history('1235','456','hah我是')
    print(result)

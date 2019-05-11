"""
    sql模块
"""
# from hashlib import sha1
from connfig import *
import pymysql


class ConnSql:
    def __init__(self):
        """
            构造方法
        """
        # 数据库连接对象
        self.db_conf = DbConf()

    def open_conn(self):
        """
            连接数据库
        :return:
        """
        try:
            # 建立连接对象
            self.db_conn = pymysql.connect(self.db_conf.host, self.db_conf.user, self.db_conf.passwd,
                                           charset='utf8')
        except Exception as e:
            print("连接数据库错误")
            return False
            print(e)
        # else:
        #     print("连接数据库成功")
    #创建游标
        self.cur = self.db_conn.cursor()
        return True

    def create_chatdb(self):
        """
            访问或创建chat库
        """
        try:
            self.cur.execute("create database chat default charset=utf8")
        except Exception as e:
            print(e)
            return False
        else:
            # print("创建数据库成功")
            return False

    # 创建user表
    def create_user_tb(self):
        #进入chat数据库
        self.cur.execute("use chat:")
        #print(进入数据库成功)
        #用户id
        #用户名称
        #用户id状态
        #用户密码
        sql = "create table user (user_id int primary key auto_increment,\
        user_name varchar(20),\
        user_stateID int,\
        user_passwd varchar(20));"
        self.cur.execute(sql)
        return True

    #创建用户
    def insert_user(self,name, passwd):

        sql = "insert into user(name,passwd) values('%s','%s')"%(name,passwd)
        try:
            self.cur.execute(sql)
            self.db_conn.commit()
            return True
        except:
            self.db_conn.rollback()
            return False

    # #查询用户表
    # def query_user_by_name(name):
    #     sql = "select * from user where name ='%s'"%name
    #     self.cur.execute(sql)
    #     r = self.cur.fetchone()
    #     if r != None:
    #         return False
    #     else:
    #         return r

    #创建聊天记录表
    def create_chat_history_tb(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        #自增长id
        #发送方用户id
        #接收方用户id
        #聊天内容
        sql = "create table chat_history (historyID int primary key auto_increment,\
                              fromID int(32),\
                              userID int(32),\
                              Content text(256),\
                send_time datetime full));"#聊天时间
        self.cur.execute(sql)
        return True

    #创建好友表
    def create_chat_friends(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        #自增长id
        #发送方用户id
        #接收方用户id
        #聊天内容
        sql = "create table frinends (owner_id int not null,\
                              friend_id int not null,\
                              friend_type int(64),\
                              friend_group text(256),\
                );"
        self.cur.execute(sql)
        return True

    #创建好友分组表
    def create_chat_friend_groups(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        #分组ID
        #分组名称
        sql = "create table friend_groups (fg_id int not null,\
                              fg_name varchar(32),\
                              fg_userID int(64),\
                );"#用户ID
        self.cur.execute(sql)
        return True

    #创建好友类型表
    def create_chat_friend_type(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        sql = "create table friend_type (ft_id int not null,\
                                 ft_name varchar(32),\
                   );"  # 类型名称
        self.cur.execute(sql)
        return True

    #创建用户群表
    def create_chat_user_groups(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        # 群ID
        # 群名称
        # 群简介
        sql = "create table user_groups (ug_id int not null,\
                                 ug_name varchar(32),\
                                 ug_intro varchar(200),\
           ug_createtime datatime full);"
        self.cur.execute(sql)
        return True

        # 创建用户群表

    #创建群用户关联表
    def create_chat_groups_to_user(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        # 用户ID
        # 群ID
        #发送时间
        sql = "create table groups_to_user (gt_id int not null,\
                                    gt_userID int(32),\
                                    gt_groupID int(20),\
                                    gt_createtime datatime full,\
              gt_groupnick varchar(15));" # 群内用户昵称
        self.cur.execute(sql)
        return True

    # 创建群消息内容表
    def create_chat_groups_message(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        # 群消息ID
        #群消息内容
        # 发送者ID
        # 发送时间
        sql = "create table groups_message (gm_id int not null,\
                                    gm_content text,\
                                    gm_fromID int(20),\
                                    gm_createtime datatime full,\
              gm_fromname varchar(30));"  # 发送者昵称
        self.cur.execute(sql)
        return True

    # 创建群消息关联表
    def create_chat_groups_message_to_user(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        # 用户ID
        # 群消息ID
        # 接收者ID
        #发送时间
        sql = "create table groups_to_user (gt_id int not null,\
                                    gt_messageID int(32),\
                                    gt_userID int(20),\
                                    gt_createtime datatime full,\
              gt_state varchar(15));"  # 接收状态
        self.cur.execute(sql)
        return True

    #创建群内用户私聊消息关联表
    def create_chat_groups_message_user_to_user(self):
        # 进入chat数据库
        self.cur.execute("use chat:")
        # print(进入数据库成功)
        # 消息内容
        #发送者ID
        #发送时间
        #发送者昵称
        #接收者ID
        #接收状态
        sql = "create table groups_message_user_to_user (gu_id int not null,\
                                    gu_msgcontent varchar(300),\
                                    gu_fromuserID int(32),\
                                    gu_createtime datatime full,\
                                    gu_fromusername varchar(30),\
                                    gu_touserID int(32),\
                                    gu_state bit,\
              gu_usergroupID int(20));" # 所属群ID
        self.cur.execute(sql)
        return True
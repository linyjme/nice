"""
    处理用户请求模块
"""

from server_tool import *
from sql_tool import *


class Response(object):
    """
        处理客户端响应
    """
    def __init__(self):
        
        # 建立数据库调用对象
        self.sql = Sql_tool()

        # 创建服务端方法调用对象
        self.tool = Servertool()



    def do_login(self,c,request,addr):
        """
            处理客户登录
            1.接收客户信息，解析
            2.验证客户账号跟密码
            3.如果账号已经在异地登录，则将其踢下线
            4.用户上线信息进行存储
        """
        uid  = request['uid']
        upwd = request['upwd']
        uaddr = request['addr']
        # 验证客户账号跟密码是否正确
        res = self.sql.verify_login(uid,upwd)
        if res == False:
            c.send('账号或密码有误'.encode())
            return
        user_status = self.tool.query_user_status(uid)
        if user_status == True:
        # 表示远程有登录,剔除远程的下线
            self.tool.get_rid_repeat_users(c,uid,addr)
        c.send(b'OK')
        self.tool.record_user_status(uid,addr)
        
        

    def do_register(self,c,request,addr):
        """
            处理用户注册
            1.接收客户请求
            2.对账号进行验证，如果账号存在，返回失败
            3.如果账号成功，则将用户信息写入数据库
        """
        uid = request["uid"]
        # 验证用户名是否存在
        res = self.sql.query_user_by_name(uid)
        if res == True:
            c.send(b'OK')
            uname = request['uname']
            upwd = request['upwd']
            # 创建用户信息
            self.sql.insert_user(self,uid,uname,upwd)
        else:
            c.send("账号已存在".encode())

    def do_do_joinfriend(self,c,request,addr):
        """
            处理用户添加好友请求
            1.判断好友是否存在
            2.已经是好友
            3.已经发送过好友请求
            4.将用户添加的好友信息暂存到添加好友数据库中
        """
        uid = request['uid']
        fuid = request['fuid']
        res = self.sql.query_user_by_name(fuid)
        if res == True:
            c.send(b'OK')
            # 将用户添加好友的信息存储
        else:
            c.send("用户不存在".encode())


    def do_update_state(self,c,request,addr):
        """
            处理客户刷新请求
            1.接收用户刷新请求
            2.获取被添加好友的信息
            3.获取好友列表(在线好友与非在线好友)
            4.将2,3信息回发给客户端
        """
        pass
    
    def do_joinfriend(self,c,request,addr):
        """
            加好友的功能
        """
        fuid = request['fuid']
        uid = request['uid']
        # 查询好友关系
        




        

        
        




    

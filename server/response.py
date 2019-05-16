"""
    处理用户请求模块
"""

from server_tool import *
from sql_tool import *



# 在线用户
# 键：用户账号
# 值：用户addr
online_user = {}

class Response(object):
    """
        处理客户端响应
    """
    def __init__(self):
        
        # 建立数据库对象调用方法
        self.sql = Sql_tool()

        # 创建服务端对象调用方法
        self.tool = Servertool()



    def do_login(self,c,request):
        """
            处理客户登录
            1.接收客户信息，解析
            2.验证客户账号跟密码
            3.如果账号已经在异地登录，则将其踢下线
            4.用户上线信息进行存储
        """
        uid  = request['uid']
        upwd = request['upwd']
        # uaddr = request['addr']
        # 验证客户账号跟密码是否正确
        res = self.sql.verify_login(uid,upwd)
        if res == False:
            c.send('账号或密码有误'.encode())
            return
        user_status = self.tool.query_user_status(uid)
        if user_status == True:
        # 表示远程有登录,剔除远程的下线
            self.tool.get_rid_repeat_users(uid)
        c.send(b'OK')
        self.tool.record_user_status(uid,c)
        

    def do_register(self,c,request):
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

    def do_joinfriend(self,c,request):
        """
            处理用户添加好友请求
            1.判断好友账号是否存在
            2.已经是好友
            3.已经发送过好友请求
            4.将用户添加的好友信息暂存到添加好友数据库中
        """
        uid = request['uid']
        fuid = request['fuid']
        res = self.sql.query_user_by_name(fuid)
        if res == True:
            c.send(b'OK')
            # 处理用户好友信息添加的请求
            self.tool.send_add_fri_require(uid,fuid)
        else:
            c.send("用户不存在".encode())


    def do_update_state(self,c,request):
        """
            处理用户刷新请求
            1.接收用户刷新请求
            2.获取被添加好友的信息
            3.获取好友列表(在线好友与非在线好友)
            4.将2,3信息回发给客户端
        """
        uid = request['uid']
        fri_re = self.tool.get_add_fri_require(uid)
        fri_re_list = []
        if len(fri_re) != 0:
            for k in fri_re:
                re = self.sql.query_uname_by_uid(k)
                fri_re_list.append(re)
        else:
            pass
        
        fri_list = self.sql.query_friens_by_uid(uid)

    def do_friends_reply(self,c,request):
        """
            处理用户好友请求答复
            如果用户同意，则将同意信息发送给另外一个用户(包括对方好友是否在线)
                如果此时用户不在线，则将信息临时存储
            同时存储两个好友到好友列表
            如果不同意
            回复给另外一个客户端
        """
        uid_re = request['re']
        uid_01 = request['uid']
        uid_02 = request['fuid']

        if uid_re == "yes":
            pass



        
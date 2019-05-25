"""
    处理用户请求模块
"""

from server_tool import *
from sql_tool import *
import json


class Response(object):
    """
        处理客户端响应
    """
    def __init__(self):
        
        # 建立数据库对象调用方法
        self.sql = Sql_tool()

        # 创建服务端对象调用方法
        self.tool = Servertool()

    def do_user_exit(self,c):
        """
            处理用户退出
            删除用户在线状态
            将用户离线信息发送给好友
        """
        uid = self.tool.del_user_status_by_c(c)
        if uid != False:
            # 通知好友用户离线信息
            self.tool.send_user_status_to_friend(uid,'Q')
            return True


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
        uid_c = self.tool.get_online_status_by_uid(uid)
        # print("登录状态",user_status)
        if uid_c != False:
        # 表示远程有登录,剔除远程的下线
            self.tool.get_rid_repeat_users(uid,uid_c)
        c.send(b'OK')
        self.tool.record_user_status(uid,c)

        # 用户上线消息通知给用户好友
        self.tool.send_user_status_to_friend(uid,'O')
        

    def do_register(self,c,request):
        """
            处理用户注册
            1.接收客户请求
            2.对账号进行验证，如果账号存在，返回失败
            3.如果账号成功，则将用户信息写入数据库
        """
        uid = request["uid"]
        # 验证用户名是否存在
        # res = self.sql.query_user_by_name(uid)
        res = self.sql.query_user_by_uid(uid)
        if res == True:
            c.send(b'OK')
            uname = request['uname']
            upwd = request['upwd']
            # 创建用户信息
            self.sql.insert_user(uid,uname,upwd)
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
        msg = {'style':'B'}
        result = self.sql.query_is_friend(uid,fuid)
        if result:
            # msg['re']='is' 已经是好友
            msg['re']='is'
            msg = json.dumps(msg)
            c.send(msg.encode())
            return
        res = self.sql.query_user_by_uid(fuid)
        if res :
            msg['re'] = 'no'
        else:
            msg['re']='yes'
            # 处理用户好友信息添加的请求
            self.tool.send_add_fri_require(uid,fuid)
        msg = json.dumps(msg)
        c.send(msg.encode())


    def do_load_friend_list(self,c,request):
        """
            处理用户刷新请求
            1.接收用户刷新请求
            2.将用户的账号跟昵称打包
            3.将用户好友账号跟昵称打包一并发给用户
        """
        # 发送好友列表给用户
        client_fri_list = {}
        uid = request['uid']
        uname = self.sql.get_uname_by_uid(uid)
        client_fri_list['uid'] = uid
        client_fri_list['uname'] = uname

        fri_list = self.sql.get_friends_list_by_uid(uid)
        # fri_list : ["好友账号":"好友昵称"]
        # fris_on_line : [在线好友]
        if len(fri_list) == 0:
            msg = json.dumps(client_fri_list)
        else:
            list_temp = []
            for item in fri_list:
                fri_dict = {}
                fname = self.sql.get_uname_by_uid(item)
                fri_dict[item] = fname
                list_temp.append(fri_dict)
            client_fri_list["fri_list"] = list_temp

            fris_on_line = []
            for item in fri_list:
                result = self.tool.get_online_status_by_uid(item)
                if result != False:
                    fris_on_line.append(item)
            client_fri_list["fris_on_line"] = fris_on_line
            msg = json.dumps(client_fri_list)

        c.send(msg.encode())

    
    def do_off_line_msg(self,c,request):
        """
            用户离线消息
            离线的消息，离线好友请求
        """
        uid = request['uid']

        # fir_add = {'style':'F'}
        fir_add = {}
        result = self.tool.get_add_fri_require(uid)
        if result:
            for item in result:
                uname = self.sql.get_uname_by_uid(item)
                fir_add[item] = uname
            msg = json.dumps(fir_add)
            # 删除临时存储加好友的请求
            self.tool.del_add_fri_require(uid)
        else:
            msg = json.dumps(fir_add)

        c.send(msg.encode())



    def do_friends_reply(self,c,request):
        """
            处理用户好友请求答复
            如果用户同意，则将同意信息发送给另外一个用户(包括对方好友是否在线)
            如果此时用户不在线，则将信息临时存储
            同时存储两个好友到好友列表
            如果不同意,回复给另外一个客户端
        """
        uid_re = request['re']
        uid_01 = request['uid']
        uid_02 = request['fuid']
        msg = {'style':'D'}
        # 获得好友昵称
        uname = self.sql.get_uname_by_uid(uid_01)
        msg['fuid'] = uid_01
        msg['fname'] = uname
        if uid_re == "yes": 
            msg["re"] = 'yes'
            # 存储好友关系到数据库
            self.sql.insert_friends(uid_01,uid_02)
            # 获得用户是否在线
            fuid_c = self.tool.get_online_status_by_uid(uid_02)
            uid_02_uname = self.sql.get_uname_by_uid(uid_02)
            uid_01_msg = {uid_02:uid_02_uname}
            if fuid_c != False:
                uid_01_msg['style'] = 'O'
                # 获得uid_01是否在线:
                uid_01_status = self.tool.get_online_status_by_uid(uid_01)
                if uid_01_status != False:
                    msg['state'] = 'yes'
                else:
                    msg['state'] = 'no'
                msg = json.dumps(msg)
                fuid_c.send(msg.encode())
            else:
                uid_01_msg['style'] = 'Q'
                # 将信息存储
                self.tool.save_add_fri_rep_msg(uid_02,msg)
            uid_01_msg = json.dumps(uid_01_msg)
            c.send(uid_01_msg.encode())
        else:
            msg["re"] = 'no'
            fuid_c = self.tool.get_online_status_by_uid(uid_02)
            if fuid_c != False:
                msg = json.dumps(msg)
                fuid_c.send(msg.encode())
                return
            else:
                # 将信息存储
                self.tool.save_add_fri_rep_msg(uid_02, msg)


    def do_priv_chat(self,c,request):
        uid  = request['uid']
        fuid = request['fuid']
        msg = request['msg']
        times = request['times']
        # 查看好友是否在线
        fuid_c = self.tool.get_online_status_by_uid(fuid)
        if fuid_c != False:
            # 将聊天信息写入到history
            self.sql.insert_chat_history(uid,fuid,msg,times,'y')
            msg = json.dumps(request)
            fuid_c.send(msg.encode())
        else:
            self.sql.insert_chat_history(uid,fuid,msg,times,'n')


    def do_create_romm(self,c, request):
        """
            创建群聊室
        :param c:
        :param request:
        :return:
        """
        pass

    def do_group_chat(self,c,request):
        """
            群聊消息
        :param c:
        :param request:
        :return:
        """
        pass

            

            


            




        
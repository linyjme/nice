"""
    服务端配置文件
"""

# 服务端地址＆ip

SERVER_IP = "0.0.0.0"
PORT = 8888

# [debug]
DEBUG = True

# 数据库参数
class DbConf(object):
    def __init__(self):
        self.host = "localhost"  # 服务器地址127.0.0.1
        self.user = "root"  # 连接数据库的用户名
        self.passwd = "123456"  # 密码
        self.dbname = "chat"  # 连接哪一个库


# 存储临时加好友的信息 被添加方账号为键,主动方账号为值
# def _init():
#     global dict_fri
#     dict_fri = {}

# def set_value(name, value):
#     dict_fri[name] = value

# def get_value():
#     try:
#         return dict_fri
#     except KeyError:
#         return defValue
        
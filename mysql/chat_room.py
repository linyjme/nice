"""
*chat_room
#定义三种房间
1.用户刚登陆时的房间
2.聊天房间
3.退出登录时的房间
"""
#包含多个用户环境,负责基本的命令处理和广播
import CommandHandler from *
class Room(CommandHandler):

    def __init__(self,server):
        self.server = server
        self.sessions = []

    def add(self,session):
        #一个用户进入房间
        self.sessions.append(session)

    def remove(self,session):
        #一个用户离开房间
        self.sessions.remove(session)

    def broadcast(self,line):
        #向所有用户发送指定消息
        for session in self.sessions:
            session.push(line)

    def do_logout(self,session,line):
        #退出房间
        raise EndSession

class LoginRoom(Room):
    """
    刚登陆的用户房间
    """

    def add(self,session):
        #用户连接成功的回应
        Room.add(self,session)
        session.push("Connect Success")

    def do_login(self,session,line):
        #登录命令处理
        name = line.strip()
        if not name:
            session.push("UserName Empty")
        elif name in self.server.users:
            session.push("UserName Exist")
        else:
            session.name = name
            session.enter(self.server.main_room)

class ChatRoom(Room):
    """
    聊天用的房间
    """
    def add(self,session):
        #广播新用户进入
        session.push("Login Success")
        self.broadcast(session.name + "has entered the room.\n")
        self.server.users[session.name] = session
        Room.add(self,session)

    def remove(self,session):
        #广播用户离开
        Room.remove(self,session)
        self.broadcast(session.name + "has left the room.\n")

    def do_say(self,session,line):
        #客户端发送消息
        self.broadcast(session.name + ":" + line + "\n")

    def do_look(self,session,line):
        #查看在线用户
        session.push("Online Users:\n")
        for other in self.sessions:
            session.push(other.name + "\n")

class LogoutRoom(Room):
    """
    用户退出时的房间
    """

    def add(self,session):
        #从服务器中移除
        try:
            del self.server.users[session.name]
        except KeyError:
            pass









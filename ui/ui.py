from tkinter import *
from tkinter import ttk



class Application:
    def __init__(self, master):
        self.root = master

        # 窗口大小
        self.root.geometry("350x200")
        # 设置窗口标题
        self.root.title("登录")
        # 设置窗口不可变
        self.root.resizable(0, 0)
        self.login_window()
        self.win = None

    def login_window(self):  # 创建登录窗口
        # 设置窗口背景图
        self.photo = PhotoImage(file="backgr.gif")
        self.label = Label(self.root, image=self.photo)
        self.label.pack()

        # 创建账号密码标签
        Label(self.root, text='账号', ).place(x=50, y=40)
        Label(self.root, text='密码', ).place(x=50, y=80)

        # 创建输入框
        text1 = StringVar()
        text2 = StringVar()
        Entry(self.root, textvariable=text1).place(x=110, y=40)
        Entry(self.root, show="*", textvariable=text2).place(x=110, y=80)

        # 创建按钮
        Button(self.root, text="注册", command=self.register_window).place(x=120, y=130)
        Button(self.root, text="登录", command=lambda: self.send_data(text1.get(), text2.get())).place(x=200, y=130)

    def register_window(self):  # 创建注册窗口

        self.reg = Toplevel()
        # 窗口大小
        self.reg.geometry("350x200")
        # 设置窗口大小固定
        self.reg.resizable(0, 0)
        # 设置窗口标题
        self.reg.title("注册")
        # 设置窗口背景图
        photo = PhotoImage(file="backgr.gif")
        label = Label(self.reg, image=photo)  # 图片
        label.pack()
        # 创建账号密码标签
        Label(self.reg, text='账号').place(x=50, y=30)
        Label(self.reg, text='密码').place(x=50, y=70)
        Label(self.reg, text='确认密码').place(x=26, y=110)
        # 创建输入框
        text1 = StringVar()
        text2 = StringVar()
        text3 = StringVar()
        Entry(self.reg, textvariable=text1).place(x=110, y=30)
        Entry(self.reg, show="*", textvariable=text2).place(x=110, y=70)
        Entry(self.reg, show="*", textvariable=text3).place(x=110, y=110)
        # 创建按钮
        Button(self.reg, text="确认注册", command=lambda: self.send_data(text1.get(), text2.get(), text3.get())).place(
            x=250, y=150)

        # command = lambda: self.send_data(text1.get(), text2.get(), text3.get())
        # 循环
        self.reg.mainloop()

    def send_data(self, user, passsword1, passsword2=None):
        """
            发送数据给客户端
        :param user: 用户名
        :param passsword1: 密码
        :param passsword2: 确认密码
        :return:
        """

        if passsword2 == None:
            # 登录成功
            self.login_successfully()
        if passsword2 != None:
            # 注册成功
            self.registered_successfully()

    def login_successfully(self):
        # 登录成功
        Message(self.root, text='登录成功，正在跳转，请稍候...', ).place(x=10, y=130)
        # 更新窗口
        self.root.update()
        # sleep(2)
        # 关闭登录窗口
        self.root.destroy()
        # 跳转到主窗口
        MainWindow(self.root)

    def registered_successfully(self):
        # 注册成功
        Label(self.reg, text='注册成功，请关闭本界面返回登录', ).place(x=30, y=140)


class MainWindow:
    def __init__(self, master):
        self.root = master
        # 创建主窗口
        self.root = Tk()
        # 窗口大小
        self.root.geometry("260x500")
        # 设置窗口标题
        self.root.title("主窗口")

        self.dict = {}
        self.start()

    def start(self):
        tree = ttk.Treeview(self.root, height=20)
        tree.pack()
        treeF1 = tree.insert("", 0, text="我的好友", values=("我的好友"))
        treeF2 = tree.insert("", 1, text="最近联系", values=("最近联系"))
        treeF1_1 = tree.insert(treeF1, 0, text="中国黑龙江", values=("中国黑龙江"))
        reeF1_2 = tree.insert(treeF1, 1, text="中国吉林", values=("中国吉林"))
        reeF1_3 = tree.insert(treeF1, 1, text="中国广东", values=("中国广东"))
        treeF2_1 = tree.insert(treeF2, 0, text="中国黑龙江", values=("中国黑龙江"))
        tree.bind("<Double-1>", self.dblclickAdaptor(self.dblclick, tree=tree))

        Button(self.root, text="添加好友", command=self.add_friend).place(x=170, y=430)

    def dblclickAdaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def dblclick(self, event, tree):
        item = tree.selection()[0]
        name = tree.item(item, "values")[0]
        if name != "我的好友" and name != "最近联系":
            self.chat_window(name)

        # print("you clicked on ", tree.item(item, "values"))
        # print(tree.item(item, "values")[0])

    def chat_window(self, name):  # 创建聊天窗口
        # 如果该窗口存在，则不创建
        if name in self.dict:
            # 显示已经打开窗口
            self.dict[name].deiconify()
            return
        # 创建聊天窗口
        self.chat = Toplevel()
        self.dict[name] = self.chat
        # 窗口大小
        self.chat.geometry("500x400")
        # 设置窗口大小固定
        self.chat.resizable(0, 0)
        # 设置窗口标题
        self.chat.title("与%s聊天" % name)
        # 聊天信息块
        a = Frame(self.chat, width=500, height=300, bg="green")
        a.pack()
        text1 = Text(self.chat, )
        text1.place(in_=a, width=500, height=300)
        # 发送信息块
        b = Frame(self.chat, width=500, height=100, bg="red")
        b.pack()
        text2 = Text(self.chat, )
        text2.place(in_=b, width=500, height=100)
        # 更新聊天信息
        self.recv_message(text1)

        # 点击关闭按钮触发事件
        self.chat.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(name=name))
        self.chat.mainloop()

    def recv_message(self, text):  # 接收信息
        text.config(state=NORMAL)
        # 显示信息
        text.insert(END, "5143543")
        text.config(state=DISABLED)

    def on_closing(self, name):  # 关闭聊天窗口
        self.dict[name].destroy()
        del self.dict[name]

    def add_friend(self):
        # 创建加好友窗口
        self.af = Toplevel()
        # 窗口大小
        self.af.geometry("500x200")
        # 设置窗口大小固定
        self.af.resizable(0, 0)
        # 设置窗口标题
        self.af.title("添加好友")
        Label(self.af, text='输入好友账号').place(x=50, y=30)
        text1 = StringVar()
        Entry(self.af, textvariable=text1).place(x=130, y=30)
        Button(self.af, text="添加好友", command=None).place(x=300, y=30)
        Button(self.af, text="加入群", command=None).place(x=380, y=30)


if __name__ == '__main__':
    root = Tk()
    Application(root)
    root.mainloop()

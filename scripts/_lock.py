import time
import threading

A = threading.Lock()
B = threading.Lock()
import threading


# 死锁
class obj(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.a()   # 如果两个锁同时被多个线程运行，就会出现死锁现象
        self.b()
    def a(self):
        A.acquire()
        print('123')
        B.acquire()
        print(456)
        time.sleep(1)
        B.release()
        print('qweqwe')
        A.release()
    def b(self):
        B.acquire()
        print('asdfaaa')
        A.acquire()
        print('(⊙o⊙)哦(⊙v⊙)嗯')
        A.release()
        B.release()
for i in range(2):  # 循环两次，运行四个线程，第一个线程成功处理完数据，第二个和第三个就会出现死锁
    t = obj()
    t.start()
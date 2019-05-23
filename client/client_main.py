from client_tool import *
from config import *
from ui import *
from tkinter import *

class client(object):

    def __init__(self):
        self.socket = Socket()
        self.deal_db = ClientManager()
        root = Tk()
        self.ui = Application(root)

    def main(self):
        pass

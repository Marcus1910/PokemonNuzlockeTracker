from tkinter import *

class MainWindow():
    def __init__(self, x, y, game):
        self.master = Tk()
        self.masterX = x
        self.masterY = y
        self.game = game
        print(f"given parameters: {self.masterX}, {self.masterY}, {self.game}")
        
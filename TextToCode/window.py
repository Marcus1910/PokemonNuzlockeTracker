from tkinter import *
from PIL import Image, ImageTk
from templateWindow import templateWindow

class testWindow():
    def __init__(self):
        self.tempWindow = templateWindow(400,500)
        self.window = self.tempWindow.master
        

        #self.button = Button(self.master, text = "another one", command = self.newOne)
        #self.button.pack()
        self.resizeImage = self.window.after(300, self.tempWindow.update)
        self.window.mainloop()

    def newOne(self):
        self.wind = templateWindow(400,800,"images.png", self.master)
        self.wind.update()


x = testWindow()
from tkinter import *

class testWindow():
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x600")
        self.window.title("testing purposes")
        #self.tempWindow = templateWindow(400,500)
        #self.window = self.tempWindow.master
        

        #self.button = Button(self.master, text = "another one", command = self.newOne)
        #self.button.pack()
        #self.resizeImage = self.window.after(300, self.tempWindow.update)
        button = Button(self.window, text = "klik", command = self.newWindow)
        button.grid(row=  0, column = 0)
        self.window.mainloop()


    def newWindow(self):
        varWindow("get")
        pass

    # def newOne(self):
    #     self.wind = templateWindow(400,800,"images.png", self.master)
    #     self.wind.update()


class varWindow():
    list = []
    def __init__(self, name):
        self.window = Tk()
        self.window.geometry("200x200")
        self.list.append(name)
        print(self.list)

x = testWindow()
from tkinter import *
from PIL import Image, ImageTk

class templateWindow():
    def __init__(self, x, y, parent = None):
        if parent == None:
            self.master = Tk()
        else:
            self.master = Toplevel(parent)
        self.masterX = x
        self.masterY = y
        self.image = "bg.jpg"

        self.master.geometry(str(self.masterX) + 'x' + str(self.masterY))
        self.master.iconbitmap("nuzlocke.ico")
        self.master.resizable(1,1)

        self.photo = ImageTk.PhotoImage(Image.open(self.image).resize([self.masterX, self.masterY]),Image.BOX)
        self.photoLabel = Label(self.master, image = self.photo)
        self.photoLabel.configure(image = self.photo)
        self.photoLabel.place(x=0, y=0)
        self.photoLabel.image = self.photo

    

    def update(self):
        self.master.update()
        self.masterY = self.master.winfo_height()
        self.masterX = self.master.winfo_width()
        #update the bg to fully cover the adjusted area
        photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self.masterX, self.masterY]))
        self.photoLabel.configure(image = photo)
        self.resizeImage = self.master.after(300, self.update)
        #needed otherwise image is disposed due to garbage collection
        self.photoLabel.image = photo
    
    def stop(self):
        self.master.after_cancel(self.resizeImage)

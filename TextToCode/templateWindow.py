from tkinter import *
from PIL import Image, ImageTk
import os

class TemplateWindow():
    def __init__(self, x, y, parent = None):
        """create template for gui"""
        if parent == None:
            self._master = Tk()
        else:
            self._master = Toplevel(parent)
        self._debugMode = 0
        self._numberOfBadges = 0
        self._game = None
        self._font = "Helvetica 10 italic"

        self._previousX = x
        self._previousY = y
        self._masterX = x
        self._masterY = y
        self._updateTime = 500
        self._image = "bg.jpg"
        self._icon = os.path.join(os.getcwd(), "sprites/icons/nuzlocke.ico")

        self._master.geometry(str(self._masterX) + 'x' + str(self._masterY))
        self._master.iconbitmap(self._icon)
        self._master.resizable(1,1)

        self._photo = ImageTk.PhotoImage(Image.open(self._image).resize([self._masterX, self._masterY]),Image.BOX)
        self._photoLabel = Label(self._master, image = self._photo)
        self._photoLabel.configure(image = self._photo)
        self._photoLabel.place(x=0, y=0)
        self._photoLabel.image = self._photo
        #make widgets resize with window
        self._master.rowconfigure(0, weight = 2)
        self._master.columnconfigure(0, weight = 2)
    

    def update(self):
        """update image relative to window size"""
        self._master.update()
        self._masterY = self._master.winfo_height()
        self._masterX = self._master.winfo_width()
        if (self._masterX != self._previousX) or (self._masterY != self._previousY):
            print("updating")
            #update the bg to fully cover the adjusted area
            photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self._masterX, self._masterY]))
            self._photoLabel.configure(image = photo)
            #update values after resize
            self._previousX = self._masterX
            self._previousY = self._masterY
            #needed otherwise image is disposed due to garbage collection
            self._photoLabel.image = photo
        self._resizeImage = self._master.after(self._updateTime, self.update)
    
    def stop(self):
        """stop the update cycle else an error can occur"""
        self._master.after_cancel(self._resizeImage)

    def run(self):
        """function to actually run the window"""
        self._master.mainloop()
    
    def exit(self):
        self._master.destroy()
from tkinter import *
from PIL import ImageTk, Image
#from BlazeBlack2Redux import BlazeBlack2Redux
#from RenegadePlatinum import RenegadePlatinum


class SelectGameWindow():

    def __init__(self):
        self.debugMode = 0
        self.listOfGames = ["Blaze Black Redux 2", "Renegade Platinum"]

        self.window = Tk()
        self.windowx = 962
        self.windowy = 601
        self.window.title('game selection')

        
        self.window.geometry(str(self.windowx) + 'x' + str(self.windowy))
        self.window.iconbitmap("nuzlocke.ico")
        self.window.resizable(1,1)

        #make the background as big as the screen
        self.photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self.windowx, self.windowy]),Image.BOX)
        self.photoLabel = Label(self.window, image = self.photo)
        self.photoLabel.grid(row=0, column=0, rowspan=5, columnspan=5)

        self.continueButton = Button(self.window, text = "continue")
        self.continueButton.grid(row = 1, column = 1, sticky = SE)

        self.resizeImage = self.window.after(300, self.update)
        self.window.mainloop()

    def update(self):
        self.window.update()
        self.windowy = self.window.winfo_height()
        self.windowx = self.window.winfo_width()
        if self.debugMode:
            print(f"windowx: {self.windowx}, windowy: {self.windowy}")
        #update the bg to fully cover the adjusted area
        photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self.windowx, self.windowy]))
        self.photoLabel.configure(image = photo)
        self.resizeImage = self.window.after(100, self.update)
        #needed otherwise image is disposed due to garbage collection
        self.photoLabel.image = photo



if __name__ == "__main__":
    x = SelectGameWindow()
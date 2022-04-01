from modulefinder import Module
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

        self.backgroundFrame = Frame(self.window, width = self.windowx, height = self.windowy)
        self.backgroundFrame.grid(row=0, column=0)

        #make the background as big as the screen
        self.photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self.windowx, self.windowy]),Image.BOX)
        self.photoLabel = Label(self.backgroundFrame, image = self.photo)
        self.photoLabel.grid(row=0,column=0, rowspan=2, columnspan=2)

        self.chosen = StringVar()
        self.chosen.set("which game?")
        self.chosenGameMenu = OptionMenu(self.backgroundFrame, self.chosen , *self.listOfGames )
        self.chosenGameMenu.grid(row = 0, column = 1, sticky = NE)

        self.continueButton = Button(self.backgroundFrame, text = "continue", command = self.nextWindow)
        self.continueButton.grid(row = 1, column = 1, sticky = SE)

        self.exitButton = Button(self.backgroundFrame, text = "Exit", command = self.exitWindow)
        self.exitButton.grid(row = 1, column = 0, sticky = SW)

        #call function to resize image to GUI scale
        self.window.after(300, self.update)
        self.window.mainloop()
    

    def nextWindow(self):
        self.chosenGame = self.chosen.get()
        if self.chosenGame not in self.listOfGames:
            self.chosenGameMenu.config(bg = 'Red')
        else:
            from mainWindow import MainWindow 
            if self.debugMode:
                print(f"selected {self.chosenGame}")
            #call to next window
            self.window.destroy()
            MainWindow(self.windowx, self.windowy, self.chosenGame)


    def exitWindow(self):
        self.window.destroy()

    def update(self):
        self.window.update()
        self.windowy = self.window.winfo_height()
        self.windowx = self.window.winfo_width()
        #update the bg to fully cover the adjusted area
        photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self.windowx, self.windowy]))
        self.photoLabel.configure(image = self.photo)
        self.window.after(100, self.update)
        #needed otherwise image is disposed due to garbage collection
        self.photoLabel.image = photo

if __name__ == "__main__":
    x = SelectGameWindow()
from tkinter import *
from PIL import ImageTk, Image
from templateWindow import templateWindow
#from BlazeBlack2Redux import BlazeBlack2Redux
#from RenegadePlatinum import RenegadePlatinum


class SelectGameWindow():

    def __init__(self):
        self.debugMode = 0
        self.listOfGames = ["Blaze Black Redux 2", "Renegade Platinum"]

        self.tempWindow = templateWindow(400, 500)
        self.window = self.tempWindow.master
        self.window.title('game selection')
        #self.backgroundFrame = Frame(self.window, width = self.tempWindow.masterX, height = self.tempWindow.masterY)
        #self.backgroundFrame.grid(row=0, column=0)

        self.chosen = StringVar()
        self.chosen.set("which game?")
        self.chosenGameMenu = OptionMenu(self.window, self.chosen , *self.listOfGames)
        self.chosenGameMenu.grid(row = 0, column = 1, sticky = NE)

        self.continueButton = Button(self.window, text = "continue", command = self.nextWindow)
        self.continueButton.grid(row = 1, column = 1, sticky = SE)

        self.exitButton = Button(self.window, text = "Exit", command = self.window.destroy)
        self.exitButton.grid(row = 1, column = 0, sticky = SW)
        
        #call function to resize image to GUI scale
        self.resizeImage = self.window.after(300, self.tempWindow.update)
        #self.tempWindow.stop()
        self.window.mainloop()

    def nextWindow(self):
        self.chosenGame = self.chosen.get()
        if self.chosenGame not in self.listOfGames:
            self.chosenGameMenu.config(bg = 'Red')
        else:
            from mainWindow import MainWindow 
            if self.debugMode:
                print(f"selected {self.chosenGame}")
            #make the update loop stop
            self.window.after_cancel(self.resizeImage)
            self.tempWindow.stop()
            self.window.destroy()
            #call to next window
            MainWindow(self.tempWindow.masterX, self.tempWindow.masterY, self.chosenGame, self.debugMode)

if __name__ == "__main__":
    x = SelectGameWindow()
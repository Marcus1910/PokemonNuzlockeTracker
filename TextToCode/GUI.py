from tkinter import *
from templateWindow import templateWindow
#from BlazeBlack2Redux import BlazeBlack2Redux
#from RenegadePlatinum import RenegadePlatinum


class SelectGameWindow():

    def __init__(self):
        self.debugMode = 0
        self.listOfGames = ["Blaze Black Redux 2", "Renegade Platinum", "Sacred Gold"]

        self.tempWindow = templateWindow(600, 500)
        self.window = self.tempWindow.master
        self.window.title('game selection')

        self.chosen = StringVar()
        self.chosen.set("which game?")
        self.chosenGameMenu = OptionMenu(self.window, self.chosen , *self.listOfGames)
        self.chosenGameMenu.grid(row = 0, column = 0, columnspan = 3, sticky = N)

        self.continueButton = Button(self.window, text = "continue", command = self.nextWindow)
        self.continueButton.grid(row = 5, column = 5, sticky = SE)

        self.exitButton = Button(self.window, text = "Exit", command = self.window.destroy)
        self.exitButton.grid(row = 5, column = 0, sticky = SW)
        
        #resizes window
        self.window.rowconfigure(0, weight = 2)
        self.window.columnconfigure(0, weight = 2)
        #call function to resize image to GUI scale
        self.resizeImage = self.window.after(300, self.tempWindow.update)
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
            #self.window.after_cancel(self.resizeImage)
            self.tempWindow.stop()
            self.window.destroy()
            #call to next window
            MainWindow(self.tempWindow.masterX, self.tempWindow.masterY, self.chosenGame, self.debugMode)

if __name__ == "__main__":
    x = SelectGameWindow()
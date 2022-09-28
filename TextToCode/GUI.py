from tkinter import *
from templateWindow import TemplateWindow
#from BlazeBlack2Redux import BlazeBlack2Redux
#from RenegadePlatinum import RenegadePlatinum


class SelectGameWindow(TemplateWindow):

    def __init__(self):
        super().__init__(900, 570)

        self._listOfGames = ["Blaze Black Redux 2", "Renegade Platinum", "Sacred Gold"]

        self._master.title('game selection')
        self._chosen = StringVar()
        self._chosen.set("which game?")
        self._chosenGameMenu = OptionMenu(self._master, self._chosen , *self._listOfGames)
        self._chosenGameMenu.grid(row = 0, column = 0, columnspan = 3, sticky = N)

        self._continueButton = Button(self._master, text = "continue", command = self.nextWindow)
        self._continueButton.grid(row = 5, column = 5, sticky = SE)

        self._exitButton = Button(self._master, text = "Exit", command = self.exit)
        self._exitButton.grid(row = 5, column = 0, sticky = SW)

        self.update()
        self.run()

    def nextWindow(self):
        self._chosenGame = self._chosen.get()
        #print(f"wrong : {wrongInput}")
        if self._chosenGame not in self._listOfGames:
            #wrongInput += 1
            #if wrongInput == 3:
            #    print("ja toch")
            #    pass
            self._chosenGameMenu.config(bg = 'Red')
        else:
            #wrongInput = 0
            from mainWindow import MainWindow
            if self._debugMode:
                print(f"selected {self._chosenGame}")
            
            #make the update loop stop
            self.stop()
            self.exit()
            #call to next window
            MainWindow(self._masterX, self._masterY, self._chosenGame)

if __name__ == "__main__":
    x = SelectGameWindow()
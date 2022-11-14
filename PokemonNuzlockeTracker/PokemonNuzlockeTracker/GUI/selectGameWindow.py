from tkinter import *

from templateWindow import TemplateWindow
from mainWindow import MainWindow
#imports every game and checkGames + getGameObject
import games as gm

class SelectGameWindow(TemplateWindow):

    def __init__(self):
        super().__init__(900, 570)
        #determine how many rows and columns the window has
        self.configureWindow(5,5)

        #TODO replace with function call
        self._listOfGames = gm.checkGames()
        #forward declaration, empty otherwise option menu cannot be created
        self._saveFiles = [""]

        self._master.title('game selection')

        self._setupFrame = Frame(self._master)
        self._setupFrame.grid(row = 0, column = 2, sticky = N)
        
        self._chosenGame = StringVar()
        self._chosenGame.set("which game?")
        self._chosenGame.trace_add("write", self.validateGame)
        self._gameMenu = OptionMenu(self._setupFrame, self._chosenGame , *self._listOfGames)
        self._gameMenu.grid(row = 0, column = 0, sticky = N)
        
        self._chosenSaveFile = StringVar()
        self._chosenSaveFile.set("which saveFile?")
        self._chosenSaveFile.trace_add("write", self.validateSaveFile)
        self._saveFile = OptionMenu(self._setupFrame, self._chosenSaveFile, *self._saveFiles)
        self._saveFile.grid(row = 1, column = 0, sticky = EW)
        self._saveFile.configure(state = DISABLED)

        """forward creation"""
        self._saveFileDataFrame = Frame(self._setupFrame)
        self._saveFileDataFrame.grid(row = 3, column = 0, sticky = NSEW)


        self._continueButton = Button(self._master, text = "continue", command = self.nextWindow)
        self._continueButton.grid(row = 5, column = 5, sticky = SE)
        self._continueButton.configure(state = DISABLED)

        self._exitButton = Button(self._master, text = "Exit", command = self.exit)
        self._exitButton.grid(row = 5, column = 0, sticky = SW)

        self.update()
        self.run()


    def resetSaveFileOption(self):
        self._saveFileDataFrame.grid_remove()
        self._chosenSaveFile.set("which saveFile?")

    #TODO replace to logic folder relook code
    def validateGame(self, *args):
        """validates the game chosen"""
        #checks if self._game already exists
        try:
            #checks if the chosengame has changed and resets chosengame to default if it has
            if self._game != self._chosenGame.get():
                self.resetSaveFileOption()
        except AttributeError:
            #first time changing games from default position
            pass
            

        self._game = self._chosenGame.get()
        self._gameObject = gm.MainGame(self._game)
        
        if self._game in self._listOfGames:
            
            #get all the savefiles from that game
            self._saveFile.configure(state = NORMAL)
            self.updateSaveFiles()
        else:
            self._gameMenu.config(bg = 'Red')
            self._saveFile.configure(state = DISABLED)
    
    def updateSaveFiles(self):
        """clear the menu, than update it"""
        self._saveFiles = self._gameObject.getSaveFiles()
        menu = self._saveFile["menu"]
        menu.delete(0, "end")
        for save in self._saveFiles:
            menu.add_command(label = save, command = lambda value = save: self._chosenSaveFile.set(value))
    
    #TODO replace to logic folder
    def validateSaveFile(self, *args):
        self._save = self._chosenSaveFile.get()
        print(self._save)
        if self._save in self._saveFiles:
            self._continueButton.configure(state = NORMAL)
            self.showSaveFileData()
        else:
            self._continueButton.configure(state = DISABLED)

    def showSaveFileData(self):
        for label in self._saveFileDataFrame.winfo_children():
            label.destroy()
        if self._save != "new":
            self._saveFileDataFrame.grid()
            #TODO call function that reads the savedata from the saveFile
            badge = 3
            caughtPokemon = 15
            deadPokemon = 2
            remainingEncounters = 9
            self.createDisplayLabel(f"badges: {badge}", 0)
            self.createDisplayLabel(f"caughtPokemon: {caughtPokemon}", 1)
            self.createDisplayLabel(f"dead pokemon: {deadPokemon}", 2)
            self.createDisplayLabel(f"remaining encounters: {remainingEncounters}", 3)
        else:
            self._saveFileDataFrame.grid_remove()


    def createDisplayLabel(self, text, row, column = 0):
        label = Label(self._saveFileDataFrame, text = text)
        label.grid(row = row, column = column)

    def nextWindow(self):
        #make the update loop stop
        self.stop()
        self.exit()
        #call to next window

        MainWindow(self._masterX, self._masterY, self._gameObject, self._save)

if __name__ == "__main__":
    x = SelectGameWindow()
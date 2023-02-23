import tkinter as tk
from PIL import Image, ImageTk
import os

class PokemonFrame(tk.Frame):

    _spriteFolder = os.path.join(os.path.dirname(os.getcwd()), f"images/sprites")
    _pokemonSpritesFolder = os.path.join(_spriteFolder, f"pokemon")

    states = ["Catch", "Caught", "Failed"]
    buttonImages = ["white", "green", "red"]
    #TODO how to change dynamically
    buttonWidth = 8
    
    def __init__(self, master, pokemon, areaTypeName):
        """this frame always contains a button, imagelabel, namelabel, levelslabel, percentagelabel which are stored as variables for easy access"""
        super().__init__(master)
        #this pokemon instance is only used to read data, it is no longer connected to the lists in encounterwindow
        self.pokemon = pokemon 
        self.row = 0
        #needs to know whether he is fishing or surfing etc, needed for catching
        self.areaTypeName = areaTypeName 

        self.level = tk.IntVar()

        self.statusTextVariable = tk.StringVar()
        self.statusTextVariable.set(self.states[self.pokemon.captureStatus])

        #stringvar in case the encounter name has been incorrectly submitted
        self.nameTextVariable = tk.StringVar()
        self.nameTextVariable.set(self.pokemon.name)

        self.catchButton = tk.Button(self, textvariable = self.statusTextVariable, width = self.buttonWidth)
        self.catchButton.grid(row = self.row, column = 0)

        self.imageLabel = self.createImageLabel()
        self.imageLabel.configure(image = self.pokemonImage)

        
        self.levels = None if self.pokemon.levels == "N/A" or self.pokemon.levels == "n/a" else self.getLevels(self.pokemon.levels)
        self.levelsLabel = self.placeLevelsLabel()
        
        self.selectedLevelMenu = None

        self.percentageLabel = self.textLabel(self, pokemon.percentage, self.row, 3)

        self.configure(pady = 1)
    
    def placeLevelsLabel(self):
        """function that determines whether or not the optionmenu with levels should be shown"""
        if self.levels == None: #do not create a frame, only display levelLabel
            placement = self
            column = 2
            self.level.set(1) #set it to 1 as there is no option to change it
        else: #create a frame in which both the levelslabel and the optionmenu are placed
            self.levelFrame = tk.Frame(self)
            self.levelFrame.grid(row = self.row, column = 2)
            self.createLevelMenu()
            placement = self.levelFrame
            column = 0

        return self.textLabel(placement, self.pokemon.levels, 0, column)

    def createLevelMenu(self):
        tk.OptionMenu(self.levelFrame, self.level, *self.levels).grid(row = 1, column = 0)
        #set the intvar to the lowest value possible
        self.level.set(self.levels[0])


    def createImageLabel(self):
        image = os.path.join(self._pokemonSpritesFolder, (self.pokemon.name + ".png"))
        self.pokemonImage = self.getImageTKObject(image, size = [90,90])
        imageLabel = tk.Label(self, image = self.pokemonImage, textvariable = self.nameTextVariable, compound = "top", borderwidth = 1, relief = "solid")
        imageLabel.grid(row = self.row, column = 1)
        return imageLabel
    
    def textLabel(self, parent, text, row, column):
        """quick function that creates a label and returns it. bw = 2, relief = flat and sticky = NSEW"""
        textLabel = tk.Label(parent, text = text, borderwidth = 2, relief = "flat")
        textLabel.grid(row = row, column = column, sticky = tk.NSEW)
        return textLabel

    def getLevels(self, levels):
        """function that takes a string like '5-8' and returns [5,6,7,8] also works for strings like '1-2-3-4'. 
        does not work for string like '1-3-4' as it will still display a 2"""
        separatedLevels = levels.split("-")
        return list(range(int(separatedLevels[0]), int(separatedLevels[-1]) + 1))

    def updateCatchButton(self, pokemonStatus):
        self.catchButton.configure(background = self.buttonImages[pokemonStatus])
        self.statusTextVariable.set(self.states[pokemonStatus])
    
    def updateState(self, pokemonStatus):
        return (pokemonStatus + 1) % len(self.states)

    def getImageTKObject(self, image, size = [90,90]):
        """function that returns a imageTKObject with the image and size [x,y] defaulkt is [90,90]"""
        try:
            pokemonImage = ImageTk.PhotoImage(Image.open(image).resize(size).convert("RGBA"))
        except tk.TclError:
            image = os.path.join(self._spriteFolder, '0.png')
            pokemonImage = ImageTk.PhotoImage(Image.open(image).resize(size).convert("RGBA"))
        return pokemonImage



    

    

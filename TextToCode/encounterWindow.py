from tkinter import *
from tkinter import ttk
import os


class EncounterWindow():
    _caughtPokemon = {}
    _intvarList = {}

    def __init__(self, parent, area):
        self.area = area
        self._encounterList = area.encounters
        self._areaName = area.name
        self._master = Toplevel(parent)
        #self._master.resizable(False, False)
        self._master.attributes("-topmost", True)
        self._master.geometry("450x600")
        self._master.title(self._areaName)
        self._master.columnconfigure(0, weight = 1)
        self._master.rowconfigure(0, weight = 1)
        self._masterCanvas = Canvas(self._master)
        self._masterCanvas.grid(row = 0, column = 0, sticky = NSEW)

        #captureButtonFrame = Frame(self._master, bg = "red")
        #captureButtonFrame.grid(row = 1, column = 0)
        captureButton = Button(self._master, text = "capture selected pokemon", command = self.updateCapturedPokemon)
        captureButton.grid(row = 1, column = 0, sticky = EW)
        
        scrollbar = Scrollbar(self._master, orient = VERTICAL, command = self._masterCanvas.yview)
        scrollbar.grid(row = 0, column = 5, sticky = NS)

        self._masterCanvas.configure(yscrollcommand = scrollbar.set)
        self._masterCanvas.bind('<Configure>', lambda e: self._masterCanvas.configure(scrollregion = self._masterCanvas.bbox("all")))
        self._canvasFrame = Frame(self._masterCanvas)
        self._masterCanvas.create_window((0,0), window = self._canvasFrame, anchor = NW)

        self.makeAreas()

    def makeAreas(self):
        row = 0
        column = 0
        placement = 0
        for index, areaType in enumerate(self._encounterList):
            #determine position for the next label, next to it and/or below it
            if (index % 2) == 0:
                placement = 0
                if index > 0:
                    #adjust row to create even surfaces
                    row += max(len(areaType[1]), len(self._encounterList[index-1]))
            else:
                placement = 2
            
            areaTypeFrame = Frame(self._canvasFrame, borderwidth = 1, relief = "solid")
            areaTypeFrame.grid(row = row, column = column + placement, columnspan = 2, sticky = NSEW)

            typeLabel = Label(areaTypeFrame, text = areaType[0], borderwidth = 1, relief = "raised", fg = "blue")
            typeLabel.grid(row = 0, column=1, columnspan = 5, sticky = NSEW)

            SpritesPath = os.path.join(os.getcwd(), "sprites/pokemon")

            #draw everything inside areaTypeFrame
            for index, encounter in enumerate(areaType[1]): 
                if encounter.name  not in self._intvarList:
                    self._intvarList[encounter.name] = BooleanVar() 

                #checkbuttons             
                checkButton = Checkbutton(areaTypeFrame, variable = self._intvarList[encounter.name])
                checkButton.grid(row = index + 1, column = 0)


                #get correct pokemon picture
                image = os.path.join(SpritesPath, (encounter.name + ".png"))
                try:
                    pokemonImage = PhotoImage(file = image)
                except TclError:
                    image = os.path.join(SpritesPath, '0.png')
                    pokemonImage = PhotoImage(file = image)

                imageLabel = Label(areaTypeFrame, image = pokemonImage, borderwidth = 1, relief = "solid")
                imageLabel.grid(row = index + 1, column = 1)

                self.encounterLabel(areaTypeFrame, encounter.name, index + 1, 2)
                self.encounterLabel(areaTypeFrame, encounter.levels, index + 1, 3)
                self.encounterLabel(areaTypeFrame, encounter.percentage, index + 1, 4)
                imageLabel.image = pokemonImage

    def encounterLabel(self, frame, text, row, column):
        encounterNameLabel = Label(frame, text = text, borderwidth = 2, relief = "flat")
        encounterNameLabel.grid(row = row, column = column, sticky = NSEW)
    
    def updateCapturedPokemon(self):
        print("updating")
    
            

    
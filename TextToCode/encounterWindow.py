from tkinter import *
from tkinter import ttk
import os

class EncounterWindow():
    def __init__(self, parent, area):
        self.area = area
        self._encounterList = area.encounters
        self._areaName = area.name

        self._master = Toplevel(parent)
        #self._master.resizable(False, False)
        self._master.attributes("-topmost", True)
        self._master.geometry("400x600")
        self._master.title(self._areaName)
        self._master.columnconfigure(0, weight = 1)
        self._master.rowconfigure(0, weight = 1)
        self._masterFrame = Frame(self._master, bg = "green")
        self._masterFrame.grid(row = 0, column = 0, sticky = NSEW)

        #self._canvas = Canvas(self._masterFrame, bg ="red")
        #self._canvas.grid(row = 0, column = 0, sticky = NS)
        
        
        #scrollbar = ttk.Scrollbar(self._masterFrame, orient = VERTICAL, command = self._canvas.yview)
        #scrollbar.grid(row = 0, column = 5, sticky = NS)

        #self._canvas.configure(yscrollcommand = scrollbar.set)
        #self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion = self._canvas.bbox("all")))
        #self._secondFrame = Frame(self._masterFrame, bg = "blue")
        #self._canvas.create_window((0,0), window = self._secondFrame, anchor = NW)

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
                    row += max(len(areaType[1]), len(self._encounterList[index-1]))
            else:
                placement = 2
                

                

            
            
            areaTypeFrame = Frame(self._masterFrame, borderwidth = 1, relief = "solid")
            areaTypeFrame.grid(row = row, column = column + placement, columnspan = 2, sticky = NSEW)
            print(f"placing label {index} at row: {row} and column: {column + placement}")

            typeLabel = Label(areaTypeFrame, text = areaType[0], borderwidth = 1, relief = "raised", fg = "blue")
            typeLabel.grid(row = 0, column=1, columnspan = 5, sticky = NSEW)

            SpritesPath = os.path.join(os.getcwd(), "sprites/pokemon")
            for index, encounter in enumerate(areaType[1]):
                #get correct pokemon picture
                #print(encounter.name)
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

            

    
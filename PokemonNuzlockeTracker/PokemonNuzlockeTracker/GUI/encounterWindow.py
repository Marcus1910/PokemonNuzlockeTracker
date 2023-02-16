from tkinter import *
from PIL import Image, ImageTk
from trainerPokemon import EncounteredPokemon
import os


class EncounterWindow():
    #for GUI purposes only
    _caughtPokemon = {}

    #used to update buttons and labels across multiple encounterwindow instances
    _labelTextDict = {}
    _labelObjDict = {}
    _buttonDict = {}

    _spriteFolder = os.path.join(os.path.dirname(os.getcwd()), f"images/sprites")
    _pokemonSpritesFolder = os.path.join(_spriteFolder, f"pokemon")

    #other position for declaration?
    states = ["Catchable", "Caught", "Failed"]
    colours = ["white", "green", "red"]
    
    def __init__(self, parent, area, save):
        self.area = area
        self._encounterList = area.encounters
        self._areaName = area.name
        self._localLabelObjDict = {}
        self._localButtonDict = {}
        self._temporaryCaptures = {}
        #add the pokemon already caught in this area to global caughtlist
        #update should also remove duplicates 
        self._caughtPokemon.update(self.area.encounteredPokemon)
        print(self._caughtPokemon)

        self._master = Toplevel(parent)
        #self._master.resizable(False, False)
        self._master.attributes("-topmost", True)
        self._master.geometry(f"450x600+{parent.winfo_x()}+{parent.winfo_y()}")
        self._master.title(self._areaName)
        self._master.columnconfigure(0, weight = 1)
        self._master.rowconfigure(0, weight = 1)
        self._masterCanvas = Canvas(self._master)
        self._masterCanvas.grid(row = 0, column = 0, sticky = NSEW)

        #captureButtonFrame = Frame(self._master, bg = "red")
        #captureButtonFrame.grid(row = 1, column = 0)
        captureButton = Button(self._master, text = "Capture selected pokemon", command = self.updateCapturedPokemon)
        captureButton.grid(row = 1, column = 0, sticky = EW)
        
        scrollbar = Scrollbar(self._master, orient = VERTICAL, command = self._masterCanvas.yview)
        scrollbar.grid(row = 0, column = 5, sticky = NS)

        self._masterCanvas.configure(yscrollcommand = scrollbar.set)
        self._masterCanvas.bind('<Configure>', lambda e: self._masterCanvas.configure(scrollregion = self._masterCanvas.bbox("all")))
        self._canvasFrame = Frame(self._masterCanvas)
        self._masterCanvas.create_window((0,0), window = self._canvasFrame, anchor = NW)

        #on window deletion
        self._master.protocol("WM_DELETE_WINDOW", self.destroy)#, self.checkLeftoverChanges)

        self.makeAreas()

    # def checkLeftoverChanges(self):
    #     #TODO relook code, does not work properly
    #     print(self._temporaryCaptures)
    #     if len(self._temporaryCaptures) > 0:
    #         popup = Toplevel(self._master)
    #         popup.title("confirmation")
    #         popup.attributes("-topmost", True)
    #         popup.configure(bg = "red")
    #         Label(popup, text = "There are unsaved changes, are you sure you want to close this window?\n All changes will be deleted", bg = "red").grid(row = 0, column = 0)
    #         Button(popup, text = "yes", command = lambda: [self.updateLists(), self._master.destroy()]).grid(row = 1, column = 0)
    #         Button(popup, text = "No", command = popup.destroy).grid(row = 1, column = 1)
    #     else:
    #         self.updateLists()
    #         self._master.destroy()

    def updateLists(self):
        """removes Buttons / labels from class variable lists so you can open the same window without error. Also clears temporaryCaptures"""
        self._temporaryCaptures.clear()
        for name, labelList in self._localLabelObjDict.items():
            if name in self._labelObjDict:
                list = self._labelObjDict[name]
                for label in labelList:
                    list.remove(label)
        for name, buttonList in self._localButtonDict.items():
            if name in self._buttonDict:
                list = self._buttonDict[name]
                for button in buttonList:
                    list.remove(button)
        
    def makeAreas(self):
        row = 0
        column = 0
        placement = 0
        alreadyCaught = []
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

            #draw everything inside areaTypeFrame
            for index, encounter in enumerate(areaType[1]):
                if encounter.name not in self._caughtPokemon and encounter.captureStatus > 0:
                    self._caughtPokemon[encounter.name] = encounter
                    print(f"adding {encounter.name} to caught list")
                    
                if encounter.name  not in self._labelTextDict:
                    self._labelTextDict[encounter.name] = StringVar()
                    self._labelTextDict[encounter.name].set("catch")
                    self._buttonDict[encounter.name] = []
                    self._labelObjDict[encounter.name] = []
                if encounter.name not in self._localButtonDict:
                    self._localButtonDict[encounter.name] = []
                    self._localLabelObjDict[encounter.name] = []# create empty list to store all labels for pokemon

                #checkbutton    
                catchButton = Button(areaTypeFrame, textvariable = self._labelTextDict[encounter.name], command = lambda pokemon = encounter: [self.catchPokemon(pokemon)])
                catchButton.grid(row = index + 1, column = 0)

                #get correct pokemon picture
                image = os.path.join(self._pokemonSpritesFolder, (encounter.name + ".png"))
                try:
                    pokemonImage = ImageTk.PhotoImage(Image.open(image).resize([90, 90]).convert("RGBA"))
                except TclError:
                    image = os.path.join(self._spriteFolder, '0.png')
                    pokemonImage = ImageTk.PhotoImage(Image.open(image).resize([90, 90]).convert("RGBA"))


                imageLabel = Label(areaTypeFrame, image = pokemonImage, textvariable = self._labelTextDict[encounter.name], borderwidth = 1, relief = "solid", compound = "top")
                imageLabel.grid(row = index + 1, column = 1)

                self.encounterLabel(areaTypeFrame, encounter.name, index + 1, 2)
                self.encounterLabel(areaTypeFrame, encounter.levels, index + 1, 3)
                self.encounterLabel(areaTypeFrame, encounter.percentage, index + 1, 4)
                
                #all the same pokemon labels will change at the same time
                self._labelObjDict[encounter.name].append(imageLabel)
                self._buttonDict[encounter.name].append(catchButton)
                self._localLabelObjDict[encounter.name].append(imageLabel)
                self._localButtonDict[encounter.name].append(catchButton)

                #checks whether or not the pokemon already has been caught, shows correct graphics on startup
                if encounter.name in self._caughtPokemon:
                    #append the encounter object to a list to update them all at once instead of updating 1 button 5 times if the pokemon is 5 times in that area
                    alreadyCaught.append(self._caughtPokemon[encounter.name])

                imageLabel.image = pokemonImage
        #remove duplicate names from the list, can keep it as a set as we no longer are using it
        alreadyCaught = set(alreadyCaught)
        for pokemon in alreadyCaught:
            self.changeButtonImage(pokemon)
    
    def catchPokemon(self, pokemon):
        """'catches' the selected pokemon, puts the pokemonTrainer object into a temporary list which get submitted to the area object
         as soon as the capture button at the bottom is selected."""
        #this piece of code is included here because it is primarily for the GUI and not needed at the logic side

        level = 1 #TODO get correct value from widget get method

        #most accurate and higher possibility it was changed last and needs to be checked first
        if pokemon.name in self._temporaryCaptures.keys():
            pokemon = self._temporaryCaptures[pokemon.name]

        elif pokemon.name in self._caughtPokemon.keys():
            pokemon = self._caughtPokemon[pokemon.name]

        else:
            #doesn't exist yet, so create it
            pokemon = EncounteredPokemon(pokemon.name, level, state = 0)
            self._temporaryCaptures[pokemon.name] = pokemon
            print(f"added {pokemon} to temporarycapture list")

        #make sure the value rolls over instead of overshooting
        pokemon.captureStatus = (pokemon.captureStatus + 1) % len(self.states)

        #update GUI button pictures
        self.changeButtonImage(pokemon)
        
        
    def changeButtonImage(self, pokemon):
        buttons = self._buttonDict[pokemon.name]
        for button in buttons:
            button.configure(background = self.colours[pokemon.captureStatus])
            print(f"changed {pokemon.name} to {self.colours[pokemon.captureStatus]}")

    def encounterLabel(self, frame, text, row, column):
        encounterNameLabel = Label(frame, text = text, borderwidth = 2, relief = "flat")
        encounterNameLabel.grid(row = row, column = column, sticky = NSEW)
    
    def updateCapturedPokemon(self):
        #self.area.encounteredPokemon = name
        print(self._temporaryCaptures)
        self.area.encounteredPokemon = self._temporaryCaptures
        #remove all temporary captures, these are not submitted
        self._temporaryCaptures.clear()
        return
        
        print("updating")
        newList = []
        for key, value in self._intvarList.items():
            print(value.get())
            if value.get():
                newList.append(key)
        for pokemon in newList:
            print(pokemon)
            if pokemon not in self._caughtPokemon:
                print("adding pokemon to caughtList")
                self._caughtPokemon[pokemon] = self._areaName
                self.area.caughtPokemon = pokemon
            else:
                print("already caught")
                
        newList = []
    
        print(self._caughtPokemon)
    
    def destroy(self):
        """destroys the window and removes local tkinter references from the global list"""
        self.updateLists()
        self._master.destroy()


            

    
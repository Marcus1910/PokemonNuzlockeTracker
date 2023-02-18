from tkinter import *
from pokemonFrame import PokemonFrame
from trainerPokemon import EncounteredPokemon



class EncounterWindow():
    #for GUI purposes only
    _caughtPokemon = {}

    #used to update buttons and labels across multiple encounterwindow instances
    _pokemonFrames = {}

    def __init__(self, parent, area, save):
        self.area = area
        self._encounterList = area.encounters
        self._areaName = area.name
        self._localPokemonFrames = {} #contains all frames madew in this window
        self._areaFrames = {} #contains all the frames from every area

        self._temporaryCaptures = {}
        #add the pokemon already caught in this area to global caughtlist
        #update should also overwrite duplicates 
        self._caughtPokemon.update(self.area.encounteredPokemon)

        self._master = Toplevel(parent)
        self._master.attributes("-topmost", True)
        self._master.geometry(f"450x600+{parent.winfo_x()}+{parent.winfo_y()}")
        self._master.title(self._areaName)
        self._master.columnconfigure(0, weight = 1)
        self._master.rowconfigure(0, weight = 1)
        #self._master.resizable(False, True) #only strecth in the y direction
        self._masterCanvas = Canvas(self._master)
        self._masterCanvas.grid(row = 0, column = 0, sticky = NSEW)

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
        """removes Frames from class variable lists so you can open the same window without error. Also clears temporaryCaptures"""
        self._temporaryCaptures.clear()
        for name, localframeList in self._localPokemonFrames.items():
            if name in self._pokemonFrames:
                list = self._pokemonFrames[name]
                for frame in localframeList:
                    list.remove(frame)
        
    def makeAreas(self):
        row = 0
        column = 0
        placement = 0
        alreadyCaught = []
        for index, areaType in enumerate(self._encounterList):
            areaTypeName = areaType[0]
            #determine position for the next label, next to it and/or below it
            if (index % 2) == 0:
                placement = 0
                if index > 0:
                    #adjust row to create even surfaces
                    row += max(len(areaType[1]), len(self._encounterList[index-1]))
            else:
                placement = 2

            
            
            areaTypeFrame = Frame(self._canvasFrame, borderwidth = 1, relief = "solid")
            areaTypeFrame.grid(row = row, column = column + placement, columnspan = 2, sticky = NSEW, pady = 1, padx = 1)

            typeLabel = Label(areaTypeFrame, text = areaTypeName, borderwidth = 1, relief = "raised", fg = "blue")
            typeLabel.grid(row = 0, column = 0, columnspan = 5, sticky = NSEW)

            """"
            # indexFrame = Frame(areaTypeFrame)
            # indexFrame.grid(row = 1, column = 0, columnspan = 4, sticky = NSEW)

            # self.textLabel(indexFrame, "catchButton", 0, 0)
            # self.textLabel(indexFrame, "pokemon", 0, 1)
            # self.textLabel(indexFrame, "levels", 0, 2)
            # self.textLabel(indexFrame, "percentage", 0, 3)
            """

            #draw everything inside areaTypeFrame
            for index, encounter in enumerate(areaType[1]):
                #create individual Frames for the pokemon
                indivFrame = PokemonFrame(areaTypeFrame, encounter, areaTypeName)
                indivFrame.grid(row = index + 1, column = 0, columnspan = 4, sticky = NSEW)

                if encounter.name not in self._pokemonFrames:
                    #create an entry with the encounter.name as key
                    self._pokemonFrames[encounter.name] = []
                if encounter.name not in self._localPokemonFrames: #check whether or not it has been created already
                    self._localPokemonFrames[encounter.name] = []
                if areaTypeName not in self._areaFrames:
                    self._areaFrames[areaTypeName] = {}

                #give the pokemonFrame object catchButton a command   
                indivFrame.catchButton.configure(command = lambda pokemon = encounter, name = areaTypeName: [self.catchPokemon(pokemon, name)])

                self._pokemonFrames[encounter.name].append(indivFrame)
                self._localPokemonFrames[encounter.name].append(indivFrame)
                #each pokemon only appears once in the separated area
                self._areaFrames[areaTypeName][encounter.name] = indivFrame

                #checks whether or not the pokemon already has been caught, shows correct graphics on startup
                if encounter.name in self._caughtPokemon:
                    #append the encounter object to a list to update them all at once instead of updating 1 button 5 times if the pokemon is 5 times in that area
                    alreadyCaught.append(self._caughtPokemon[encounter.name])

        #remove duplicate names from the list, can keep it as a set as we no longer are using it
        alreadyCaught = set(alreadyCaught)
        for pokemon in alreadyCaught:
            self.changeButtonImage(pokemon)
    
    def catchPokemon(self, pokemon, areaTypeName):
        """'catches' the selected pokemon, puts the pokemonTrainer object into a temporary list which get submitted to the area object
         as soon as the capture button at the bottom is selected."""
        frame = self._areaFrames[areaTypeName][pokemon.name]
        
        level = frame.level.get()

        #most accurate and higher possibility it was changed last and needs to be checked first
        if pokemon.name in self._temporaryCaptures.keys():
            pokemon = self._temporaryCaptures[pokemon.name]

        elif pokemon.name in self._caughtPokemon.keys():
            pokemon = self._caughtPokemon[pokemon.name]

        else:
            #doesn't exist yet, so create it
            pokemon = EncounteredPokemon(pokemon.name, level, state = 0)
            self._temporaryCaptures[pokemon.name] = pokemon

        #synch the capturestatus
        pokemon.captureStatus = frame.updateState(pokemon.captureStatus)
        print("pokemon status: ", pokemon.captureStatus)

        #update GUI button pictures
        self.changeButtonImage(pokemon)
        
        
    def changeButtonImage(self, pokemon):
        frames = self._pokemonFrames[pokemon.name]
        print(len(frames))
        for frame in frames:
            print(frame)
            frame.updateCatchButton(pokemon.captureStatus) 
    
    def updateCapturedPokemon(self):
        """update the area.encounteredPokemon attribute with all the temporaryCaptures that are caught"""
        #self.area.encounteredPokemon = name
        for pokemon in self._temporaryCaptures.values():
            #not actually captured, or misclick
            if pokemon.captureStatus == 0:
                #try except in case it doesn't exist
                try:
                    del self.area.encounteredPokemon[pokemon.name]
                except KeyError:
                    pass
            else:    
                self.area.encounteredPokemon[pokemon.name] = pokemon
        #remove all temporary captures
        self._temporaryCaptures.clear()
    
    def destroy(self):
        """destroys the window and removes local tkinter references from the global list"""
        self.updateLists()
        self._master.destroy()


            

    
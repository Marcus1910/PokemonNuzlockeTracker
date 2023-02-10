from tkinter import *
from PIL import Image, ImageTk
import os


class EncounterWindow():
    #for GUI purposes only
    _caughtPokemon = {}
    
    _labelTextDict = {}
    _labelObjDict = {}
    _buttonDict = {}
    _spriteFolder = os.path.join(os.path.dirname(os.getcwd()), f"images/sprites")
    _pokemonSpritesFolder = os.path.join(_spriteFolder, f"pokemon")

    def __init__(self, parent, area, save):
        self.area = area
        self._encounterList = area.encounters
        self._areaName = area.name
        self._localLabelObjDict = {}
        self._localButtonDict = {}

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

        #on window deletion
        self._master.protocol("WM_DELETE_WINDOW", lambda : [self.updateLists(), self._master.destroy()])

        self.makeAreas()

    def updateLists(self):
        """removesButtons / labels from class variable lists so you can open the same window without error"""
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
                if encounter.name  not in self._labelTextDict:
                    self._labelTextDict[encounter.name] = StringVar()
                    self._labelTextDict[encounter.name].set("catch")
                    self._buttonDict[encounter.name] = []
                    self._labelObjDict[encounter.name] = []
                if encounter.name not in self._localButtonDict:
                    self._localButtonDict[encounter.name] = []
                    self._localLabelObjDict[encounter.name] = []# create empty list to store all labels for pokemon

                #checkbutton    
                catchButton = Button(areaTypeFrame, textvariable = self._labelTextDict[encounter.name], command = lambda name = encounter.name : [self.changeColour(name)])
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

                imageLabel.image = pokemonImage
    
    def changeColour(self, name):
        print(name)
        x = self._labelObjDict[name]
        for i in x:
            i.configure(bg = "green")
        buttons = self._buttonDict[name]
        for button in buttons:
            button.configure(bg = "red")
            print(button)

    def encounterLabel(self, frame, text, row, column):
        encounterNameLabel = Label(frame, text = text, borderwidth = 2, relief = "flat")
        encounterNameLabel.grid(row = row, column = column, sticky = NSEW)
    
    def updateCapturedPokemon(self):
        pass
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


            

    
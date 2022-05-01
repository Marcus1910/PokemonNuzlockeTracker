from PIL import ImageTk
import PIL.Image
from tkinter import *

from templateWindow import TemplateWindow

class MainWindow(TemplateWindow):
    """window is 5 by 5"""
    def __init__(self, x, y, game):
        super().__init__(x, y)      
        self._game = game
        self._master.title(f"{self._game}")
        self._listOfAreas = []
        self._areaNames = []
        self._listOfTrainers = []
        self._trainerNames = ["choose an area first"]
        self.getAreas()

        self._numberOfBadges = StringVar()
        self._numberOfBadges.set("number of badges")
        self._badgesMenu = OptionMenu(self._master, self._numberOfBadges, *list(range(0,9)))
        self._badgesMenu.grid(row=0, column=0,rowspan=1, columnspan=1, sticky=NW) 

        self._itemFrame = Frame(self._master, bg= "blue")
        self._itemFrame.grid(row=0, column=2,rowspan=25, sticky = NSEW)
        self._itemButton = Button(self._itemFrame, text="Items komen hier terecht")
        self._itemButton.grid(row=0,column=0,sticky=NSEW)

        self._trainerFrame = Frame(self._master)
        self._trainerFrame.grid(row=0, column=1, rowspan=8, columnspan = 1, sticky = N)
        self._trainerFrame.rowconfigure(0, weight = 2)
        self._trainerFrame.columnconfigure(0, weight = 2)

        self._selectedTrainer = StringVar()
        self._selectedTrainer.set("which trainer do you want to see")
        self._selectedTrainer.trace("w", self.getPokemon)
        self._trainerMenu = OptionMenu(self._trainerFrame, self._selectedTrainer, *self._trainerNames, command = self.getPokemon)
        self._trainerMenu.grid(row=0, column = 0, columnspan = 3, sticky = N)

        self._indivTrainerFrame = Frame(self._trainerFrame)
        self._indivTrainerFrame.grid(row = 1, column = 0, columnspan = 3, sticky = N)
        self._indivTrainerFrame.rowconfigure(0, weight = 2)
        self._indivTrainerFrame.columnconfigure(0, weight = 2)

        self._exportToShowdownButton = Button(self._trainerFrame, text = "export to showdown")
        self._exportToShowdownButton.grid(row = 8, column =0, columnspan = 3, sticky = NSEW)

        self._selectedArea = StringVar()
        self._selectedArea.set("choose an Area")
        self._areaMenu = OptionMenu(self._master, self._selectedArea, *self._areaNames, command = self.getTrainers)
        self._areaMenu.grid(row=0, column=4, sticky=NW)

        self._exitButton = Button(self._master, text = "exit", command = self.exit)
        self._exitButton.grid(row=4, column = 0, sticky=SW)

        self._backButton = Button(self._master, text = "back", command = self.createGameMenu)
        self._backButton.grid(row=4, column=4, sticky=SE)

        self.update()
        self.run()

    def getAreas(self):
        """determine which game should be called and retrieve the correct information"""
        from main import SacredGold
        self._game = SacredGold()
        self._listOfAreas = self._game.areaList
        for area in self._listOfAreas:
            self._areaNames.append(area.name)
    
    def getTrainers(self, areaName):
        """empty and update trainerlist for the option menu depending on the selected area"""
        menu = self._trainerMenu["menu"]
        #reset lists
        self._trainerNames = []
        self._listOfTrainers = []
        for area in self._listOfAreas:
            if areaName in area.name:
                self._listOfTrainers = area.trainers
                for trainer in area._trainers:
                    self._trainerNames.append(trainer.name)
        #empty the optionmenu
        menu.delete(0, "end")
        for trainer in self._trainerNames:
            menu.add_command(label = trainer, command = lambda value = trainer: self._selectedTrainer.set(value))
    
    def getPokemon(self, *args):
        trainerName = self._selectedTrainer.get()
        #print(self._listOfTrainers)
        if len(self._listOfTrainers) == 0:
            print("This trainer has no pokemon")
        else:
            for trainer in self._listOfTrainers:
                if trainerName in trainer.name:
                    self.deletePokemonDisplay()
                    for index, pokemon in enumerate(trainer.pokemon):
                        self.displayPokemon(pokemon, index)

    def deletePokemonDisplay(self):
        """delete all listboxs etc in indivtrainerframe"""
        for label in self._indivTrainerFrame.winfo_children():
            label.destroy()

    def displayPokemon(self, pokemon, index):
        """look for photo of the pokemon and at the pokemon data to the gui"""
        photo = "66.png"
        pokemonImg = ImageTk.PhotoImage(PIL.Image.open(photo))
        pokemonPhoto = Label(self._indivTrainerFrame, image = pokemonImg)
        pokemonPhoto.grid(row = index, column = 0, sticky = N)
        
        dataBox = Listbox(self._indivTrainerFrame, height = 4)
        dataBox.grid(row = index, column = 1, sticky = N)
        dataBox.insert(1, f"{pokemon._name}")
        dataBox.insert(2, f"Ability: {pokemon._ability}")
        dataBox.insert(3, f"Item: {pokemon._heldItem}")
        dataBox.insert(4, f"Gender: {pokemon._gender}")

        moveBox = Listbox(self._indivTrainerFrame, height = 4)
        moveBox.grid(row = index, column = 2, sticky = N)
        for index, move in enumerate(pokemon.moves):
            moveBox.insert(index, move)

        pokemonPhoto.image = pokemonImg


    def createGameMenu(self):
        from GUI import SelectGameWindow
        self.stop()
        self.exit()
        SelectGameWindow()





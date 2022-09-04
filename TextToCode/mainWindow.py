from tkinter import *
import os
from tkinter import ttk

from AddDeleteAttributeWindows import AddDeleteTrainerWindow

from templateWindow import TemplateWindow
from encounterWindow import EncounterWindow
from games.trainer import Trainer
#from attributeWindow import TrainerWindow, ItemWindow
from games.item import Item

class MainWindow(TemplateWindow):
    def __init__(self, x, y, game):
        super().__init__(x, y)   
        self._game = game
        self._master.title(f"{self._game}")
        self._listOfAreas = []
        self._areaNames = []
        self._listOfTrainers = []
        self._listOfItems = []
        #optionmenu needs list with a minimum of 1 item
        self._trainerNames = [None]
        self.getAreas()

        """number of badges"""
        self._numberOfBadges = IntVar()
        self._numberOfBadges.set(0)
        self._badgesMenu = OptionMenu(self._master, self._numberOfBadges, *list(range(0,9)), command = self.changeAreaList)
        self._badgesMenu.grid(row=0, column=0,rowspan=1, columnspan=1, sticky=NW) 

        """item frames"""
        self._itemFrame = Frame(self._master)
        self._itemFrame.grid(row=0, column=4,rowspan = 25, columnspan = 1, sticky = N)
        self._itemFrame.rowconfigure(0, weight = 2)
        self._itemFrame.columnconfigure(0, weight = 2)

        self._indivItemFrame = Frame(self._itemFrame)
        self._indivItemFrame.grid(row = 1, column = 0, columnspan = 4, sticky = N)
        self._indivItemFrame.rowconfigure(0, weight = 2)
        self._indivItemFrame.columnconfigure(0, weight = 2)


        self._itemLabel = Label(self._itemFrame, text="Available Items")
        self._itemLabel.grid(row=0,column=0,sticky=N)

        """trainer frames"""
        self._trainerFrame = Frame(self._master)
        self._trainerFrame.grid(row=0, column=1, rowspan=10, columnspan = 3, sticky = N)
        self._trainerFrame.rowconfigure(0, weight = 2)
        self._trainerFrame.columnconfigure(0, weight = 2)

        self._selectedTrainer = StringVar()
        self._selectedTrainer.set("which trainer do you want to see")
        self._selectedTrainer.trace_add("write", self.getPokemon)
        self._trainerMenu = OptionMenu(self._trainerFrame, self._selectedTrainer, *self._trainerNames, command = self.getPokemon)
        self._trainerMenu.grid(row=0, column = 0, columnspan = 3, sticky = N)

        self._indivTrainerFrame = Frame(self._trainerFrame)
        self._indivTrainerFrame.grid(row = 1, column = 0, columnspan = 3, sticky = N)
        self._indivTrainerFrame.rowconfigure(0, weight = 2)
        self._indivTrainerFrame.columnconfigure(0, weight = 2)

        """trainer buttons"""
        self._addTrainerButton = Button(self._trainerFrame, text = "add a trainer", bd = 3, font = self._font, command = self.addTrainer)
        self._addTrainerButton.grid(row = 8, column = 0, sticky = NSEW)

        self._editTrainerButton = Button(self._trainerFrame, text = "edit a trainer", bd = 3, font = self._font)#, command =self.editTrainer)
        self._editTrainerButton.grid(row = 8, column = 1, sticky = NSEW)

        self._deleteTrainerButton = Button(self._trainerFrame, text = "delete a trainer", bd = 3, font = self._font, command = self.deleteTrainer)
        self._deleteTrainerButton.grid(row = 8, column = 2, sticky = NSEW)

        """showdown buttons"""
        self._exportToShowdownButton = Button(self._trainerFrame, text = "export current trainer to showdown", bd = 5, font = self._font, command = self.showdownExport)
        self._exportToShowdownButton.grid(row = 9, column =0, columnspan = 3, sticky = NSEW)

        self._exportAllToShowdownButton = Button(self._trainerFrame, text = "export all available trainer data to showdown", bd = 5, font = self._font)
        self._exportAllToShowdownButton.grid(row = 10, column =0, columnspan = 3, sticky = NSEW)

        """selected Area"""
        self._areaFrame = Frame(self._master)
        self._areaFrame.grid(row = 0, column = 5, sticky = N)

        self._selectedArea = StringVar()
        self._selectedArea.set("choose an Area")
        #area is the _selectedArea variable
        self._areaMenu = ttk.Combobox(self._areaFrame, textvariable = self._selectedArea, values = self._areaNames)#, command = lambda area: [self.getTrainers(area), self.getItems(area)])
        self._areaMenu.grid(row=0, column=5, sticky=NSEW)
        self._areaMenu['state'] = 'readonly'
        self._areaMenu.bind("<<ComboboxSelected>>", lambda area = self._areaMenu.get(): [self.getTrainers(area), self.getItems(area)])

        self._showWildEncounterButton = Button(self._areaFrame, text = "Encounters", command = self.showEncounters)
        self._showWildEncounterButton.grid(row = 1, column = 5, sticky = NSEW)

        """exit buttons and main loop"""
        self._exitButton = Button(self._master, text = "exit", command = self.exit)
        self._exitButton.grid(row=4, column = 0, sticky=SW)

        self._backButton = Button(self._master, text = "back", command = self.createGameMenu)
        self._backButton.grid(row=4, column=5, sticky=SE)

        self._exportToShowdownButton.configure(state = DISABLED)
        #self.changeTrainerButtonState(DISABLED)
        self.update()
        self.run()

    def showEncounters(self):
        currentArea = self._areaMenu.get()
        print(currentArea)
        print("showing")
        for area in self._listOfAreas:
            if area.name == currentArea:
                print(area.encounters)
                encounterWindow = EncounterWindow(area.encounters, self._master)
                break
        #print(self._listOfAreas)

    def getAreas(self):
        """determine which game should be called and retrieve the correct information TODO replace with call to /games/game"""
        from main import SacredGold
        self._game = SacredGold()
        self._listOfAreas = self._game.areaList
        for area in self._listOfAreas:
            self._areaNames.append(area.name)
    
    def changeAreaList(self, *args):
        badges = self._numberOfBadges.get()
        #TODO sort list on number of badges
        pass
    
    def getTrainers(self, event):
        """empty and update trainerlist for the option menu depending on the selected area"""
        #enable to select trainer and export buttons
        #self.changeTrainerButtonState(NORMAL)
        areaName = event.widget.get()
        menu = self._trainerMenu["menu"]
        #reset lists
        self._trainerNames = []
        self._listOfTrainers = []
        for area in self._listOfAreas:
            if areaName in area.name:
                self._listOfTrainers = area.trainers

                if len(area.trainers) == 0:
                    self._selectedTrainer.set("this route has no trainers, please add one with the add trainer button")

                for trainer in area._trainers:
                    self._trainerNames.append(trainer.name)
        #empty the optionmenu
        menu.delete(0, "end")
        for trainer in self._trainerNames:
            menu.add_command(label = trainer, command = lambda value = trainer: self._selectedTrainer.set(value))
        
    
    def getPokemon(self, *args):
        """get the pokemon from a selected trainer"""
        trainerName = self._selectedTrainer.get()
        self._exportToShowdownButton.configure(state = NORMAL)
        #print(self._listOfTrainers)
        if len(self._listOfTrainers) == 0:
            print("This trainer has no pokemon")
        else:
            if trainerName is None:
                return
            for trainer in self._listOfTrainers:
                if trainerName in trainer.name:
                    self.deletePokemonDisplay()
                    for index, pokemon in enumerate(trainer.pokemon):
                        self.displayPokemon(pokemon, index)
    
    def getItems(self, event):
        areaName = event.widget.get()
        self._listOfItems = []
        for area in self._listOfAreas:
            if areaName == area.name:
                self.deleteItemDisplay()
                self._listOfItems = area._items
                self.displayItems()

    def deletePokemonDisplay(self):
        """delete all listboxs etc in indivtrainerframe"""
        for label in self._indivTrainerFrame.winfo_children():
            label.destroy()
        
    def displayPokemon(self, pokemon, index):
        """look for photo of the pokemon and add the pokemon to the gui"""
        folderPath = os.path.join(os.getcwd(), 'sprites/pokemon')
        photo = os.path.join(folderPath, pokemon.name + '.png')
        #check if pokemon name is correct else display '?' png
        try:
            pokemonImg = PhotoImage(file = photo)
        except TclError:
            photo = os.path.join(folderPath, '0.png')
            pokemonImg = PhotoImage(file = photo)
        
        #pokemonImg = ImageTk.PhotoImage(PIL.Image.open(photo))
        pokemonPhoto = Label(self._indivTrainerFrame, image = pokemonImg)
        pokemonPhoto.grid(row = index, column = 0, sticky = N)
        
        dataBox = Listbox(self._indivTrainerFrame, height = 4)
        dataBox.grid(row = index, column = 1, sticky = N)
        dataBox.insert(1, f"{pokemon._name} lvl {pokemon._level}")
        dataBox.insert(2, f"Ability: {pokemon._ability}")
        dataBox.insert(3, f"Item: {pokemon._heldItem}")
        dataBox.insert(4, f"Gender: {pokemon._gender}")

        moveBox = Listbox(self._indivTrainerFrame, height = 4)
        moveBox.grid(row = index, column = 2, sticky = N)
        for index, move in enumerate(pokemon.moves):
            moveBox.insert(index, move)
        #prevent garbage collection
        pokemonPhoto.image = pokemonImg
    
    def deleteItemDisplay(self):
        for label in self._indivItemFrame.winfo_children():
            label.destroy()

    def displayItems(self):
        itemScrollbar = Scrollbar(self._indivItemFrame)
        itemScrollbar.grid(row = 0, column = 1, sticky = NS)
        itemBox = Listbox(self._indivItemFrame, yscrollcommand = itemScrollbar.set)
        itemBox.grid(row = 0, column = 0)
        for item in self._listOfItems:
            itemBox.insert(END, item.name)
        itemScrollbar.configure(command = itemBox.yview)
    
    def addTrainer(self):
        """add a trainer to trainer list"""
        #disable add/ edit and delete button
        #open new window which containes current trainers
        #back button which closes window
        #send name to main program
        newWindow = AddDeleteTrainerWindow(self._master, self._listOfTrainers, self._selectedArea.get(), False, "trainer")
        print(f"adding Trainer to {self._selectedArea.get()}")
        pass
    

    def editTrainer(self):
        #self._newWindow = TrainerWindow(self._master, self._listOfTrainers)
        pass

    def deleteTrainer(self):
        """delete a trainer from trainer list"""
        newWindow = AddDeleteTrainerWindow(self._master, self._listOfTrainers, self._selectedArea.get(), True, "trainer")
        print(f"deleting trainer")


    def showdownExport(self):
        """grabs current trainer selected and converts its data to showdown format"""
        chosenTrainer = self._selectedTrainer.get()
        for trainer in self._listOfTrainers:
            if chosenTrainer == trainer.name:
                with open('showdown.txt', 'w') as outputFile:
                    #TODO rewrite to showdown format
                    pass
                break

    def createGameMenu(self):
        from GUI import SelectGameWindow
        self.stop()
        self.exit()
        SelectGameWindow()




# def addDeleteAttribute(self, button, list, delete, windowtype, itemType):
    #     button.configure(state = DISABLED)
    #     newWindow = windowtype(self._master, list, delete)
    #     #TODO find better way to do this
    #     newWindow._submitButton.wait_variable(newWindow._validated)
    #     newTrainerName = newWindow._newAttribute.get()
    #     newTrainer = itemType(newTrainerName)
    #     newWindow.destroy()
    #     button.configure(state = NORMAL)
    #     return newTrainer

    # def addTrainer(self):
    #     trainer = self.addDeleteAttribute(self._addTrainerButton, self._listOfTrainers, False, TrainerWindow, Trainer)
    #     self._listOfTrainers.append(trainer)
    #     #update optionmenu list
    #     self.getTrainers(self._selectedArea.get())
    
    # def deleteTrainer(self):
    #     trainer = self.addDeleteAttribute(self._deleteTrainerButton, self._listOfTrainers, True, TrainerWindow, Trainer)
    #     for index ,trainers in enumerate(self._listOfTrainers):
    #         if trainer.name == trainers.name:
    #             self._listOfTrainers.pop(index)
    #     self.getTrainers(self._selectedArea.get())
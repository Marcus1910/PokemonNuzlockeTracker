from nuzlockeScreen import NuzlockeScreen
from detailedPokemonBox import DetailedPokemonBox
from editTrainerBox import EditTrainerBox
from loggerConfig import logger

from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

import games as gm
import os

class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        #need areaObject to update trainers and add trainers
        self.areaObject = None
        #trainer Object for current trainer
        self.currentTrainerObject = None
        self.trainers = None
        #spinner to select trainer with label to edit trainer
        self.trainerSpinnerBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.04)
        #create trainerspinner
        self.defaultTrainerText = "Select Trainer"
        self.trainerSpinner = Spinner(text = self.defaultTrainerText, values = ["New Trainer"], size_hint_x = 0.75)
        self.trainerSpinner.bind(text = self.updateTrainerBox)
        self.trainerSpinner.background_color = gm.opaque
        #create buttons that edits trainer, logic is inside of editTrainerBox
        self.editTrainerButton = Button(text = "edit", size_hint_x = 0.25)
        #disable button till a trainer is selected
        self.editTrainerButton.disabled = True
        self.editTrainerButton.background_color = gm.opaque
        self.editTrainerButton.bind(on_press = self.editTrainer) 

        #box that contains global view, all pokemon from trainer
        self.trainerBox = BoxLayout(size_hint_y = 0.71, orientation = "vertical")

        #used for detailed view
        self.detailedPokemonBox = DetailedPokemonBox(screen = self, orientation = "vertical", size_hint_y = 0.71)
    
        #used to edit/add trainers from/to area
        self.editTrainerBox = EditTrainerBox(trainerScreen = self, orientation = "horizontal", size_hint_y = 0.71)

        self.viewBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.05, padding = (0, 0, 0, 10))
        self.viewLabel = Label(text = "view mode: ", size_hint_x = 0.15, padding = (0, 0, 50, 0))
        self.viewSpinner = Spinner(values = ["global", "detailed"], size_hint_x = 0.15, pos_hint = {"right": 1}, padding = (10, 0, 0, 0), text_autoupdate = True)
        self.viewSpinner.bind(text = self.updateTrainerBox)



        self.spriteFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")

        self.trainerSpinnerBox.add_widget(self.trainerSpinner)
        self.trainerSpinnerBox.add_widget(self.editTrainerButton)

        self.viewBox.add_widget(self.viewLabel)
        self.viewBox.add_widget(self.viewSpinner)

        self.layout.add_widget(self.trainerSpinnerBox)
        self.layout.add_widget(self.viewBox)
        self.layout.add_widget(self.trainerBox)
    
    def areaChanged(self, spinner, text):
        super().areaChanged(spinner, text)
        self.updateTrainers()
        self.trainerSpinner.text = self.defaultTrainerText
        self.currentTrainerObject = None
        self.areaObject = self.manager.currentArea

    def updateTrainers(self):
        #disable edit button for trainers till trainer has been found in showTrainers function
        self.editTrainerButton.disabled = True
        spinnerList = []
        areaObject = self.manager.currentArea
        self.trainers = areaObject.trainers
        if len(self.trainers) > 0:
            spinnerList = [trainer for trainer in self.trainers.keys()]
        spinnerList.append("New Trainer")
        self.trainerSpinner.values = spinnerList
        logger.debug(f"loaded new Trainers into spinner {spinnerList}")
        self.clearTrainerBox()
    
    def updateTrainerBox(self, spinner, text):
        """function that gets called by trainerspinner and viewSpinner, changes trainer and UI"""
        #disable edit button for trainers till trainer has been found in showTrainers function
        self.editTrainerButton.disabled = True
        #return self.currentTrainerObject to None so it is clean
        self.currentTrainerObject = None
        self.changeTrainerSpinnerColor(gm.opaque)
        self.clearTrainerBox()
        self.detailedPokemonBox.clearLayout()
        self.editTrainerBox.clearLayout()
        selectedTrainer = self.trainerSpinner.text
        viewMode = self.viewSpinner.text
        self.showTrainer(selectedTrainer, viewMode)
    
    def showTrainer(self, selectedTrainer, view):
        """selects correct trainer object and choses correct UI to display pokemon"""
        if selectedTrainer == self.defaultTrainerText:
            #default value for trainerspinner so do nothing
            return
        if selectedTrainer == "New Trainer":
            #fill trainerBox with new window to add new trainer
            self.addNewTrainer()
            return
        try:
            self.currentTrainerObject = self.trainers[selectedTrainer]
        except ValueError as e:
            #trainer not found
            logger.error(f"{selectedTrainer} has not been found")
            return
            
        #change the color of the trainer spinner based on defeated status
        color = gm.green if self.currentTrainerObject.defeated else gm.red
        self.changeTrainerSpinnerColor(color)
        #trainer has been found, unlock edit mode for trainer
        self.editTrainerButton.disabled = False

        #change trainerbox layout to selected view
        self.changeView(view)

    def changeTrainerSpinnerColor(self, color: tuple):
        """changes trainerspinner color to green if trainer is defeated else turns to red"""
        newColor = color[0:3] + (gm.opaque[3],)
        self.trainerSpinner.background_color = newColor
        
    def changeView(self, view):
        """function that changes the view to detailed or global"""
        self.editTrainerBox.clearLayout()
        if view == "global":
            self.showGlobalView()
        elif view == "detailed":
            self.showDetailedView()
        else:
            logger.error(f"{view} is not a correct view")
  
    def clearTrainerBox(self):
        """removes self.detailedPOkemonBox or pokemonBox from self.trainerBox"""
        self.trainerBox.clear_widgets()
        logger.debug(f"clearing trainerBox")

    def showGlobalView(self):
        for index, pokemonObject in enumerate(self.currentTrainerObject.pokemon):
            #gather pokemon data and put it in Labels
            pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = (1 - 0.05)/ (len(self.currentTrainerObject.pokemon)), padding = (0, 0, 0, 10))
            #create Image with name underneath
            imageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
            pokemonImage = Image(source = os.path.join(self.spriteFolder, f"{pokemonObject.name.lower()}.png"))
            pokemonImage.fit_mode = "contain"
            nameLevelLabel = Label(text = f"{pokemonObject.name} lvl {pokemonObject.level}", color = self.standardColor, pos_hint = {"right": 1})
            
            itemAbilityBox = BoxLayout(orientation = "vertical", size_hint_x = 0.1)
            abilityInput = Label(text = f"{pokemonObject.ability}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"top" : 1})
            heldItemInput = Label(text = f"{pokemonObject.heldItem}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"bottom" : 1})
            
            moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)

            for moveIndex in range(4): 
                moveSlot = Label(text = f"Not revealed", color = self.standardColor)
                if moveIndex < len(pokemonObject.moves):
                    moveSlot.text = f"{pokemonObject.moves[moveIndex]}"
                moveBox.add_widget(moveSlot)

            imageBox.add_widget(pokemonImage)
            imageBox.add_widget(nameLevelLabel)
            pokemonBox.add_widget(imageBox)

            itemAbilityBox.add_widget(abilityInput)
            itemAbilityBox.add_widget(heldItemInput)

            pokemonBox.add_widget(itemAbilityBox)
            pokemonBox.add_widget(moveBox)
        
            self.trainerBox.add_widget(pokemonBox)
        logger.debug("created global view")
    
    def showDetailedView(self):
        self.detailedPokemonBox.buildLayout(self.currentTrainerObject)
        self.trainerBox.add_widget(self.detailedPokemonBox)

    def editTrainer(self, *args):
        """gives trainerobject to self.editTrainerBox for editing"""
        logger.debug(f"editing {self.currentTrainerObject.name}")
        self.editTrainerBox.buildLayout(self.currentTrainerObject)
        #clear the previous layout
        self.clearTrainerBox()
        #show new layout
        self.trainerBox.add_widget(self.editTrainerBox)

    def on_leave(self):
        super().on_leave()
        logger.debug("saving pokemon")
        self.detailedPokemonBox.savePokemon()
    
    def addNewTrainer(self):
        """displays the edittrainerBox for a new trainer to be added"""
        logger.debug("create new Trainer screen")
        #no object as we want to create a new object
        self.editTrainerBox.buildLayout()
        self.trainerBox.add_widget(self.editTrainerBox)

    
    def addTrainerToGame(self, trainerObject):
        """Add trainerObject to the gameObject, function called in the editTrainer box"""
        logger.debug(f"Adding {trainerObject.name} to {self.areaObject.name}")
        self.areaObject.addTrainer(trainerObject)
        #refresh listbox
        self.updateTrainers()
    
    def editTrainerObject(self, trainerObject, newName):
        """Edit the trainerObject from the game"""
        #NewName is either the name or None, None is the default value in the called function
        logger.debug(f"editing {trainerObject.name} in {self.areaObject.name}")
        self.areaObject.editTrainer(trainerObject, newName)
        self.updateTrainers()
        #change text from the spinner then call the function which would be called with a normal interaction.
        self.trainerSpinner.text = trainerObject.name if newName == None else newName
        self.updateTrainerBox(self.trainerSpinner, self.trainerSpinner.text)
        




        





from nuzlockeScreen import NuzlockeScreen
from detailedPokemonBox import DetailedPokemonBox
from editTrainerBox import EditTrainerBox
from addTrainerBox import AddTrainerBox, TrainerDialog
from loggerConfig import logger

from expandableBox import ExpandableTrainerBox

from kivy.uix.spinner import Spinner
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog

import games as gm
import os

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton

class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        #need areaObject to update trainers and add trainers
        self.areaObject = None
        #trainer Object for current trainer
        self.currentTrainerObject = None
        self.trainers = None 

        self.newTrainerDialog = TrainerDialog()

        #box that contains all expandabletrainerboxes
        self.trainerBox = BoxLayout(size_hint_y = 0.61, orientation = "vertical")

        self.newTrainerButton = Button(text = "add new Trainer", on_release = self.addNewTrainer, size_hint_y = 0.1)

        self.spriteFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")

        self.screenBox.add_widget(self.trainerBox)
        self.screenBox.add_widget(self.newTrainerButton)
    
    def areaChanged(self, spinner, text) -> None:
        if not super().areaChanged(spinner, text):
            #invalid area, should not be able to add new Trainer to it
            self.newTrainerButton.disabled = True
            return
        self.updateTrainers()
        self.currentTrainerObject = None
        self.areaObject = self.manager.currentArea
        self.newTrainerButton.disabled = False
    
    def on_leave(self):
        super().on_leave()

    def updateTrainers(self):
        """reloads the expandabletrainerboxes with updated trainer dict"""
        areaObject = self.manager.currentArea
        self.trainers = areaObject.trainers
        logger.debug(f"loaded trainers: {self.trainers}")
        self.clearTrainerBox()
        emptyBoxes = 4 - len(self.trainers)
        print(emptyBoxes)
        for trainer in self.trainers:
            box = ExpandableTrainerBox(trainer)
            self.trainerBox.add_widget(box)
        
        for emptyBox in range(emptyBoxes):
            box = BoxLayout()
            self.trainerBox.add_widget(box)
  
    def clearTrainerBox(self):
        """removes all widgets from trainerBox"""
        self.trainerBox.clear_widgets()
        logger.debug(f"clearing trainerBox")

    def addNewTrainer(self, instance):
        """displays the edittrainerBox for a new trainer to be added"""
        logger.debug("create dialog to add new trainer")
        self.newTrainerDialog.open()

    
    def addTrainerToGame(self, trainerObject):
        """Add trainerObject to the gameObject, function called in the editTrainer box"""
        logger.debug(f"Adding {trainerObject.name} to {self.areaObject.name}")
        if self.areaObject.addTrainer(trainerObject):
            logger.debug("added trainer")
        else:
            logger.debug("error ocured adding trainer")
            #update self.trainerobject to None, otherwise next call will execute edittrainer
            self.editTrainerBox.trainerObject = None
            return
        self.updateTrainers()
        #change text from the spinner then call the function which would be called with a normal interaction

    def editTrainerObject(self, trainerObject, newName):
        """Edit the trainerObject from the game"""
        #NewName is either the name or None, None is the default value in the called function
        logger.debug(f"editing {trainerObject.name} in {self.areaObject.name}")
        if self.areaObject.editTrainer(trainerObject, newName):
            logger.debug("edit done succesfully, redrawing screen")
        else:
            logger.debug("error occurred")
            return
        self.updateTrainers()

    def removeTrainer(self, trainerName):
        """remove trainer from game object using its name"""
        if self.areaObject.removeTrainer(trainerName):
            logger.debug("removed Trainer sucessfully")
        else:
            logger.debug("error ocurred during removal")
            return

        self.updateTrainers()

    # def showGlobalView(self):
    #     if len(self.currentTrainerObject.pokemon) == 0:
    #         #add new pokemon by showing empty detailedpokemonBox
    #         # addPokemonLabel = Label(text = "No pokemon found", size_hint_y = 0.6)
    #         # addPokemonButton = Button(text = "add pokemon", on_press = self.addFirstPokemon, size_hint_y = 0.4)
    #         # self.trainerBox.add_widget(addPokemonLabel)
    #         # self.trainerBox.add_widget(addPokemonButton)
    #         return
        
    #     for index, pokemonObject in enumerate(self.currentTrainerObject.pokemon):
    #         #gather pokemon data and put it in Labels
    #         pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = (1 - 0.05)/ (len(self.currentTrainerObject.pokemon)), padding = (0, 0, 0, 10))
    #         #create Image with name underneath
    #         imageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
    #         pokemonImage = Image(source = os.path.join(self.spriteFolder, f"{pokemonObject.name.lower()}.png"))
    #         pokemonImage.fit_mode = "contain"
    #         nameLevelLabel = MDLabel(text = f"{pokemonObject.name} lvl {pokemonObject.level}", color = self.standardColor, pos_hint = {"right": 1})
            
    #         itemAbilityBox = BoxLayout(orientation = "vertical", size_hint_x = 0.1)
    #         abilityInput = MDLabel(text = f"{pokemonObject.ability}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"top" : 1})
    #         heldItemInput = MDLabel(text = f"{pokemonObject.heldItem}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"bottom" : 1})
            
    #         moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)

    #         for moveIndex in range(4): 
    #             moveSlot = MDLabel(text = f"Not revealed", color = self.standardColor)
    #             if moveIndex < len(pokemonObject.moves):
    #                 moveSlot.text = f"{pokemonObject.moves[moveIndex]}"
    #             moveBox.add_widget(moveSlot)

    #         imageBox.add_widget(pokemonImage)
    #         imageBox.add_widget(nameLevelLabel)
    #         pokemonBox.add_widget(imageBox)

    #         itemAbilityBox.add_widget(abilityInput)
    #         itemAbilityBox.add_widget(heldItemInput)

    #         pokemonBox.add_widget(itemAbilityBox)
    #         pokemonBox.add_widget(moveBox)
        
    #         self.trainerBox.add_widget(pokemonBox)
    #     logger.debug("created global view")
    
    # def showDetailedView(self):
    #     self.detailedPokemonBox.buildLayout(self.currentTrainerObject)
    #     self.trainerBox.add_widget(self.detailedPokemonBox)

    # def editTrainer(self, *args):
    #     """gives trainerobject to self.editTrainerBox for editing"""
    #     logger.debug(f"editing {self.currentTrainerObject.name}")
    #     self.editTrainerBox.buildLayout(self.currentTrainerObject)
    #     #clear the previous layout
    #     self.clearTrainerBox()
    #     #show new layout
    #     self.trainerBox.add_widget(self.editTrainerBox)
from nuzlockeScreen import NuzlockeScreen
from trainerDialog import AddTrainerDialog
from loggerConfig import logger
from expandableBox import ExpandableTrainerBox
from transparentButton import TransparentButton

from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

import games as gm
from games import pokemonSprites, trainerSprites, itemSprites
import os

class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        #need areaObject to update trainers and add trainers
        self.areaObject = None
        #trainer Object for current trainer
        self.currentTrainerObject = None
        self.trainers = None 

        self.newTrainerDialog = AddTrainerDialog(self.addTrainerToGame)

        #box that contains all expandabletrainerboxes
        self.trainerBox = GridLayout(size_hint_y = None, cols = 1)
        self.trainerBoxScroll = ScrollView(size = (self.trainerBox.width, self.trainerBox.height))
        self.trainerBox.bind(minimum_height = self.trainerBox.setter("height"))
        

        self.newTrainerButton = TransparentButton(text = "add new Trainer", on_release = self.addNewTrainer, size_hint_y = 0.1)
        #start disabled
        self.newTrainerButton.disabled = True

        self.trainerSpriteFolder = trainerSprites
        self.pokemonSpriteFolder = pokemonSprites

        self.trainerBoxScroll.add_widget(self.trainerBox)
        self.screenBox.add_widget(self.trainerBoxScroll)
        self.screenBox.add_widget(self.newTrainerButton)
    
    def areaChanged(self, spinner, text) -> None:
        if not super().areaChanged(spinner, text):
            #invalid area, should not be able to add new Trainer to it
            self.newTrainerButton.disabled = True
            return
        self.currentTrainerObject = None
        self.areaObject = self.manager.currentArea
        self.updateTrainers()
        self.newTrainerButton.disabled = False
    
    def on_leave(self):
        super().on_leave()

    def updateTrainers(self):
        """reloads the expandabletrainerboxes with updated trainer dict"""
        print(f"object: {self.areaObject}")
        self.trainers = self.areaObject.trainers
        logger.debug(f"loaded trainers: {self.trainers.keys()}")
        self.clearTrainerBox()

        for trainer in self.trainers.values():
            box = ExpandableTrainerBox(trainer, self.removeTrainer)
            self.trainerBox.add_widget(box)
        
        """code below should not have an effect, leftover if something where to happen to the scrollbar"""
        # self.trainerBoxScroll.size = (self.trainerBox.width, self.trainerBox.height)
        # self.trainerBox.bind(minimum_height = self.trainerBox.setter("height"))
  
    def clearTrainerBox(self):
        """removes all widgets from trainerBox"""
        self.trainerBox.clear_widgets()
        logger.debug(f"clearing trainerBox")

    def addNewTrainer(self, instance):
        """displays the edittrainerBox for a new trainer to be added"""
        logger.debug("create dialog to add new trainer")
        self.newTrainerDialog.open()

    
    def addTrainerToGame(self, trainerObject) -> bool:
        """Add trainerObject to the gameObject, function called in the addtrainerDialog. returns 0 on failure, 1 on success"""
        logger.debug(f"Adding {trainerObject.name} to {self.areaObject.name}")
        if self.areaObject.addTrainer(trainerObject):
            logger.debug("added trainer")
        else:
            logger.debug("error occured adding trainer")
            #update self.trainerobject to None, otherwise next call will execute edittrainer
            # self.editTrainerBox.trainerObject = None
            return 0
        self.updateTrainers()
        return 1

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
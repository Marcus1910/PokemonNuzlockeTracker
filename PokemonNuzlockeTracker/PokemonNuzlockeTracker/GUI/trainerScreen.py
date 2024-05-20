from nuzlockeScreen import NuzlockeScreen
from trainerDialog import AddTrainerDialog
from loggerConfig import logger
from expandableBox import ExpandableTrainerBox

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

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

        self.newTrainerDialog = AddTrainerDialog(self.addTrainerToGame)

        #box that contains all expandabletrainerboxes
        self.trainerBox = BoxLayout(size_hint_y = 0.61, orientation = "vertical")

        self.newTrainerButton = Button(text = "add new Trainer", on_release = self.addNewTrainer, size_hint_y = 0.1)
        #start disabled
        self.newTrainerButton.disabled = True

        self.spriteFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites")
        self.trainerSpriteFolder = os.path.join(self.spriteFolder, "trainerSprites")
        self.pokemonSpriteFolder = os.path.join(self.spriteFolder, "pokemonMinimalWhitespace")

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
        for trainer in self.trainers.values():
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
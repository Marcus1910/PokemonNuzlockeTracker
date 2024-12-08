from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from GUI.Dialog.trainerDialog import AddTrainerDialog
from GUI.nuzlockeScreen import NuzlockeScreen
from GUI.expandableBox import ExpandableTrainerBox
from GUI.transparentButton import TransparentButton

from loggerConfig import logger

from Logic.games import pokemonSprites, trainerSprites, itemSprites


class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        #need locationRecord to update trainers and add trainers
        self.locationRecord = None
        #trainer Object for current trainer
        self.trainers = None 

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

        self.locationRecord = self.manager.locationRecord
        self.updateTrainers()
        self.newTrainerButton.disabled = False
    
    def on_leave(self):
        super().on_leave()

    def updateTrainers(self) -> None:
        """reloads the expandabletrainerboxes with updated trainer dict"""
        noTrainers = True
        
        self.trainers = self.manager.getTrainerNames()
        self.clearTrainerBox()
        
        for trainerName in self.trainers:
            noTrainers = False
            trainerRecord = self.manager.getTrainerRecord(trainerName)
            box = ExpandableTrainerBox(trainerRecord)
            #trainer.addRemoveObserver(self.updateTrainers)
            self.trainerBox.add_widget(box)

        if noTrainers:
            """make the new trainer button stand out more when there are no trainers"""
            self.newTrainerButton.greenColor()
            return
        
        self.newTrainerButton.resetColor()
  
    def clearTrainerBox(self):
        """removes all widgets from trainerBox"""
        self.trainerBox.clear_widgets()
        logger.debug(f"clearing trainerBox")

    def addNewTrainer(self, instance):
        """displays the edittrainerBox for a new trainer to be added"""
        logger.debug("create dialog to add new trainer")
        dialog = AddTrainerDialog(self.updateTrainers)
        dialog.open()

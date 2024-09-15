from nuzlockeScreen import NuzlockeScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from expandableBox import EncounterTypeBox
from transparentButton import TransparentButton

from loggerConfig import logger
import games as gm
import os

class EncounterScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        self.areaTypeSpinnerString = "choose an encounterType"
        self.encounterBox = BoxLayout(orientation= 'vertical', size_hint_y = 1)
        
        self.encounterBox = GridLayout(cols = 1, size_hint_y = None)
        self.encounterScroll = ScrollView(size = (self.encounterBox.width, self.encounterBox.height))
        self.encounterBox.bind(minimum_height = self.encounterBox.setter("height"))

        self.newEncounterTypeButton = TransparentButton(text = "add new area type", size_hint_y = 0.1, on_release = lambda btn: self.addNewEncounterType())
        self.newEncounterTypeButton.disabled = True

        self.encounterScroll.add_widget(self.encounterBox)
        
        self.screenBox.add_widget(self.encounterScroll)
        self.screenBox.add_widget(self.newEncounterTypeButton)
    
    def areaChanged(self, spinner, text):
        if not super().areaChanged(spinner, text):
            self.newEncounterTypeButton.disabled = True
            return 0
        
        self.encounters = self.manager.currentArea.encounters
        # update encounter boxes
        self.updateEncounters()
        self.newEncounterTypeButton.disabled = False

    def updateEncounters(self) -> None:
        self.clearLayout()
        noEncounters = True

        for encounterType, encounters in self.encounters.items():
            noEncounters = False
            self.encounterBox.add_widget(EncounterTypeBox(encounterType, encounters, self.manager.currentArea.name))
        
        if noEncounters:
            self.newEncounterTypeButton.greenColor()
            return
        
        self.newEncounterTypeButton.resetColor()


    def addNewEncounterType(self):
        logger.debug(f"adding new encounterType, TODO")

    def clearLayout(self):
        """clears the encounterBox"""
        self.encounterBox.clear_widgets()
    



    # def changeEncounters(self, spinner, text):
    #     """change the encounters based on the text provided by the areaTypeSpinner"""
    #     self.clearLayout()
    #     if text == "new encounterType":
    #         return
        
    #     for area in self.encounters:
    #         if area[0] == text:
    #             #found encounters
    #             break
    #     else:
    #         logger.error("encounters could not be found")
    #         return

    #     logger.debug(f"showing new encounters from text, TODO")

    #     for encounter in area[1]:
    #         self.catchableEncounterBox.add_widget(EncounterBox(encounter, self.manager.currentArea, area[0]))
        

        
        

            
        
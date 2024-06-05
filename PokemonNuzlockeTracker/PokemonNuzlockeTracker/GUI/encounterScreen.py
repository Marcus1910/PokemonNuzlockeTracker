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

        self.encounterScroll.add_widget(self.encounterBox)

        self.screenBox.add_widget(self.encounterScroll)
    
    def areaChanged(self, spinner, text):
        if not super().areaChanged(spinner, text):
            return 0
        self.clearLayout()
        self.encounters = self.manager.currentArea.encounters
        # update encounter boxes
        self.updateEncounters()

    def updateEncounters(self) -> None:
        print("adding encounters")
        for encounterType, encounters in self.encounters.items():
            self.encounterBox.add_widget(EncounterTypeBox(encounterType, encounters))
        # print(self.encounters)
        # for encounterType in self.encounters:
        #     print(encounterType)

    def addNewEncounterType(self, args):
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
        

        
        

            
        
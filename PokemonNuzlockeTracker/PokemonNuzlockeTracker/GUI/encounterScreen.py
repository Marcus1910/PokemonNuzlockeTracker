from nuzlockeScreen import NuzlockeScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.label import Label

from loggerConfig import logger
import games as gm
import os

class EncounterScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        self.areaTypeSpinnerString = "choose an encounterType"
        self.encounterBox = BoxLayout(orientation= 'vertical', size_hint_y = 0.76)
        
        self.encounterTypeList = []
        self.catchableEncounterBox = BoxLayout(orientation= 'vertical', size_hint_y = 0.8)

        self.encounterBox.add_widget(self.catchableEncounterBox)

        self.areaTypeSpinner = Spinner(text = self.areaTypeSpinnerString, values = [], size_hint_y = 0.04)
        self.areaTypeSpinner.background_color = gm.opaque
        self.areaTypeSpinner.bind(text = self.changeEncounters)
        self.areaTypeSpinner.disabled = True

        self.screenBox.add_widget(self.areaTypeSpinner)
        self.screenBox.add_widget(self.encounterBox)
    
    def areaChanged(self, spinner, text):
        if not super().areaChanged(spinner, text):
            self.areaTypeSpinner.disabled = True
            return 0
        self.areaTypeSpinner.disabled = False
        self.clearLayout()
        self.resetSpinner()
        self.encounterTypeList = []
        self.encounters = self.manager.currentArea.encounters
        self.updateSpinner()
    
    def updateSpinner(self):
        """update the values of the spinner to the new encounter types"""
        #get only the names
        self.areaTypeSpinner.values = [x[0] for x in self.encounters]
        self.areaTypeSpinner.values.append("new encounterType")
    
    def resetSpinner(self):
        self.areaTypeSpinner.text = self.areaTypeSpinnerString
        self.areaTypeSpinner.values = ["new encounterType"]

    def addNewEncounterType(self, args):
        logger.debug(f"adding new encounterType, TODO")

    def changeEncounters(self, spinner, text):
        """change the encounters based on the text provided by the areaTypeSpinner"""
        self.clearLayout()
        if text == "new encounterType":
            return
        
        for area in self.encounters:
            if area[0] == text:
                #found encounters
                break
        else:
            logger.error("encounters could not be found")
            return

        logger.debug(f"showing new encounters from text, TODO")

        for encounter in area[1]:
            self.catchableEncounterBox.add_widget(EncounterBox(encounter, self.manager.currentArea, area[0]))
        
    def clearLayout(self):
        self.catchableEncounterBox.clear_widgets()
        
        
class EncounterBox(BoxLayout):
    pokemonSpritesFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")
    def __init__(self, pokemonObject, area, areaType, *args, **kwargs):
        """expects pokemonObject, area, and areaType"""
        super().__init__(*args, **kwargs)
        self.pokemonObject = pokemonObject
        self.orientation = "horizontal"
        print(pokemonObject.name)
        self.catchButton = Button(text = "catch", on_press = self.catch, size_hint_x = 0.1)
        image = os.path.join(self.pokemonSpritesFolder, f"{pokemonObject.name.lower()}.png")
        self.pokemonImage = Image(source = image, pos_hint = {"top": 1}, size_hint_x = 0.4)
        self.pokemonImage.fit_mode = "contain"
        self.infoBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
        self.percentageLabel = Label(text = f"percentage: {pokemonObject.percentage}")
        self.levelsLabel = Label(text = f"levels: {pokemonObject.levels}")
        self.moreInfoButton = Button(text = "more info", on_press = self.showMoreInfo, size_hint_x = 0.2)
        
        self.infoBox.add_widget(self.percentageLabel)
        self.infoBox.add_widget(self.levelsLabel)

        self.add_widget(self.catchButton)
        self.add_widget(self.pokemonImage)
        self.add_widget(self.infoBox)
        self.add_widget(self.moreInfoButton)

    def catch(self, button):
        logger.debug(f"catching {self.pokemonObject.name}, TODO")
    
    def showMoreInfo(self, button):
        logger.debug(f"show more info, TODO")
            
        
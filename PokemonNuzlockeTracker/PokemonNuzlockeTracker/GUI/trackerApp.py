from kivymd.app import MDApp
from kivy.core.window import Window

from windowmanager import WindowManager
from selectGameScreen import SelectGameScreen
from trainerScreen import TrainerScreen
from attemptInfoScreen import AttemptInfoScreen
from encounterScreen import EncounterScreen
from itemScreen import ItemScreen

import sys
from loggerConfig import logger

class TrackerApp(MDApp):
    def __init__(self, operatingSystem, **kwargs):
        super().__init__(**kwargs)
        self.operatingSystem = operatingSystem

    def build(self):
        #use OS to change view to that of android
        if self.operatingSystem == "Windows":
            logger.info("detected windows")
            Window.size = (390, 780)

        sm = WindowManager()
        selectGameScreen = SelectGameScreen(operatingSystem = self.operatingSystem, name = "selectGameScreen")
        
        attemptInfoScreen = AttemptInfoScreen(name = "attemptInfoScreen", screenName = "Info on current attempt")
        trainerScreen = TrainerScreen(name = "trainerScreen", screenName = "Trainer Screen")
        encounterScreen = EncounterScreen(name = "encounterScreen", screenName = "Encounter Screen")
        itemScreen = ItemScreen(name = "itemScreen", screenName = "Item Screen")

        sm.add_widget(selectGameScreen)
        sm.add_widget(trainerScreen)
        sm.add_widget(attemptInfoScreen)
        sm.add_widget(encounterScreen)
        sm.add_widget(itemScreen)
        #attempt info screen as first so it has index 0
        sm.screenList.extend([attemptInfoScreen.name, trainerScreen.name, encounterScreen.name, itemScreen.name])

        sm.current = "selectGameScreen"
        return sm
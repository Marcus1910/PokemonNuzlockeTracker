from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window

import games as gm
from selectGameScreen import SelectGameScreen
from attemptInfoScreen import AttemptInfoScreen

from nuzlockeScreen import NuzlockeScreen
import os
import time

#define different screens
class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(TrainerScreen, self).__init__(screenName = screenName, **kwargs)


class ItemScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(ItemScreen, self).__init__(screenName = screenName, **kwargs)

class EncounterScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(EncounterScreen, self).__init__(screenName = screenName, **kwargs)

class WindowManager(ScreenManager):
    attempt = None
    _gameObject = None
    areaList = None
    _screenNumber= 0
    screenList = []



    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self, gameObject):
        self._gameObject = gameObject
        print("gathering data")
        self.areaList = self._gameObject.retrieveGameData()
    
    @property
    def screenNumber(self):
        return self._screenNumber
    
    @screenNumber.setter
    def screenNumber(self, number):
        self._screenNumber = number % len(self.screenList)
        self.current = self.screenList[self._screenNumber]


class SelectGame(App):

    def build(self):
        #given by selectgameWindow
        

        sm = WindowManager()
        selectGameScreen = SelectGameScreen(name = "selectGameScreen")
        
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
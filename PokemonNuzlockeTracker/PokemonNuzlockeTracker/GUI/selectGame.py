from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window

import games as gm
from windowmanager import WindowManager
from selectGameScreen import SelectGameScreen
from trainerScreen import TrainerScreen
from attemptInfoScreen import AttemptInfoScreen
from nuzlockeScreen import NuzlockeScreen

import os
import time

#define different screens




class ItemScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(ItemScreen, self).__init__(screenName = screenName, **kwargs)

class EncounterScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(EncounterScreen, self).__init__(screenName = screenName, **kwargs)




class SelectGame(App):

    def build(self):
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
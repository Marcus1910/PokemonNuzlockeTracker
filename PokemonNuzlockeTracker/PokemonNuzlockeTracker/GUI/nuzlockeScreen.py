from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label

from kivy.uix.spinner import Spinner

from transparentButton import TransparentButton
import games as gm

import os

class NuzlockeScreen(Screen):
    """adds the name of the screen at the top, add self.layout which is a boxLayout. Can also add background for all screens except first screen, total of 0.25 size_hint_y"""
    def __init__(self, screenName, **kwargs):
        super(NuzlockeScreen, self).__init__(**kwargs)

        self.entered = False
        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background.jpg"))
        bgImage.size = Window.size
        bgImage.pos = self.pos

        self.layout = BoxLayout(orientation= "vertical")
        self.screenBox = BoxLayout(orientation = "vertical", size_hint_y = 0.04)
        screenLabel = Label(text = screenName, color = (0, 0, 0, 1))
        self.screenBox.add_widget(screenLabel)

        self.areaSpinner = Spinner(text = "choose an area", values = ["new Area"], size_hint_y = 0.08)
        self.areaSpinner.background_color = gm.opaque
        self.areaSpinner.bind(text = self.areaChanged)

        self.layout.add_widget(self.screenBox)
        self.layout.add_widget(self.areaSpinner)

        self.add_widget(bgImage)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.areaSpinner.values = [area.name for area in self.manager.areaList]
        if self.manager.currentArea == None:
            return 0
        self.areaSpinner.text = self.manager.currentArea.name
        return 1

    def areaChanged(self, spinner, text):
        """text is the areaName"""
        self.manager.currentArea = text
        

    def on_enter(self):
        """call function to add next and previous buttons to the bottom of the screen"""
        #return if the function is already called, else create buttons. otherwise creates multiple buttons on each exit
        if self.entered:
            return
        #create buttons to naviagte through the screens and add to layout
        self.buttons = BoxLayout(orientation = "horizontal", size_hint_y = 0.08)
        continueButton = TransparentButton(text = "next", size_hint_x = 0.2)
        continueButton.bind(on_press = self.nextScreen)
        fillerLabel = Label(text = "", size_hint_x = 0.6)
        previousButton = TransparentButton(text = "previous", size_hint_x = 0.2, pos_hint = {"x" : 0.8})
        previousButton.bind(on_press = self.previousScreen)
        self.buttons.pos_hint = {"y": 0, "x": 0}

        self.buttons.add_widget(previousButton)
        self.buttons.add_widget(fillerLabel)
        self.buttons.add_widget(continueButton)

        self.layout.add_widget(self.buttons)
        self.entered = True
    
    def nextScreen(self, instance):
        """go to the next screen"""
        self.manager.screenNumber += 1

    def previousScreen(self, insatnce):
        """go to previous screen"""
        self.manager.screenNumber -= 1


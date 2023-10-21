from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button

from transparentButton import TransparentButton

import os

class NuzlockeScreen(Screen):
    """adds the name of the screen at the top, add self.layout which is a boxLayout. Can also add background for all screens except first screen"""
    def __init__(self, screenName, **kwargs):
        super(NuzlockeScreen, self).__init__(**kwargs)

        self.entered = False
        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background.jpg"))
        bgImage.size = Window.size
        bgImage.pos = self.pos

        self.layout = BoxLayout(orientation= "vertical")
        self.screenBox = BoxLayout(orientation = "vertical", size_hint_y = 0.05)
        screenLabel = Label(text = screenName, color = (0, 0, 0, 1))
        self.screenBox.add_widget(screenLabel)

        self.layout.add_widget(self.screenBox)

        self.add_widget(bgImage)
        self.add_widget(self.layout)

    def on_enter(self):
        """call function to add next and previous buttons to the bottom of the screen"""
        #return if the function is already called, else create buttons. otherwise creates multiple buttons on each exit
        if self.entered:
            return
        self.buttons = BoxLayout(orientation = "horizontal", size_hint_y = 0.1)
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
        self.manager.screenNumber += 1

    def previousScreen(self, insatnce):
        self.manager.screenNumber -= 1


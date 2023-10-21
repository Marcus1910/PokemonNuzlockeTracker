from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label


import os

class NuzlockeScreen(Screen):
    """adds the name of the screen at the top, add self.layout which is a boxLayout. Can also add background for all screens except first screen"""
    def __init__(self, screenName, **kwargs):
        
        super(NuzlockeScreen, self).__init__(**kwargs)

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
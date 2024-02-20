from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
import os

class BackgroundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background3.jpg"))
        bgImage.fit_mode = "fill"
        self.add_widget(bgImage)
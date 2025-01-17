from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class ClickableImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
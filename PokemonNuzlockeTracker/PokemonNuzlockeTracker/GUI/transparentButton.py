from kivy.uix.button import Button

class TransparentButton(Button):
    def __init__(self, **kwargs):
        super(TransparentButton, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.5)  # Set the background color to transparent
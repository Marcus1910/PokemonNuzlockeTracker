from kivy.uix.button import Button

class TransparentButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.5)  # Set the background color to transparent
    
    def resetColor(self):
        self.background_color = (1, 1, 1, 0.5)
    
    def redColor(self):
        self.background_color = (1, 0, 0, 0.5)

    def greenColor(self):
        self.background_color = (0, 1, 0, 0.5)
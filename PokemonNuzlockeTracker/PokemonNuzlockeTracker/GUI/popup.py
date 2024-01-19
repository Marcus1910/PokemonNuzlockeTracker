from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class RemovePokemonPopup(Popup):
    def __init__(self, text, *args, **kwargs):
        """popup that displays given text and has 2 buttons, yes and no"""
        super().__init__(*args, **kwargs)
        # self.layout = BoxLayout(orientation = ver)
        # self.messageLabel = Label(text = text)
        # self.removeButton = Button(text = "yes", on_press = self.returnTrue)
        # self.cancelButton = Button(text = "no", on_press = self.returnFalse)
        # Create buttons for selection
        button_0 = Button(text='Return 0')
        button_0.bind(on_press=lambda instance: self.dismiss(return_value=0))

        button_1 = Button(text='Return 1')
        button_1.bind(on_press=lambda instance: self.dismiss(return_value=1))

        # Add buttons to the content of the Popup
        self.content = Button(text='Select an Option')
        self.content.add_widget(button_0)
        self.content.add_widget(button_1)

    
    # def returnTrue(self, button):
    #     return True
    
    # def returnFalse(self, button):
    #     return False

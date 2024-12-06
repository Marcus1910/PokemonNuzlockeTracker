from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from GUI.transparentButton import TransparentButton
from GUI.numberInput import NumberInput

from loggerConfig import logger


class NewAreaBox(BoxLayout):
    def __init__(self, confirmCallback, **kwargs):
        """Boxlayout to add a new Area, confirmCallback will receive the Area name and badge requirement when confirm button is pressed."""
        super().__init__(**kwargs)
        self.confirmCallback = confirmCallback 
        self.dismiss = None #changes when used with a popup to the function that dismisses the popup
        self.areaNameLabel = TextInput(hint_text = "Area Name", size_hint_y = 0.2)
        self.badgeAccessible = NumberInput(hint_text = "amount of badges required to visit Area", size_hint_y = 0.2)
        #used to create an empty space
        self.filling = BoxLayout(orientation = "horizontal", size_hint_y = 0.4)

        self.buttonBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.2, pos_hint = {"bottom" : 1})
        self.confirmButton = TransparentButton(text = "confirm", size_hint_x = 0.7, on_release = self.returnAreaName)
        self.cancelButton = TransparentButton(text = "cancel", size_hint_x = 0.3)

        self.buttonBox.add_widget(self.confirmButton)
        self.buttonBox.add_widget(self.cancelButton)

        self.add_widget(self.areaNameLabel)
        self.add_widget(self.badgeAccessible)
        self.add_widget(self.filling)
        self.add_widget(self.buttonBox)

    def returnAreaName(self, button):
        name = self.areaNameLabel.text
        badge = self.badgeAccessible.text
        if not self.confirmCallback(name, badge):
            logger.debug(f"trouble creating {name}, {badge}")
            return 0
        #area succesfully added
        
        #dismiss popup if it is a popup
        if self.dismiss != None:
            self.dismiss()
        return 1

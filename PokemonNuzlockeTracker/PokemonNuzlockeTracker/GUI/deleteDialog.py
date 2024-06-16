from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from loggerConfig import logger

class DeletePopup(MDDialog):
    def __init__(self, **kwargs):
        self.auto_dismiss = False
        self.type = "custom" 
        self.result = 0
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        self.buttons = [MDFlatButton(text = "yes", md_bg_color = "red" ,on_release = self.yes), MDFlatButton(text = "no", on_release = self.no)]
        super().__init__(**kwargs)
    
    def yes(self, instance):
        self.result = 1
        self.dismiss()
    
    def no(self, instance):
        self.result = 0
        self.dismiss()

class DeleteTrainerPopup(DeletePopup):
    def __init__(self, trainerName, areaName, **kwargs):
        self.title = f"Delete {trainerName} for {areaName}?"
        super().__init__(**kwargs)

class DeleteTrainerPokemonPopup(DeletePopup):
    def __init__(self, pokemonName, trainerName, **kwargs):
        self.title = f"Delete {pokemonName} from {trainerName}?"
        super().__init__(**kwargs)
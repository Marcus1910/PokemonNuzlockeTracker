from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch

from utilityFunctions import checkString, validateTextInput
from loggerConfig import logger
from pokemon import TrainerPokemon

class AddPokemonDialog(MDDialog):
    def __init__(self, trainerObject, trainerBox, **kwargs):
        self.trainerObject = trainerObject
        self.trainerBox = trainerBox
        self.auto_dismiss = False
        self.title = "add new Pokemon"
        self.type = "custom"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        self.content = AddPokemonBox(size_hint_y = None)
        self.buttons = [MDFlatButton(text = "add", on_release = self.createPokemon), MDFlatButton(text = "discard", on_release = self.dismiss)]
        self.content_cls = self.content
        super().__init__(**kwargs)
    
    def createPokemon(self, instance):
        object = self.content.getInput()
        self.trainerObject.pokemon = object
        self.trainerObject.checkDefeated()
        self.trainerBox.updateContent()
        self.dismiss()


class AddPokemonBox(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.height = "200dp"
        self.pokemonName = MDTextField(hint_text = "Pokemon Name")
        self.pokemonLevel = MDTextField(hint_text = "pokemon Level")
        self.add_widget(self.pokemonName)
        self.add_widget(self.pokemonLevel)
    
    def getInput(self):
        name = self.pokemonName.text
        level = self.pokemonLevel.text
        pokemonObject = TrainerPokemon(name, level)
        return pokemonObject

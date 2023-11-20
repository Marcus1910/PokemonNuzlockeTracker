from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from trainerPokemon import TrainerPokemon
import os

class DetailedPokemonBox(BoxLayout):
    pokemonSpritesFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")
    def __init__(self, screen, **kwargs):
        """DetailedPokemonBox uses 50% of the boxLayout in which it is placed, size_hint_y = 0.5"""
        super().__init__(**kwargs)
        self.moveList = []
        self.trainerObject = None #used for saving purposes
        self.trainerScreen = screen
    
    def clearLayout(self):
        """save previous pokemon and clear screen for new pokemon"""
        self.savePokemon()
        #remove trainerName
        self.trainerObject = None
        self.clear_widgets()
        self.moveList = []

    def buildLayout(self, trainerObject):
        """build standard layout with inputs so pokemon can be created"""
        #add new trainerName
        self.trainerObject = trainerObject
        #create Name label and input
        self.nameInput = TextInput(hint_text = "Name", multiline = False, size_hint_x = 0.7)
        self.levelInput = TextInput(hint_text = "Level", multiline = False, size_hint_x = 0.3)
        self.nameLevelBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.1)
        #add pokemon image
        self.imageBox = BoxLayout(size_hint_y = 0.9)
        self.pokemonImage = Image(source = os.path.join(self.pokemonSpritesFolder, "0.png"), size_hint_y = 0.4, pos_hint = {"top": 1})
        self.pokemonImage.fit_mode = "contain"

        self.nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        #add information about pokemon, ability, held item, typing
        self.pokemonInfoBox = BoxLayout(orientation= "vertical", size_hint_x = 0.3, size_hint_y = 0.5, pos_hint = {"top": 1})
        self.abilityInput = TextInput(hint_text = "ability", multiline = False)
        self.heldItemInput = TextInput(hint_text = "held item", multiline = False)
        self.typing1Input = TextInput(hint_text = "typing 1", multiline = False)
        self.typing2Input = TextInput(hint_text = "typing 2", multiline = False)

        self.moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3, size_hint_y = 0.5, pos_hint = {"top": 1})
        for move in range(4):
            moveInput = TextInput(hint_text = f"move #{move + 1}", size_hint_y = 0.25, multiline = False)
            self.moveList.append(moveInput)
            self.moveBox.add_widget(moveInput)

        self.nameLevelBox.add_widget(self.nameInput)
        self.nameLevelBox.add_widget(self.levelInput)

        self.imageBox.add_widget(self.pokemonImage)

        self.nameImageBox.add_widget(self.nameLevelBox)
        self.nameImageBox.add_widget(self.imageBox)

        self.pokemonInfoBox.add_widget(self.abilityInput)
        self.pokemonInfoBox.add_widget(self.heldItemInput)
        self.pokemonInfoBox.add_widget(self.typing1Input)
        self.pokemonInfoBox.add_widget(self.typing2Input)

        self.add_widget(self.nameImageBox)
        self.add_widget(self.pokemonInfoBox)
        self.add_widget(self.moveBox)

    def fillLayout(self, pokemonObject):
        """fills in the layout made by buildLayout function, needs pokemon object to do so"""
        self.nameInput.text = pokemonObject.name
        self.levelInput.text = str(pokemonObject.level)
        self.pokemonImage.source = os.path.join(self.pokemonSpritesFolder, f"{pokemonObject.name.lower()}.png")
        
        if pokemonObject.ability is not None:
            self.abilityInput.text = pokemonObject.ability
        if pokemonObject.heldItem != "n/a" and pokemonObject.heldItem != None:
            self.heldItemInput.text = pokemonObject.heldItem
        for index, move in enumerate(pokemonObject.moves):
            self.moveList[index].text = move


    def savePokemon(self, pokemonObject = None):
        """create pokemon object or change pokemon object and save it to the arealist, route, trainer,"""
        try:
            #check if the box already exists, otherwise crashes when switching from screens when area has changed
            name = self.nameInput.text
        except AttributeError:
            return
        if self.checkString(name):
            print("empty name")
            return

        level = self.levelInput.text
        #create own pokemonObject
        if pokemonObject == None:
            pokemonObject = TrainerPokemon(name, level)
        #decorate pokemonObject before saving it
        pokemonObject.ability = self.abilityInput.text if not self.checkString(self.abilityInput.text) else None
        print(f"bye bye: {pokemonObject}")

        if pokemonObject == None:
            self.trainerObject.editPokemon(pokemonObject)
        else:
            self.trainerObject.pokemon = pokemonObject
        self.trainerScreen.update()
        
    def checkString(self, text):
        """function that checks whether the given text consists of only whitespace or is empty, 1 if True"""
        return text.isspace() or text == ""
        
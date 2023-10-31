from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class DetailedPokemonBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moveList = []
    
    def clearLayout(self):
        self.clear_widgets()
        self.moveList = []

    def buildLayout(self):
        """build standard layout with inputs so pokemon can be created"""
        #create Name label and input
        self.nameInput = TextInput(hint_text = "Name", multiline = False, size_hint_x = 0.7)
        self.levelInput = TextInput(hint_text = "Level", multiline = False, size_hint_x = 0.3)
        self.nameLevelBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.1)
        #add pokemon image
        self.imageBox = BoxLayout(size_hint_y = 0.9)

        self.nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        #add information about pokemon, ability, held item, typing
        self.pokemonInfoBox = BoxLayout(orientation= "vertical", size_hint_x = 0.3, size_hint_y = 0.5, pos_hint = {"top": 1})
        self.abilityInput = TextInput(hint_text = "ability", multiline = False)
        self.heldItemInput = TextInput(hint_text = "held item", multiline = False)
        self.typing1Input = TextInput(hint_text = "typing 1", multiline = False)
        self.typing2Input = TextInput(hint_text = "typing 2", multiline = False)



        self.moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3, size_hint_y = 0.5, pos_hint = {"top": 1})
        for move in range(4):
            moveInput = TextInput(hint_text = f"move #{move + 1}", size_hint_y = 0.25)
            self.moveList.append(moveInput)
            self.moveBox.add_widget(moveInput)

        self.nameLevelBox.add_widget(self.nameInput)
        self.nameLevelBox.add_widget(self.levelInput)

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
        print(pokemonObject.ability)
        print(pokemonObject.heldItem)
        self.nameInput.text = pokemonObject.name
        self.levelInput.text = str(pokemonObject.level)
        
        if pokemonObject.heldItem != "n/a" and pokemonObject.heldItem != None:
            print(pokemonObject.heldItem)

        if pokemonObject.ability is not None:
            self.abilityInput.text = pokemonObject.ability

            self.heldItemInput.text = pokemonObject.heldItem
        for index, move in enumerate(pokemonObject.moves):
            self.moveList[index].text = move


    def savePokemon(self):
        """create pokemon object or change pokemon object"""
        pass
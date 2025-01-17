from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

from GUI.nuzlockeScreen import NuzlockeScreen
from GUI.transparentButton import TransparentButton


class PokemonInfoScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        """Make box that has idpokemon | trainerpokemon | playerpokemon as input
        idpokemon show levelupmoves it should know, trainerpokemon moves it knows (green), could know (yellow)"""  
        super().__init__(screenName, **kwargs)
        self.levelupMoves = []
        self.learnedMoves = []
        self.basestats = None #-> object boxlayout -> image/graph + textfields
        
        
    def createLayout(self):
        self.editButton = TransparentButton(text = "Edit", on_press = self.editPokemon)
        self.pokemonImage = Image(source = None)
        self.pokemonName = TextInput(hint_text = "Pokemon name")
        self.type1 = Image(source = None)
        self.type2 = Image(source = None)
        
        
    
    def editPokemon(self, button: TransparentButton):
        print("putting screen in edit mode, TODO")
            
        
 
from nuzlockeScreen import NuzlockeScreen
from games import getPokemonSprite

from kivymd.app import MDApp 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image


class AttemptInfoScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)

        self.areaLabel = Label(text = "gathering data", color = self.standardColor, size_hint_y = 0.19)
        self.badgeLabel = Label(text = "gathering data", color = self.standardColor, size_hint_y = 0.19)

        self.pcBox = BoxLayout(orientation= "vertical", size_hint_y = 0.31)
        self.pcLabel = Label(text = "Pokemon still available Placeholder", color = self.standardColor, size_hint_y = 0.1)
        self.pokemonPcSpritesBox = BoxLayout(orientation = "vertical", size_hint_y = 0.9)
        self.pcBox.add_widget(self.pcLabel)
        self.pcBox.add_widget(self.pokemonPcSpritesBox)

        self.graveBox = BoxLayout(orientation = "vertical", size_hint_y = 0.31)
        self.graveyardLabel = Label(text = "Fainted pokemon placeholder", color = self.standardColor, size_hint_y = 0.1)
        self.pokemonGraveyardSpritesBox = BoxLayout(orientation = "vertical", size_hint_y = 0.9)
        self.graveBox.add_widget(self.graveyardLabel)
        self.graveBox.add_widget(self.pokemonGraveyardSpritesBox)

        self.screenBox.add_widget(self.areaLabel)
        self.screenBox.add_widget(self.badgeLabel)
        self.screenBox.add_widget(self.pcBox)
        self.screenBox.add_widget(self.graveBox)
    
    def areaChanged(self, spinner, text):
        if not super().areaChanged(spinner, text):
            #area has not been changed succesfully
            return
        self.areaLabel.text = f"current area: {self.manager.currentArea.name}"
    
    def on_pre_enter(self) -> bool:
        super().on_pre_enter()
        self.updateBadgeLabel()
        self.updateArena()
        self.updateGraveyard()
    
    def updateBadgeLabel(self) -> None:
        badge = self.manager.gameObject.badge
        self.badgeLabel.text = f"amount of badges: {badge}"
    
    def updateArena(self):
        #cleanup and garbage colection needs fixing
        self.pokemonPcSpritesBox.clear_widgets()
        caughtPokemon = MDApp.get_running_app().game.arena
        amountCaughtPokemon = len(caughtPokemon)
        self.pcLabel.text = "No pokemon caught and alive"
        if amountCaughtPokemon > 0:
            self.pcLabel.text = "Pokemon available"
            box = None       
            for index, pokemon in enumerate(caughtPokemon):    
                if index % 6 == 0:
                    if box:
                        self.pokemonPcSpritesBox.add_widget(box)
                    print("adding box")
                    box = BoxLayout(orientation = "horizontal", size_hint_y = 1/5, size_hint_x = 1)
                pokemonImage = Image(source = getPokemonSprite(pokemon[0].name), fit_mode = "contain")
                box.add_widget(pokemonImage)
                #pokemonImage.source = getPokemonSprite(pokemon[0].name)
                print(f"adding {pokemon[0].name} to box")
            if box:
                self.pokemonPcSpritesBox.add_widget(box)
    
    def updateGraveyard(self):
        self.pokemonGraveyardSpritesBox.clear_widgets()
        caughtPokemon = MDApp.get_running_app().game._graveyard
        amountCaughtPokemon = len(caughtPokemon)
        self.graveyardLabel.text = "No pokemon caught and alive"
        if amountCaughtPokemon > 0:
            self.graveyardLabel.text = "Pokemon available"
            box = None
            for index, pokemon in enumerate(caughtPokemon):    
                if index % 6 == 0:
                    if box:
                        self.pokemonGraveyardSpritesBox.add_widget(box)
                    print("adding box")
                    box = BoxLayout(orientation = "horizontal", size_hint_y = 1/5, size_hint_x = 1)
                pokemonImage = Image(source = getPokemonSprite(pokemon[0].name), fit_mode = "contain")
                box.add_widget(pokemonImage)
                #pokemonImage.source = getPokemonSprite(pokemon[0].name)
                print(f"adding {pokemon[0].name} to box")
            if box:
                self.pokemonGraveyardSpritesBox.add_widget(box)       

            

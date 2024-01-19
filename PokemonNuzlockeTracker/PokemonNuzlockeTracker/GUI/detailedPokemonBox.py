from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from loggerConfig import logger
from popup import RemovePokemonPopup
from trainerPokemon import TrainerPokemon
import os

class DetailedPokemonBox(BoxLayout):
    pokemonSpritesFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")
    def __init__(self, screen, *args, **kwargs):
        """DetailedPokemonBox used to give more info about a pokemon, buildlayout to build it, if given an pokemonObject it will fill it"""
        super().__init__(*args, **kwargs)
        self.moveList = []
        self.pokemonObject = None
        self.pokemonIndex = None #used for saving purposes
        self.trainerObject = None #used for saving purposes
        self.trainerScreen = screen

        #forward declarations for clear_layout function
        self.pokemonBox = BoxLayout(orientation = "horizontal")
        self.additionalInfoBox = BoxLayout(orientation = "horizontal")
        self.pokemonChoice = BoxLayout(orientation = "horizontal", size_hint_y = 0.2, pos_hint = {"bottom": 1})
    
    def clearLayout(self):
        """save previous pokemon and clear screen for new pokemon"""
        #self.clear_widgets does the same however the clearPokemonLayout also adjusts the pokemons index
        self.clearPokemonLayout()
        self.clear_widgets()
        #reset variables
        self.trainerObject = None
        self.moveList = []
    
    def clearPokemonLayout(self):
        """saves pokemon, resets index and clears pokemonbox and additionalInfoBox"""
        self.savePokemon()
        self.pokemonIndex = None
        self.pokemonObject = None
        self.pokemonBox.clear_widgets()
        self.additionalInfoBox.clear_widgets()

    def buildLayout(self, trainerObject):
        """build standard layout with inputs so pokemon can be created"""
        self.trainerObject = trainerObject
        
        #always show first pokemon if applicable
        self.pokemonObject = self.trainerObject.pokemon[0] if len(self.trainerObject.pokemon) > 0 else None
        self.pokemonIndex = 0 # set to 0 so the first pokemon gets updated instead of None
        self.buildPokemonLayout()
        #TODO give regular pokemon object to function to give additional info
        self.buildAdditionalInfoLayout()
        self.updateButtons()

        self.add_widget(self.pokemonBox)
        self.add_widget(self.additionalInfoBox)
        self.add_widget(self.pokemonChoice)

    
    def buildPokemonLayout(self):
        """builds the layout which shows everything from the pokemon; abilities, moves, etc. places everything inside of self.pokemonBox"""
        #create Name label and input
        self.nameInput = TextInput(hint_text = "Name", multiline = False, size_hint_x = 0.7)
        self.levelInput = TextInput(hint_text = "Level", multiline = False, size_hint_x = 0.3)
        self.nameLevelBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.15)
        #add pokemon image
        self.imageBox = BoxLayout(size_hint_y = 0.75)
        self.pokemonImage = Image(source = os.path.join(self.pokemonSpritesFolder, "0.png"), pos_hint = {"top": 1})
        self.pokemonImage.fit_mode = "contain"

        self.nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        
        #add information about pokemon, ability, held item, typing
        self.pokemonInfoBox = BoxLayout(orientation= "vertical", size_hint_x = 0.3, pos_hint = {"top": 1})
        self.abilityInput = TextInput(hint_text = "ability", multiline = False)
        self.heldItemInput = TextInput(hint_text = "held item", multiline = False)
        self.typing1Input = TextInput(hint_text = "typing 1", multiline = False)
        self.typing2Input = TextInput(hint_text = "typing 2", multiline = False)

        self.moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3, pos_hint = {"top": 1})
        for move in range(4):
            moveInput = TextInput(hint_text = f"move #{move + 1}", size_hint_y = 0.25, multiline = False)
            self.moveList.append(moveInput)
            self.moveBox.add_widget(moveInput)

        #code for removeButton
        self.removeButton = Button(text = "remove pokemon", on_press = self.removePokemon, size_hint_y = 0.2)
        
        #add everything to correct widgets
        self.nameLevelBox.add_widget(self.nameInput)
        self.nameLevelBox.add_widget(self.levelInput)

        self.imageBox.add_widget(self.pokemonImage)
        
        self.nameImageBox.add_widget(self.nameLevelBox)
        self.nameImageBox.add_widget(self.imageBox)
        self.nameImageBox.add_widget(self.removeButton)

        self.pokemonInfoBox.add_widget(self.abilityInput)
        self.pokemonInfoBox.add_widget(self.heldItemInput)
        self.pokemonInfoBox.add_widget(self.typing1Input)
        self.pokemonInfoBox.add_widget(self.typing2Input)

        self.pokemonBox.add_widget(self.nameImageBox)
        self.pokemonBox.add_widget(self.pokemonInfoBox)
        self.pokemonBox.add_widget(self.moveBox)

        #check if a pokemonObject has been provided or it is a completely new Trainer
        if self.pokemonObject == None:
            return
        
        self.fillPokemonLayout(self.pokemonObject)
        #call fill additional info here?

    def fillPokemonLayout(self, pokemonObject):
        """fills in the layout made by buildPokemonLayout function, needs pokemon object to do so"""
        self.nameInput.text = pokemonObject.name
        self.levelInput.text = str(pokemonObject.level)
        self.pokemonImage.source = os.path.join(self.pokemonSpritesFolder, f"{pokemonObject.name.lower()}.png")
        
        if pokemonObject.ability is not None:
            self.abilityInput.text = pokemonObject.ability
        if pokemonObject.heldItem != "n/a" and pokemonObject.heldItem != None:
            self.heldItemInput.text = pokemonObject.heldItem
        for index, move in enumerate(pokemonObject.moves):
            self.moveList[index].text = move
        
    def buildAdditionalInfoLayout(self, pokemonObject = None):
        """builds layout in self.additionalInfoBox if pokemonObject is given, otherwise only takes up space to keep the ratio the same"""
        #create basestats + possible abilities / move box
        

        self.baseStatBox = BoxLayout(orientation = "vertical", size_hint_x = 0.45)
        self.basestatGraph = BoxLayout(orientation = "vertical", size_hint_y = 0.9)

        self.changeStatsBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.1)
        #self.currentBaseStatsLabel = Label(text = "current stats shown: ", size_hint_x = 0.7)
        self.switchBaseStatsButton = Button(text = "show 'original' stats", size_hint_x = 1, on_press = self.changeBaseStats)

        self.possibleAbilitiesBox = BoxLayout(orientation = "vertical",size_hint_x = 0.25)
        self.possibleMovesBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)

        for x in range(2):
            self.possibleAbilitiesBox.add_widget(Button(text = f"Ability {x+1}"))
        
        for x in range(4):
            self.possibleMovesBox.add_widget(Button(text = f"Move {x+1}"))

        self.testButton = Button(text = "baseStats")

        self.basestatGraph.add_widget(self.testButton)
        self.changeStatsBox.add_widget(self.switchBaseStatsButton)
        self.baseStatBox.add_widget(self.basestatGraph)
        self.baseStatBox.add_widget(self.changeStatsBox)

        #want to build everything so proportion stays the same, but doesn't need to be shown
        # if pokemonObject == None:
        #     return
        
        self.additionalInfoBox.add_widget(self.baseStatBox)
        self.additionalInfoBox.add_widget(self.possibleAbilitiesBox)
        self.additionalInfoBox.add_widget(self.possibleMovesBox)
    
    def fillAdditionalInfoLayout(self, pokemonObject):
        pass

    def buildAndFillButtonLayout(self):
        """creates the button at the bottom of the page that switches which pokemon is shown, places everything in self.pokemonChoice"""

        pokemonAmount = len(self.trainerObject.pokemon)

        for number in range(6):
            #default text settings
            buttonText = "add new\nPokemon"
            pokemonObject = None

            if number < pokemonAmount:
                #add pokemon details to buttons if there is a pokemon
                pokemonObject = self.trainerObject.pokemon[number]
                buttonText = pokemonObject.name

            pokemonButton = Button(text = buttonText)
            #pokemonObject is None or a pokemon object and gets given to showDetailedPokemon
            pokemonButton.bind(on_press = lambda instance, number= number, pokemonObject = pokemonObject: self.showPokemon(number, pokemonObject))

            self.pokemonChoice.add_widget(pokemonButton)
    
    def updateButtons(self):
        """removes and redraws the buttons so correct pokemon are shown"""
        self.pokemonChoice.clear_widgets()
        self.buildAndFillButtonLayout()
    
    def showPokemon(self, listIndex, pokemonObject = None):
        """redraws detailedPokemonBox and fills it if the pokemonObject is not None
        Also sets self.pokemonIndex and self.pokemonObjet to the values given"""
        #first save pokemon, reset variables, update variables and redraw screen
        self.clearPokemonLayout()
        self.pokemonIndex = listIndex
        self.pokemonObject = pokemonObject
        self.buildPokemonLayout()

    def changeBaseStats(self, instance):
        logger.info("changing BaseStat graph")

    def savePokemon(self):
        """create pokemon object or change pokemon object and save it to the trainerObject, also updates Buttons"""
        createNewEntry = False
        if self.trainerObject == None:
            return
        try:
            #check if the box already exists, otherwise crashes when switching from screens when area has changed
            name = self.nameInput.text
        except AttributeError:
            logger.debug("excepted AttributeError from nameInput because it has not yet been drawn and could cause a crash")
            return
        if self.checkString(name):
            logger.debug("empty name")
            return
        
        logger.debug(f"saving {name}")
        
        level = self.levelInput.text
        #create own pokemonObject
        if self.pokemonObject == None:
            logger.debug(f"creating new pokemon called {name}")
            self.pokemonObject = TrainerPokemon(name, level)
            createNewEntry = True
        # #decorate pokemonObject before saving it
        self.pokemonObject.level = level 
        #create Function for this shit
        self.pokemonObject.ability = self.abilityInput.text if not self.checkString(self.abilityInput.text) else None
        self.pokemonObject.heldItem = self.heldItemInput.text if not self.checkString(self.heldItemInput.text) else None

        #check if a new pokemon needs to be added to the roster
        if createNewEntry:
            logger.info(f"adding {self.pokemonObject.name} to {self.trainerObject.name}")
            self.trainerObject.pokemon = self.pokemonObject
            self.updateButtons()
            return
        
        #if object name differs from textinput, adjust name
        newName = None
        if name != self.trainerObject.name:
            newName = name
        
        #edit the pokemon
        self.trainerObject.editPokemon(self.pokemonObject, self.pokemonIndex, newName)
        self.updateButtons()
    
    def removePokemon(self, button):
        self.savePokemon()
        #remove pokemon from trainerObject
        self.trainerObject.removePokemon(self.pokemonObject.name, self.pokemonIndex)
        #show first pokemon again and update buttons
        pokemon = self.trainerObject.pokemon[0] if len(self.trainerObject.pokemon) > 0 else None
        self.showPokemon(0, pokemon)
        self.updateButtons()

    def checkString(self, text):
        """function that returns True when the given text consists of only whitespace or is empty"""
        return text.isspace() or text == ""

        
    

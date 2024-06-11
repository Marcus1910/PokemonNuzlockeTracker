from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from loggerConfig import logger
from transparentButton import TransparentButton
# from popup import RemovePokemonPopup
from utilityFunctions import validateTextInput
from trainerPokemon import TrainerPokemon
import os

class DetailedPokemonBox(BoxLayout):
    pokemonSpritesFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")
    def __init__(self, pokemonObject, updateHeader, *args, **kwargs):
        """DetailedPokemonBox used to give more info about a pokemon, buildlayout to build it, if given an pokemonObject it will fill it"""
        super().__init__(*args, **kwargs)
        self.pokemonObject = pokemonObject
        self.updateHeader = updateHeader
        self.moveList = [] #used for storing moves

        #forward declarations for clear_layout function
        self.pokemonBox = BoxLayout(orientation = "horizontal")
        self.additionalInfoBox = BoxLayout(orientation = "horizontal")
        self.pokemonChoice = BoxLayout(orientation = "horizontal", size_hint_y = 0.2, pos_hint = {"bottom": 1})

        self.buildPokemonLayout()
        if self.pokemonObject != None:
            self.fillPokemonLayout()
        self.add_widget(self.pokemonBox)

    
    def buildPokemonLayout(self):
        """builds the layout which shows everything from the pokemon; abilities, moves, etc. places everything inside of self.pokemonBox"""
        #create Name label and input
        self.nameInput = TextInput(hint_text = "Name", multiline = False, size_hint_x = 0.7)
        self.nameInput.bind(focus = self.updatePokemonName)
        self.levelInput = TextInput(hint_text = "Level", multiline = False, size_hint_x = 0.3)
        self.levelInput.bind(focus = self.updateLevel)
        self.nameLevelBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.15)
        #add pokemon image
        self.imageBox = BoxLayout(size_hint_y = 0.75)
        self.pokemonImage = Image(source = os.path.join(self.pokemonSpritesFolder, "0.png"), pos_hint = {"top": 1})
        self.pokemonImage.fit_mode = "contain"

        self.nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        
        #add information about pokemon, ability, held item, typing
        self.pokemonInfoBox = BoxLayout(orientation= "vertical", size_hint_x = 0.3, pos_hint = {"top": 1})
        self.abilityInput = TextInput(hint_text = "ability", multiline = False)
        self.abilityInput.bind(focus = self.updateAbility)
        self.heldItemInput = TextInput(hint_text = "held item", multiline = False)
        self.heldItemInput.bind(focus = self.updateHeldItem)
        self.typing1Input = TextInput(hint_text = "typing 1", multiline = False)
        self.typing2Input = TextInput(hint_text = "typing 2", multiline = False)

        self.moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3, pos_hint = {"top": 1})

        #code for removeButton
        self.defeatButton = Button(text = "Defeat Pokemon", on_press = self.pokemonObject.changeDefeated, size_hint_y = 0.1)
        self.removeButton = Button(text = "Remove Pokemon", size_hint_y = 0.1)
        
        #add everything to correct widgets
        self.nameLevelBox.add_widget(self.nameInput)
        self.nameLevelBox.add_widget(self.levelInput)

        self.imageBox.add_widget(self.pokemonImage)
        
        self.nameImageBox.add_widget(self.nameLevelBox)
        self.nameImageBox.add_widget(self.imageBox)
        self.nameImageBox.add_widget(self.defeatButton)
        self.nameImageBox.add_widget(self.removeButton)

        self.pokemonInfoBox.add_widget(self.abilityInput)
        self.pokemonInfoBox.add_widget(self.heldItemInput)
        self.pokemonInfoBox.add_widget(self.typing1Input)
        self.pokemonInfoBox.add_widget(self.typing2Input)

        self.pokemonBox.add_widget(self.nameImageBox)
        self.pokemonBox.add_widget(self.pokemonInfoBox)
        self.pokemonBox.add_widget(self.moveBox)
    
    def updatePokemonName(self, label, focus):
        """updates the pokemon Image and object name"""
        if focus:
            #entering text
            return
        pokemonName = validateTextInput(label.text)
        if pokemonName == None:
            return
        image = self.retrievePokemonImage(label.text)
        self.pokemonImage.source = image
        self.pokemonObject.name = pokemonName
        #update header so name and image are updated
        self.updateHeader()

   #TODO Fix this shittiness 
    def updateLevel(self, input, focus):
        if focus:
            return
        pokemonLevel = validateTextInput(input.text)
        if pokemonLevel == None:
            return
        level = int(input.text)
        self.pokemonObject.level = level
        self.updateHeader()
    
    def updateAbility(self, input, focus):
        if focus:
            return
        pokemonAbility = validateTextInput(input.text)
        if pokemonAbility == None:
            return
        ability = input.text
        self.pokemonObject.ability = ability
        self.updateHeader()
    
    def updateHeldItem(self, input, focus):
        if focus:
            return
        pokemonHeldItem = validateTextInput(input.text)
        if pokemonHeldItem == None:
            return
        hi = input.text
        self.pokemonObject.heldItem = hi
        self.updateHeader()
    
    def updateMoves(self, input, focus):
        if focus:
            return
        pokemonMove = validateTextInput(input.text)
        if pokemonMove == None:
            return        
        self.pokemonObject.moves = pokemonMove
        self.clearMoveBox()
        self.fillMoveBox()
        self.updateHeader()
    
    def removeMove(self, instance):
        move = instance.text
        self.pokemonObject.deleteMove(move)
        #remove button
        self.moveBox.remove_widget(instance)
        self.updateHeader()

    def retrievePokemonImage(self, name: str) -> str:
        """returns location of the pokemon image or the 0.png, TODO centralized place"""
        logger.debug(f"searching for image of {name}")
        imagePath = os.path.join(self.pokemonSpritesFolder, f"{name.lower()}.png")
        if os.path.exists(imagePath):
            logger.debug(f"found image for {name}")
            return imagePath
        else:
            logger.debug(f"could not find image for {name}")
            return os.path.join(self.pokemonSpritesFolder, f"0.png")

    def fillPokemonLayout(self):
        """fills in the layout made by buildPokemonLayout function, needs pokemon object to do so"""
        self.nameInput.text = self.pokemonObject.name
        self.levelInput.text = str(self.pokemonObject.level)
        self.pokemonImage.source = self.retrievePokemonImage(self.pokemonObject.name)
        
        if self.pokemonObject.ability is not None:
            self.abilityInput.text = self.pokemonObject.ability
        if self.pokemonObject.heldItem != "n/a" and self.pokemonObject.heldItem != None:
            self.heldItemInput.text = self.pokemonObject.heldItem
        self.fillMoveBox()
        
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

        
        self.additionalInfoBox.add_widget(self.baseStatBox)
        self.additionalInfoBox.add_widget(self.possibleAbilitiesBox)
        self.additionalInfoBox.add_widget(self.possibleMovesBox)
    
    def fillMoveBox(self) -> None:
        for index, move in enumerate(self.pokemonObject.moves):
            self.moveBox.add_widget(TransparentButton(text = move, on_release = self.removeMove))
        moveInput = TextInput(hint_text = f"enter new move", multiline = False)
        moveInput.bind(focus = self.updateMoves)
        self.moveBox.add_widget(moveInput)
    
    def clearMoveBox(self) -> None:
        self.moveBox.clear_widgets()

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

    def changeBaseStats(self, instance):
        logger.info("changing BaseStat graph")

        
    

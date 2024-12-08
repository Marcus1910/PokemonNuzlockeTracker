from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

import os

from GUI.transparentButton import TransparentButton
from GUI.Dialog.deleteDialog import DeleteTrainerPokemonPopup

from Logic.games import getItemSprite, getPokemonSprite, getTrainerSprite
from Logic.utilityFunctions import validateTextInput
from loggerConfig import logger

class DetailedPokemonBox(MDBoxLayout):
    def __init__(self, pokemonObject, *args, **kwargs):
        """DetailedPokemonBox used to give more info about a pokemon, buildlayout to build it, if given an pokemonObject it will fill it"""
        super().__init__(*args, **kwargs)
        self.pokemonObject = pokemonObject
        self.moveList = [] #used for storing moves

        #forward declarations for clear_layout function
        self.pokemonBox = MDBoxLayout(orientation = "horizontal")
        self.additionalInfoBox = MDBoxLayout(orientation = "horizontal")
        self.pokemonChoice = MDBoxLayout(orientation = "horizontal", size_hint_y = 0.2, pos_hint = {"bottom": 1})

        self.buildPokemonLayout()
        if self.pokemonObject != None:
            self.fillPokemonLayout()
        self.add_widget(self.pokemonBox)
    
    def buildPokemonLayout(self):
        """builds the layout which shows everything from the pokemon; abilities, moves, etc. places everything inside of self.pokemonBox"""
        #create Name label and input
        self.nameInput = TextInput(hint_text = "Name", multiline = False, size_hint_x = 0.7)
        self.nameInput.bind(focus = self.updatePokemonName)
        self.pokemonObject.addNameObserver(self.updatePokemonImage)

        self.levelInput = TextInput(hint_text = "Level", multiline = False, size_hint_x = 0.3)
        self.levelInput.bind(focus = self.updateLevel)
        self.nameLevelBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.15)
        #add pokemon image
        self.imageBox = BoxLayout(size_hint_y = 0.75)
        self.pokemonImage = Image(source = getPokemonSprite("0.png"), pos_hint = {"top": 1})
        self.pokemonImage.fit_mode = "contain"

        self.nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        
        #add information about pokemon, ability, held item, typing
        self.pokemonInfoBox = BoxLayout(orientation= "vertical", size_hint_x = 0.3, pos_hint = {"top": 1})
        self.abilityBox = BoxLayout(orientation = "vertical", size_hint_y = 0.5)
        self.abilityInput = TextInput(hint_text = "ability", multiline = False)
        self.abilityInput.bind(focus = self.updateAbility)
        self.abilityBox.add_widget(self.abilityInput)

        self.heldItemInput = TextInput(hint_text = "held item", multiline = False, size_hint_y = 0.1)
        self.heldItemInput.bind(focus = self.updateHeldItem)

        self.typing1Input = TextInput(hint_text = "typing 1", multiline = False, size_hint_y = 0.1)
        self.typing2Input = TextInput(hint_text = "typing 2", multiline = False, size_hint_y = 0.1)

        self.moveBox = BoxLayout(orientation = "vertical", size_hint_y = 0.3)
        self.pokemonObject.addLearnedMoveObserver(self.updateMoveBox)

        self.possibleMoveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3, pos_hint = {"top": 1})
    
        self.removeButton = TransparentButton(text = "Remove Pokemon", size_hint_y = 0.1, on_release = self.deletePokemonPopup)
        self.removeButton.redColor()
        
        #add everything to correct widgets
        self.nameLevelBox.add_widget(self.nameInput)
        self.nameLevelBox.add_widget(self.levelInput)

        self.imageBox.add_widget(self.pokemonImage)
        
        self.nameImageBox.add_widget(self.nameLevelBox)
        self.nameImageBox.add_widget(self.imageBox)
        self.nameImageBox.add_widget(self.removeButton)

        self.pokemonInfoBox.add_widget(self.abilityBox)
        self.pokemonInfoBox.add_widget(self.heldItemInput)
        self.pokemonInfoBox.add_widget(self.typing1Input)
        self.pokemonInfoBox.add_widget(self.typing2Input)
        self.pokemonInfoBox.add_widget(self.moveBox)

        self.pokemonBox.add_widget(self.nameImageBox)
        self.pokemonBox.add_widget(self.pokemonInfoBox)
        self.pokemonBox.add_widget(self.possibleMoveBox)

    def fillPokemonLayout(self):
        """fills in the layout made by buildPokemonLayout function, needs pokemon object to do so"""
        self.nameInput.text = self.pokemonObject.name
        self.levelInput.text = str(self.pokemonObject.level)
        self.pokemonImage.source = self.retrievePokemonImage(self.pokemonObject.name)
        
        self.updateAbilities()
        if self.pokemonObject.heldItem != "n/a" and self.pokemonObject.heldItem != None:
            self.heldItemInput.text = self.pokemonObject.heldItem
        self.fillMoveBox()
        self.fillPossibleMoveBox()
    
    def updateMoveBox(self) -> None:
        self.clearMoveBox()
        self.fillMoveBox()
    
    def updateAbilities(self) -> None:
        abilities = self.pokemonObject.getAbilities()
        for ability in abilities:
            abilityButton = TransparentButton(text = ability, on_release = lambda btn, ability = ability: self.addAbility(ability))
            self.abilityBox.add_widget(abilityButton)
    
    def addAbility(self, ability) -> None:
        self.pokemonObject.ability = ability

    def fillMoveBox(self) -> None:
        for index, move in enumerate(self.pokemonObject.learnedMoves):
            self.moveBox.add_widget(TransparentButton(text = move, on_release = self.removeMove))
    
    def fillPossibleMoveBox(self) -> None:
        self.possibleMoveBox.clear_widgets()
        possibleMoves = self.pokemonObject.getLevelupMoves()
        for level, move in possibleMoves.items():
            #create level label and move button
            moveBox = BoxLayout(orientation = "horizontal")
            levelLabel = Label(text = str(level), size_hint_x = 0.2)
            moveButton = TransparentButton(text = move, size_hint_x = 0.8, on_release = lambda btn, move=move: self.addLearnedMove(move))
            moveBox.add_widget(levelLabel)
            moveBox.add_widget(moveButton)
            self.possibleMoveBox.add_widget(moveBox)
        moveInput = TextInput(hint_text = f"enter new move", multiline = False)
        moveInput.bind(focus = self.updateMoves)
        self.possibleMoveBox.add_widget(moveInput)
        

    
    def clearMoveBox(self) -> None:
        self.moveBox.clear_widgets()

    def changeBaseStats(self, instance):
        logger.info("changing BaseStat graph")
    
    def updatePokemonName(self, label, focus) -> None:
        """updates the pokemon Image and object name"""
        if focus:
            #entering text
            return
        pokemonName = validateTextInput(label.text)
        if pokemonName == None:
            return
        self.pokemonObject.name = pokemonName
        

    def updatePokemonImage(self) -> None:
        """updates pokemon Image"""
        image = self.retrievePokemonImage(self.pokemonObject.name)
        self.pokemonImage.source = image
 
    def updatePokemonAttribute(self, input, focus, attribute):
        if focus:
            return
        attributeValue = validateTextInput(input.text)
        if attributeValue == None:
            return 
        setattr(self.pokemonObject, attribute, attributeValue)

    def updateLevel(self, input, focus):
        self.updatePokemonAttribute(input, focus, "level")
    
    def updateAbility(self, input, focus):
        self.updatePokemonAttribute(input, focus, "ability")
    
    def updateHeldItem(self, input, focus):
        self.updatePokemonAttribute(input, focus, "heldItem")
    
    def updateMoves(self, input, focus):
        if focus:
            return
        pokemonMove = validateTextInput(input.text)
        if pokemonMove == None:
            return        
        self.addLearnedMove(pokemonMove)
    
    def addLearnedMove(self, move) -> None:
        self.pokemonObject.learnedMoves = move
    
    def removeMove(self, instance):
        move = instance.text
        self.pokemonObject.deleteLearnedMove(move)
        #remove button
        self.moveBox.remove_widget(instance)
    
    def deletePokemonPopup(self, instance):
        """dialog that asks whether you want to delete the pokemon or cancel deletion"""
        dialog = DeleteTrainerPokemonPopup(self.pokemonObject.name, self.pokemonObject.trainer.name)
        dialog.open()
        dialog.bind(on_dismiss = self.removePokemon)
    
    def removePokemon(self, instance):
        """removes the pokemon from the trainer and puts it into the lost&found section"""
        if instance.result:
            if self.pokemonObject.removePokemon():
                return
            logger.error(f"{self.pokemonObject.name} could not be removed")
            return
        else:
            logger.debug(f"not deleting pokemon")


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



        
    

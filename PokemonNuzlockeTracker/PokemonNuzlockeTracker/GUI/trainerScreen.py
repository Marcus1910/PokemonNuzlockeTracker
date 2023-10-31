from nuzlockeScreen import NuzlockeScreen
from detailedPokemonBox import DetailedPokemonBox
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.switch import Switch
import time

import games as gm
import os

class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)

        #spinner to select trainer
        self.defaultTrainerText = "Select Trainer"
        self.trainerSpinner = Spinner(text = self.defaultTrainerText, values = ["New Trainer"], size_hint_y = 0.04)
        self.trainerSpinner.bind(text = self.updateTrainerBox)
        self.trainerSpinner.background_color = gm.opaque
        #box that contains all pokemon from trainer
        self.trainerBox = BoxLayout(size_hint_y = 0.71, orientation = "vertical")
        #used for detailed view
        self.detailedPokemonBox = DetailedPokemonBox(orientation = "horizontal", size_hint_y = 0.51)

        self.viewBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.05, padding = (0, 0, 0, 10))
        self.viewLabel = Label(text = "view mode: ", size_hint_x = 0.15, padding = (0, 0, 50, 0))
        self.viewSpinner = Spinner(values = ["global", "detailed"], size_hint_x = 0.15, pos_hint = {"right": 1}, padding = (10, 0, 0, 0), text_autoupdate = True)
        self.viewSpinner.bind(text = self.updateTrainerBox)

        self.spriteFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemonMinimalWhitespace")

        self.viewBox.add_widget(self.viewLabel)
        self.viewBox.add_widget(self.viewSpinner)

        self.layout.add_widget(self.trainerSpinner)
        self.layout.add_widget(self.viewBox)
        self.layout.add_widget(self.trainerBox)

    def on_pre_enter(self):
        print("pre enter trainer")
        if not super().on_pre_enter():
            return
    
    def areaChanged(self, spinner, text):
        super().areaChanged(spinner, text)
        self.updateTrainers()
        self.trainerSpinner.text = self.defaultTrainerText

    def updateTrainers(self):
        spinnerList = []
        areaObject = self.manager.currentArea
        self.trainers = areaObject.trainers
        if len(self.trainers) > 0:
            spinnerList = [trainer for trainer in self.trainers.keys()]
        spinnerList.append("New Trainer")
        self.trainerSpinner.values = spinnerList
        self.clearTrainerBox()
    
    def updateTrainerBox(self, spinner, text):
        """function that gets called by trainerspinner and viewSpinner, changes trainer and UI"""
        self.changeTrainerSpinnerColor(gm.opaque)
        self.detailedPokemonBox.clearLayout()
        self.clearTrainerBox()
        selectedTrainer = self.trainerSpinner.text
        viewMode = self.viewSpinner.text
        self.showTrainer(selectedTrainer, viewMode)
    
    def showTrainer(self, selectedTrainer, view):
        """selects correct trainer object and choses correct UI to display pokemon"""
        if selectedTrainer == self.defaultTrainerText:
            #default value for trainerspinner so do nothing
            return
        if selectedTrainer == "New Trainer":

            #TODO Call to new Trainer
            return
        for trainerName, trainerObject in self.trainers.items():
            if trainerName == selectedTrainer:
                break
        else:
            print(f"trainer {selectedTrainer} not found")

        #change the color of the trainer spinner based on defeated status
        color = gm.green if trainerObject.defeated else gm.red
        self.changeTrainerSpinnerColor(color)

        #change trainerbox layout to selected view
        self.changeView(view, trainerObject)

    def changeTrainerSpinnerColor(self, color: tuple):
        """changes trainerspinner color to green if trainer is defeated else turns to red"""
        newColor = color[0:3] + (gm.opaque[3],)
        self.trainerSpinner.background_color = newColor
        
    def changeView(self, view, trainerObject):
        """function that changes the view to detailed or global"""
        if view == "global":
            self.showGlobalView(trainerObject)
        elif view == "detailed":
            self.showDetailedView(trainerObject)
        else:
            print(f"{view} has not been found")

        
    def clearTrainerBox(self):
        self.trainerBox.clear_widgets()

    def showGlobalView(self, trainerObject):
        for index, pokemonObject in enumerate(trainerObject.pokemon):
            #gather pokemon data and put it in Labels
            pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = (1 - 0.05)/ (len(trainerObject.pokemon)), padding = (0, 0, 0, 10))
            #create Image with name underneath
            imageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
            pokemonImage = Image(source = os.path.join(self.spriteFolder, f"{pokemonObject.name.lower()}.png"))
            pokemonImage.fit_mode = "contain"
            nameLevelLabel = Label(text = f"{pokemonObject.name} lvl {pokemonObject.level}", color = self.standardColor, pos_hint = {"right": 1})
            
            itemAbilityBox = BoxLayout(orientation = "vertical", size_hint_x = 0.1)
            abilityInput = Label(text = f"{pokemonObject.ability}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"top" : 1})
            heldItemInput = Label(text = f"{pokemonObject.heldItem}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"bottom" : 1})
            
            moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)

            for moveIndex in range(4): 
                moveSlot = Label(text = f"Not revealed", color = self.standardColor)
                if moveIndex < len(pokemonObject.moves):
                    moveSlot.text = f"{pokemonObject.moves[moveIndex]}"
                moveBox.add_widget(moveSlot)


            imageBox.add_widget(pokemonImage)
            imageBox.add_widget(nameLevelLabel)
            pokemonBox.add_widget(imageBox)

            itemAbilityBox.add_widget(abilityInput)
            itemAbilityBox.add_widget(heldItemInput)

            pokemonBox.add_widget(itemAbilityBox)
            pokemonBox.add_widget(moveBox)
        
            self.trainerBox.add_widget(pokemonBox)
        
    def showDetailedView(self, trainerObject):
        """creates buttons for detailed view"""
        pokemonChoice = BoxLayout(orientation = "horizontal", size_hint_y = 0.2, pos_hint = {"bottom": 1})
        buttonSize = 1 / len(trainerObject.pokemon)
        for pokemon in trainerObject.pokemon:
            pokemonButton = Button(text = pokemon.name, size_hint_x = buttonSize)
            pokemonButton.bind(on_press = lambda instance, pokemonObject = pokemon: self.showDetailedPokemon(pokemonObject))
            pokemonChoice.add_widget(pokemonButton)
        self.trainerBox.add_widget(self.detailedPokemonBox)
        self.trainerBox.add_widget(pokemonChoice)
    
    def showDetailedPokemon(self, pokemonObject):
        """fills detailedPokemonBox with pokemon information"""
        print(pokemonObject.name)
        self.detailedPokemonBox.clearLayout()
        self.detailedPokemonBox.buildLayout()
        self.detailedPokemonBox.fillLayout(pokemonObject)
        

    def prints(self, move):
        print(f"prints: {move}")

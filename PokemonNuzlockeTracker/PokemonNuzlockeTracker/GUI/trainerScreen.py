from nuzlockeScreen import NuzlockeScreen
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

import games as gm
import os

class TrainerScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(TrainerScreen, self).__init__(screenName = screenName, **kwargs)
        #spinner to select trainer
        self.trainerSpinner = Spinner(text = "select Trainer", values = "New Trainer", size_hint_y = 0.08)
        self.trainerSpinner.bind(text = self.showTrainer)
        self.trainerSpinner.background_color = gm.opaque
        #box that contains all pokemon from trainer
        self.trainerBox = BoxLayout(size_hint_y = 0.67, orientation = "vertical")
        self.spriteFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites", "pokemon")
        self.layout.add_widget(self.trainerSpinner)
        self.layout.add_widget(self.trainerBox)

    
    def on_pre_enter(self):
        if not super().on_pre_enter():
            return
        self.updateTrainers()
    
    def areaChanged(self, spinner, text):
        super().areaChanged(spinner, text)
        self.updateTrainers()
        
    def updateTrainers(self):
        spinnerList = []
        areaObject = self.manager.currentArea
        self.trainers = areaObject.trainers
        if len(self.trainers) > 0:
            spinnerList = [trainer for trainer in self.trainers.keys()]
        spinnerList.append("New Trainer")
        self.trainerSpinner.values = spinnerList
        self.clearTrainerBox()
    
    def showTrainer(self, spinner, text):
        self.clearTrainerBox()
        if text == "New Trainer":
            return
        for trainerName, trainerObject in self.trainers.items():
            if trainerName == text:
                break
        else:
            print(f"trainer {trainerName} not found")
        #add trainer attributes
        self.trainerLabel = Label(text = f"{trainerObject.name} {trainerObject.gender} {trainerObject.defeated}", size_hint_y = 0.05, pos_hint = {"top" : 1})
        self.trainerBox.add_widget(self.trainerLabel)
        #add pokemon
        for index, pokemonObject in enumerate(trainerObject.pokemon):
            #gather pokemon data and put it in textInputs
            print(pokemonObject.name)
            size = (1 - 0.05)/ (len(trainerObject.pokemon))
            print(f"size: {size}")
            pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = (1 - 0.05)/ (len(trainerObject.pokemon)))
            #create Image with name underneath
            imageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
            #imgButton = Button(text = "image", size_hint_y = 0.7, pos_hint = {"top" : 1})
            pokemonImage = Image(source = os.path.join(self.spriteFolder, f"{pokemonObject.name.lower()}.png"))
            pokemonImage.allow_stretch = True
            pokemonImage.keep_ratio = True
            
            nameLevelBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.3, pos_hint = {"bottom" : 1})
            nameInput = TextInput(text = f"{pokemonObject.name}", background_normal="", background_color=(1, 1, 1, 0.5), size_hint_x = 0.6)
            levelLabel = TextInput(text = f"lvl:", size_hint_x = 0.2, background_normal="", background_color=(1, 1, 1, 0.5))
            #easier than making a label transparent
            levelLabel.disabled = True
            levelInput = TextInput(text = f"{pokemonObject.level}", background_normal="", background_color=(1, 1, 1, 0.5),size_hint_x = 0.2)
            
            itemAbilityBox = BoxLayout(orientation = "vertical", size_hint_x = 0.2)
            abilityInput = TextInput(text = f"{pokemonObject.ability}", background_normal="", background_color=(1, 1, 1, 0.5), size_hint_y = 0.5, pos_hint = {"top" : 1})
            heldItemInput = TextInput(text = f"{pokemonObject.heldItem}", background_normal="", background_color=(1, 1, 1, 0.5), size_hint_y = 0.5, pos_hint = {"bottom" : 1})
            
            moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.2)

            for moveIndex in range(4): 
                moveSlot = TextInput(text = f"", background_normal="", background_color=(1, 1, 1, 0.5))
                if moveIndex < len(pokemonObject.moves):
                    moveSlot.text = f"{pokemonObject.moves[moveIndex]}"
                moveBox.add_widget(moveSlot)

            nameLevelBox.add_widget(nameInput)
            nameLevelBox.add_widget(levelLabel)
            nameLevelBox.add_widget(levelInput)

            imageBox.add_widget(pokemonImage)
            imageBox.add_widget(nameLevelBox)
            pokemonBox.add_widget(imageBox)

            itemAbilityBox.add_widget(abilityInput)
            itemAbilityBox.add_widget(heldItemInput)

            pokemonBox.add_widget(itemAbilityBox)
            pokemonBox.add_widget(moveBox)
        
            self.trainerBox.add_widget(pokemonBox)
    
    def clearTrainerBox(self):
        self.trainerBox.clear_widgets()


        


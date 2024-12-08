from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.dropdown import DropDown
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton

from kivy.uix.button import Button
from kivy.uix.image import Image

from GUI.Dialog.addDialog import AddDialog
from GUI.transparentButton import TransparentButton

from Logic.databaseModels import TrainerPokemon, Trainer
from loggerConfig import logger
# from pokemon import TrainerPokemon

class AddPokemonDialog(AddDialog):
    def __init__(self, trainerRecord: Trainer, updateFuncion: callable, **kwargs):
        self.manager = MDApp.get_running_app().windowManager
        self.trainerRecord = trainerRecord
        self.updateFunction = updateFuncion
        self.title = f"Add Pokemon to {self.trainerRecord.name}"
        self.content = AddEditPokemonBox(size_hint_y = None)
        self.content_cls = self.content
        
        super().__init__(**kwargs)
        
        self.okButton.text = "Add"
        
    def onOk(self, instance):
        trainerPokemon = self.content.createTrainerPokemonRecord(self.trainerRecord.IDtrainer)
        if trainerPokemon != None:
            if self.manager.insertRecord(trainerPokemon):
                self.updateFunction()
                self.dismiss()

class EditPokemonDialog(AddDialog):
    def __init__(self, trainerPokemonRecord: TrainerPokemon, updateFuncion: callable, **kwargs):
        self.manager = MDApp.get_running_app().windowManager
        self.trainerPokemonRecord = trainerPokemonRecord
        self.updateFunction = updateFuncion
        self.title = f"Edit Pokemon"
        self.okButton.text = "Add"
        self.content = AddEditPokemonBox(True, self.trainerPokemonRecord, size_hint_y = None)
        self.content_cls = self.content
        
        super().__init__(**kwargs)
        
    def onOk(self, instance):
        trainerPokemon = self.content.updateTrainerPokemonRecord()
        if trainerPokemon != None:
            if self.manager.insertRecord(trainerPokemon):
                self.updateFunction()
                self.dismiss()

class AddEditPokemonBox(MDBoxLayout):
    def __init__(self, trainerPokemonRecord: TrainerPokemon | None = None, **kwargs):
        """giving trainerPokemonRecord automatically means editing pokemon"""
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.height = "200dp"
        self.width = "100dp"
        self.trainerPokemonRecord = trainerPokemonRecord
        
        self.moveList = []
        self.pokemonBox = MDBoxLayout()
        
        self.buildLayout()
        if self.trainerPokemonRecord != None:
            self.fillLayout()
        self.add_widget(self.pokemonBox)
            
        
        #base pokemon
        #abilityslot -> LU -> also invoer
        #gender -> LU
        #isDefeated -> only edit
        #helditem -> not required -> LU
        #moves -> not required

        
    def buildLayout(self):
        self.pokemonTextField = MDTextField(hint_text = "Pokemon")
        
        self.pokemonBox.add_widget(self.pokemonTextField)


    def fillLayout(self):
        self.moveList = self.manager.getPokemonLevelupMoves(self.trainerPokemonRecord.IDPokemon)
        pass
    
    def createTrainerPokemonRecord(self, IDTrainer: int) -> TrainerPokemon:
        #Trainer, pokemon, idabilityslot, gender, defeated = False, helditem, move 1, move 2, move3, move4
        trainerPokemon = TrainerPokemon()
        return trainerPokemon

    def updateTrainerPokemonRecord(self) -> bool:
        pass

        
    def getInput(self):
        name = self.pokemonName.text
        level = self.pokemonLevel.text
        trainerPokemonRecord = TrainerPokemon(name, level)
        return trainerPokemonRecord

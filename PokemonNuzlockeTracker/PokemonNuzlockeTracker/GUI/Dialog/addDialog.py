from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.image import Image

from GUI.detailedPokemonBox import DetailedPokemonBox

from Logic.games import getItemSprite, getPokemonSprite
from Logic.databaseModels.game import newTrainerString
from Logic.databaseModels.trainer import Trainer
from Logic.utilityFunctions import validateFields
from loggerConfig import logger

class AddDialog(MDDialog):
    def __init__(self, **kwargs):
        self.auto_dismiss = False
        self.type = "custom"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        self.okButton = MDFlatButton(text = "add", on_release = self.onOK)
        self.cancelButton = MDFlatButton(text = "discard", on_release = self.dismiss)
        self.deleteButton = MDFlatButton(text = "delete", md_bg_color = "red", opacity = 0, disabled = False)
        self.buttons = [self.deleteButton,self.okButton, self.cancelButton]
        super().__init__(**kwargs)  
    
    def onOK(self, instance):
        self.dismiss()

class EditDialog(AddDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.okButton.text = "save changes"
        self.cancelButton.text = "discard changes"
        self.deleteButton.opacity = 1
        self.deleteButton.disabled = False
        self.deleteButton.bind(on_release = self.onDelete)
    
    def onDelete(self, instance):
        self.onOK(instance)


class AddItemDialog(AddDialog):
    def __init__(self, addItemFunction, **kwargs):
        self.title = "Add new item"
        self.content = AddItemBox(size_hint_y = None)
        self.addItemFunction = addItemFunction
        self.content_cls = self.content
        
        super().__init__(**kwargs)
    
    def onOK(self, instance) -> None:
        """creates itemObject and adds it to area"""
        itemObject = self.content.makeItemObject()
        if itemObject != 0:
            if self.addItemFunction(itemObject):
                self.dismiss()

    def dismiss(self, *args):
        self.content.resetFields()
        super().dismiss()

class AddItemBox(MDBoxLayout):
    def __init__(self, **kwargs):
        """provides input fields to create Item Object"""
        super().__init__(**kwargs)
        self.height = "200dp"
        self.inputBox = MDBoxLayout(orientation = "vertical")
        self.errorLabel = MDLabel(size_hint_y = 0.1, theme_text_color = "Error")
        self.itemName = MDTextField(hint_text = "Item name", pos_hint = {"top": 1})
        self.itemName.bind(focus = self.updateImage)

        self.inputBox.add_widget(self.errorLabel)
        self.inputBox.add_widget(self.itemName)

        self.itemImage = Image(fit_mode = "contain")

        self.orientation = "horizontal"
        self.add_widget(self.inputBox)
        self.add_widget(self.itemImage)

    def makeItemObject(self):
        pass
        # name = self.itemName.text
        # if checkString(name):
        #     self.errorLabel.text = "please enter name"
        #     return 0
        # self.errorLabel.text = ""
        # itemObject = Item(name)
        # return itemObject

    def updateImage(self, input, focus):
        if focus:
            return
        self.itemImage.source = getItemSprite(input.text)

    def resetFields(self):
        self.errorLabel.text = ""
        self.itemName.text = ""
        self.itemImage.source = ""

class ConvertEncounteredPokemonToPlayerPokemonDialog(AddDialog):
    def __init__(self, encounteredPokemon, areaName, **kwargs):
        self.encounteredPokemon = encounteredPokemon
        self.areaName = areaName
        self.title = f"Catch {encounteredPokemon.name}"
        self.content = self.createContent()
        self.content_cls = self.content
        super().__init__(**kwargs)
    
    def createContent(self) -> MDBoxLayout:
        return ConvertPokemonBox(self.encounteredPokemon, size_hint_y = None)

    def onOK(self, instance):
        pokemon = self.content.convert() 
        MDApp.get_running_app().game.catchPokemon(pokemon, self.areaName)
        self.dismiss()

    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()

class ConvertPokemonBox(MDBoxLayout):
    def __init__(self, pokemonObject, **kwargs):
        super().__init__(**kwargs)
        self.pokemonObject = pokemonObject
        self.height = "200dp"
        self.orientation = "vertical"
        self.errorLabel = MDLabel(size_hint_y = 0.1, theme_text_color = "Error")
        self.pokemonImage = Image(source = getPokemonSprite(pokemonObject.name), fit_mode = "contain")
        self.pokemonName = MDLabel(text = pokemonObject.name)
        self.pokemonNickName = MDTextField(hint_text = f"Nickname for {pokemonObject.name}")
        #self.level = MDDropDownItem(text = )
        self.ability = MDTextField(hint_text = "Ability")
        self.heldItem = MDTextField(hint_text = "Held item")
        #self.gender
        
        nickNameHeldItemBox = MDBoxLayout(orientation = "vertical")
        nickNameHeldItemBox.add_widget(self.pokemonNickName)
        nickNameHeldItemBox.add_widget(self.heldItem)

        levelAbilityGenderBox = MDBoxLayout(orientation = "vertical")
        levelAbilityGenderBox.add_widget(self.ability)
        #levelAbilityGenderBox.add_widget(self.level)
        #levelAbilityGenderBox.add_widget(self.gender)

        pokemonBox = MDBoxLayout(orientation = "horizontal")
        
        pokemonBox.add_widget(nickNameHeldItemBox)
        pokemonBox.add_widget(levelAbilityGenderBox)
        pokemonBox.add_widget(self.pokemonImage)

        self.add_widget(self.errorLabel)
        self.add_widget(pokemonBox)
    
    def validateInput(self):
        #level
        
        return
    
    def resetFields(self):
        self.errorLabel.text = ""
        self.pokemonImage.source = ""
        self.pokemonName.text = ""
        self.pokemonNickName.text = ""
        #self.level
        self.ability.text = ""
        self.heldItem.text = ""
        #self.gender

    def showError(self, error: str) -> None:
        self.errorLabel.text = error
    
    def convert(self):
        pokemon = PlayerPokemon(self.pokemonObject.name, 22, nickName = self.pokemonNickName.text, ability = self.ability.text, heldItem = self.heldItem.text)
        return pokemon
    



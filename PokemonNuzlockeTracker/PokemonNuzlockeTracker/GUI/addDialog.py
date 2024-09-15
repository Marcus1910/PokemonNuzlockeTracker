from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.image import Image

from utilityFunctions import checkString, validateTextInput
from loggerConfig import logger
from trainer import Trainer
from item import Item
from pokemon import PlayerPokemon
from detailedPokemonBox import DetailedPokemonBox
from games import getTrainerSprite, getItemSprite, getPokemonSprite

class AddDialog(MDDialog):
    def __init__(self, **kwargs):
        self.auto_dismiss = False
        self.type = "custom"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        self.okButton = MDFlatButton(text = "apply", on_release = self.onOK)
        self.cancelButton = MDFlatButton(text = "discard", on_release = self.dismiss)
        self.buttons = [self.okButton, self.cancelButton]
        super().__init__(**kwargs)
    
    def onOK(self):
        self.dismiss()


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
        name = self.itemName.text
        if checkString(name):
            self.errorLabel.text = "please enter name"
            return 0
        self.errorLabel.text = ""
        itemObject = Item(name)
        return itemObject

    def updateImage(self, input, focus):
        if focus:
            return
        self.itemImage.source = getItemSprite(input.text)

    def resetFields(self):
        self.errorLabel.text = ""
        self.itemName.text = ""
        self.itemImage.source = ""


class AddTrainerDialog(AddDialog):
    def __init__(self, addTrainerFunction, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = "Add new trainer"
        self.content = AddTrainerBox(size_hint_y = None)
        self.addTrainerFunction = addTrainerFunction
        self.content_cls = self.content

        super().__init__(**kwargs)
    
    def onOK(self, instance) -> None:
        trainerObject = self.content.makeTrainerObject()
        if trainerObject != 0:
            #input is correct, create new Object for Area
            if self.addTrainerFunction(trainerObject):
                self.dismiss()

    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()

class AddTrainerBox(MDBoxLayout): 
    def __init__(self, **kwargs):
        """Provides input field to create Trainer object"""
        super().__init__(**kwargs)
        self.height = "200dp"

        self.errorLabel = MDLabel(size_hint_y = 0.1, theme_text_color = "Error")
        self.trainerName = MDTextField(hint_text = "Trainer name")
        self.trainerType = MDTextField(hint_text = "Trainer type")
        self.trainerType.bind(focus = self.updateImage)
        self.trainerGender = MDTextField(hint_text = "Gender: M/F")
        self.bossTrainerLabel = MDLabel(text = "Boss trainer", pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.bossCheck = MDSwitch(pos_hint = {'center_x': 0.5, 'center_y': 0.5}, width = "64dp")

        self.trainerImage = Image(fit_mode = "contain")

        self.bossBox = MDBoxLayout(orientation = "horizontal", padding = [0, 20, 0, 0])
        self.bossBox.add_widget(self.bossTrainerLabel)
        self.bossBox.add_widget(self.bossCheck)

        self.trainerInfoBox = MDBoxLayout(orientation = "vertical")
        self.trainerInfoBox.add_widget(self.trainerName)
        self.trainerInfoBox.add_widget(self.trainerType)
        self.trainerInfoBox.add_widget(self.trainerGender)
        self.trainerInfoBox.add_widget(self.bossBox)

        self.trainerBox = MDBoxLayout(orientation = "horizontal")
        self.trainerBox.add_widget(self.trainerInfoBox)
        self.trainerBox.add_widget(self.trainerImage)

        self.orientation = "vertical"
        self.add_widget(self.errorLabel)
        self.add_widget(self.trainerBox)

    def clearLayout(self):
        self.clear_widgets()
    
    def updateImage(self, input, focus):
        """updates trainer image to last trainertype update"""
        if focus:
            return
        self.trainerImage.source = getTrainerSprite(input.text)
    
    def validateTextFields(self):
        name = self.trainerName.text
        if checkString(name):
            logger.error(f"No name has been supplied for the new trainer, please enter name")
            self.showError("Please give a name to the trainer")
            return 0 
        return 1
    
    def makeTrainerObject(self, *args) -> bool:
        """validates textfield input, returns 0 if something is wrong, else the trainerObject"""
        if not self.validateTextFields():
            return 0
        #create trainerObject
        trainerObject = Trainer(name = self.trainerName.text)

        #decorate object
        trainerObject.gender = validateTextInput(self.trainerGender.text)
        trainerObject.trainerType = validateTextInput(self.trainerType.text)

        return trainerObject
    
    def showError(self, error: str) -> None:
        self.errorLabel.text = error
    
    def resetFields(self):
        self.trainerName.text = ""
        self.trainerImage.source = ""
        self.trainerGender.text = ""
        self.trainerType.text = ""
        self.bossCheck.active = False
        self.errorLabel.text = ""

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
    



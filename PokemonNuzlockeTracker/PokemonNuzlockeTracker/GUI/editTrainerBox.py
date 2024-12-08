from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from GUI.transparentButton import TransparentButton
from GUI.Dialog.deleteDialog import DeleteTrainerPopup

from Logic.utilityFunctions import validateTextInput
from Logic.games import getTrainerSprite

from loggerConfig import logger


class EditTrainerBox(BoxLayout): 
    def __init__(self, trainerRecord, *args, **kwargs):
        """creates a boxlayout, use buildlayout fill in the layout"""
        super().__init__(*args, **kwargs)
        self.trainerRecord = trainerRecord
        # self.trainerRecord.addDefeatedObserver(self.changeDefeatedButton)
        # self.trainerRecord.addAttributeObserver(self.fillLayout)
        # self.trainerRecord.addAttributeObserver(self.updateTrainerImage)
        self.buildLayout()

    def buildLayout(self):
        """Builds the layout to edit a trainer also calls the function to fill it with data"""
        self.trainerName = TextInput(hint_text = "Name", size_hint_y = 0.3, multiline = False)
        self.trainerName.bind(focus = self.updateName)
        self.trainerType = TextInput(hint_text = "Trainer Type", size_hint_y = 0.2, multiline = False)
        self.trainerType.bind(focus = self.updateType)
        self.trainerGender = TextInput(hint_text = "Gender: M/F", size_hint_y = 0.2, multiline = False)
        self.trainerGender.bind(focus = self.updateGender)
        self.trainerDefeatedButton = TransparentButton(text = "defeated", on_press = self.setDefeated, size_hint_y = 0.6)
        self.removeTrainerButton = TransparentButton(text = "remove trainer", bold = True, on_press = lambda btn: self.deleteTrainerPopup())
        self.removeTrainerButton.redColor()
        self.trainerImageBox= BoxLayout(size_hint_y = 0.8)
        self.trainerImage = Image(fit_mode = "contain")
        self.updateTrainerImage()
        self.trainerImageBox.add_widget(self.trainerImage)

        self.trainerNameImage = BoxLayout(orientation = "vertical")
        self.trainerNameImage.add_widget(self.trainerName)
        self.trainerNameImage.add_widget(self.trainerImageBox)

        self.trainerInfoBox = BoxLayout(orientation = "vertical")
        self.trainerInfoBox.add_widget(self.trainerType)
        self.trainerInfoBox.add_widget(self.trainerGender)
        self.trainerInfoBox.add_widget(self.trainerDefeatedButton)
    
        self.trainerInfo = BoxLayout(orientation = "horizontal", size_hint_y = 0.4)
        self.trainerInfo.add_widget(self.trainerNameImage)
        self.trainerInfo.add_widget(self.trainerInfoBox)

        self.buttonBox = BoxLayout(orientation = "vertical", size_hint_y = 0.2)
        self.buttonBox.add_widget(self.removeTrainerButton)

        self.layout = BoxLayout(orientation = "vertical")
        self.layout.add_widget(self.trainerInfo)
        self.layout.add_widget(self.buttonBox)

        self.add_widget(self.layout)

        self.fillLayout()
    
    def updateTrainerImage(self) -> Image:
        self.trainerImage.source = getTrainerSprite(self.trainerRecord.IDTrainerType)
    
    def fillLayout(self):
        """fills the layout build by buildlayout with information from the trainerRecord"""
        self.trainerName.text = self.trainerRecord.name
        self.updateTrainerImage()
        if self.trainerRecord.IDGender != None:
            self.trainerGender.text = self.trainerRecord.IDGender
        if self.trainerRecord.IDTrainerType != None:
            self.trainerType.text = self.trainerRecord.IDTrainerType
        self.changeDefeatedButton()

    def setDefeated(self, button):
        logger.info(f"button: {button} pressed to defeat {self.trainerRecord.name}")
        self.trainerRecord.changeDefeated()
    
    def changeDefeatedButton(self):
        if self.trainerRecord.isDefeated:
            self.trainerDefeatedButton.greenColor()
        else:
            self.trainerDefeatedButton.redColor()
    
    def updateTrainerAttribute(self, input, focus, attribute):
        if focus:
            return
        attributeValue = validateTextInput(input.text)
        if attributeValue == None:
            return 
        setattr(self.trainerRecord, attribute, attributeValue)
    
    def updateName(self, input, focus):
        self.updateTrainerAttribute(input, focus, "name")

    def updateType(self, input, focus):
        self.updateTrainerAttribute(input, focus, "IDTrainerType")

    def updateGender(self, input, focus):
        self.updateTrainerAttribute(input, focus, "IDGender")
    
    def deleteTrainerPopup(self) -> None:
        dia = DeleteTrainerPopup(self.trainerRecord)
        dia.open()
        dia.bind(on_dismiss = self.removeTrainer)
    
    def removeTrainer(self, instance):
        if instance.result:
            if self.trainerRecord.removeTrainer():
                return
            return
        logger.debug(f"not removing {self.trainerRecord.name}")
        



        



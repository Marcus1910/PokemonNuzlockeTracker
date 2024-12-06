from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from GUI.transparentButton import TransparentButton
from GUI.Dialog.deleteDialog import DeleteTrainerPopup

from Logic.utilityFunctions import validateTextInput
from Logic.games import getTrainerSprite

from loggerConfig import logger


class EditTrainerBox(BoxLayout): 
    def __init__(self, trainerObject, *args, **kwargs):
        """creates a boxlayout, use buildlayout fill in the layout"""
        super().__init__(*args, **kwargs)
        self.trainerObject = trainerObject
        self.trainerObject.addDefeatedObserver(self.changeDefeatedButton)
        self.trainerObject.addAttributeObserver(self.fillLayout)
        self.trainerObject.addAttributeObserver(self.updateTrainerImage)
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
        self.trainerImage.source = getTrainerSprite(self.trainerObject.trainerType)
    
    def fillLayout(self):
        """fills the layout build by buildlayout with information from the trainerobject"""
        self.trainerName.text = self.trainerObject.name
        self.updateTrainerImage()
        if self.trainerObject.gender != "n/a" and self.trainerObject.gender != None:
            self.trainerGender.text = self.trainerObject.gender
        if self.trainerObject.trainerType != "n/a" and self.trainerObject.trainerType != None:
            self.trainerType.text = self.trainerObject.trainerType
        self.changeDefeatedButton()

    def setDefeated(self, button):
        logger.info(f"button: {button} pressed to defeat {self.trainerObject.name}")
        self.trainerObject.changeDefeated()
    
    def changeDefeatedButton(self):
        if self.trainerObject.defeated:
            self.trainerDefeatedButton.greenColor()
        else:
            self.trainerDefeatedButton.redColor()
    
    def updateTrainerAttribute(self, input, focus, attribute):
        if focus:
            return
        attributeValue = validateTextInput(input.text)
        if attributeValue == None:
            return 
        setattr(self.trainerObject, attribute, attributeValue)
    
    def updateName(self, input, focus):
        self.updateTrainerAttribute(input, focus, "name")

    def updateType(self, input, focus):
        self.updateTrainerAttribute(input, focus, "trainerType")

    def updateGender(self, input, focus):
        self.updateTrainerAttribute(input, focus, "gender")
    
    def deleteTrainerPopup(self) -> None:
        dia = DeleteTrainerPopup(self.trainerObject.name, self.trainerObject.area.name)
        dia.open()
        dia.bind(on_dismiss = self.removeTrainer)
    
    def removeTrainer(self, instance):
        if instance.result:
            if self.trainerObject.removeTrainer():
                return
            return
        logger.debug(f"not removing {self.trainerObject.name}")
        



        



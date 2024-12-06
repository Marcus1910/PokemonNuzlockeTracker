from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch

from kivy.uix.image import Image


from GUI.Dialog.addDialog import AddDialog

from Logic.databaseModels.game import newTrainerString
from Logic.databaseModels.trainer import Trainer
from Logic.games import getTrainerSprite
from Logic.utilityFunctions import validateFields

class AddTrainerDialog(AddDialog):
    def __init__(self, IDLocation: int, updateFunction: callable, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = newTrainerString
        self.updateFunction = updateFunction
        self.IDLocation = IDLocation
        self.content = AddTrainerBox(size_hint_y = None)
        self.content_cls = self.content
        self.dataRetriever = MDApp.get_running_app().dataRetriever

        super().__init__(**kwargs)
    
    def onOK(self, instance) -> None:
        trainerRecord = self.content.makeTrainerRecord(self.IDLocation)
        if trainerRecord != None:
            if self.dataRetriever.insertRecord(trainerRecord):
                self.updateFunction()
                self.dismiss()
            
    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()

class AddTrainerBox(MDBoxLayout): 
    def __init__(self, **kwargs):
        """Provides input field to create Trainer object"""
        super().__init__(**kwargs)
        self.height = "200dp"

        self.dataRetriever = MDApp.get_running_app().dataRetriever
        self.errorLabel = MDLabel(size_hint_y = 0.1, theme_text_color = "Error")
        self.trainerName = MDTextField(hint_text = "Trainer name")
        self.trainerType = MDTextField(hint_text = "Trainer type")
        self.trainerType.bind(focus = self.updateImage)
        self.trainerGender = MDTextField(hint_text = "Gender: M/F")
        self.optionalTrainerLabel = MDLabel(text = "Optional Trainer", pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.optionalCheck = MDSwitch(pos_hint = {'center_x': 0.5, 'center_y': 0.5}, width = "64dp")

        self.trainerImage = Image(fit_mode = "contain")

        self.bossBox = MDBoxLayout(orientation = "horizontal", padding = [0, 20, 0, 0])
        self.bossBox.add_widget(self.optionalTrainerLabel)
        self.bossBox.add_widget(self.optionalCheck)

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
        return validateFields([self.trainerName, self.trainerType, self.trainerGender])
    
    def makeTrainerRecord(self, IDLocation: int) -> Trainer | None:
        """validates textfield input, returns 0 if something is wrong, else the trainerObject"""
        trainerRecord = None
        if not self.validateTextFields():
            return 0
        trainerRecord = Trainer(IDLocation, self.trainerType.text, self.trainerName.text, self.trainerGender.text, isOptional = self.optionalCheck.active)
        return trainerRecord
    
    def showError(self, error: str) -> None:
        self.errorLabel.text = error
    
    def resetFields(self):
        self.trainerName.text = ""
        self.trainerImage.source = ""
        self.trainerGender.text = ""
        self.trainerType.text = ""
        self.optionalCheck.active = False
        self.errorLabel.text = ""

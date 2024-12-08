from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch

from kivy.uix.image import Image


from GUI.Dialog.addDialog import AddDialog

from Logic.databaseModels.game import newTrainerString, editTrainerString
from Logic.databaseModels.trainer import Trainer
from Logic.games import getTrainerSprite
from Logic.utilityFunctions import validateFields
from loggerConfig import logger

class AddTrainerDialog(AddDialog):
    def __init__(self, updateFunction: callable, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = newTrainerString
        self.updateFunction = updateFunction
        self.content = AddEditTrainerBox(size_hint_y = None)
        self.content_cls = self.content
        self.manager = MDApp.get_running_app().windowManager

        super().__init__(**kwargs)
        self.okButton.text = "Add"
    
    def onOK(self, instance) -> None:
        trainerRecord = self.content.makeTrainerRecord(self.manager.locationRecord.IDLocation)
        if trainerRecord != None:
            if self.manager.insertRecord(trainerRecord):
                self.updateFunction()
                self.dismiss()
            
    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()
    
class EditTrainerDialog(AddDialog):
    def __init__(self, trainerRecord: Trainer, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = editTrainerString
        self.trainerRecord = trainerRecord
        self.content = AddEditTrainerBox(trainerRecord = self.trainerRecord, size_hint_y = None)
        self.content_cls = self.content
        self.manager = MDApp.get_running_app().windowManager

        super().__init__(**kwargs)
        self.okButton.text = "Update"
    
    def onOK(self, instance) -> None:
        if self.content.updateTrainerRecord():
            logger.debug("update validated")
            if self.manager.updateRecord(self.trainerRecord):
                # self.updateFunction()
                self.dismiss()
            
    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()
    

class AddEditTrainerBox(MDBoxLayout): 
    def __init__(self, trainerRecord = None, **kwargs):
        """Provides input field to create Trainer object"""
        super().__init__(**kwargs)
        self.height = "200dp"
        self.trainerRecord = trainerRecord
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
        
        self.fillLayout()
        
        self.add_widget(self.errorLabel)
        self.add_widget(self.trainerBox)

    def clearLayout(self):
        self.clear_widgets()
        
    def fillLayout(self):
        if self.trainerRecord == None:
            return
        
        self.trainerName.text = self.trainerRecord.name
        self.trainerGender.text = self.trainerRecord.IDGender
        self.optionalCheck.active = self.trainerRecord.isOptional
        self.trainerType.text = self.trainerRecord.IDTrainerType
    
    def updateImage(self, input, focus):
        """updates trainer image to last trainertype update"""
        if focus:
            return
        self.trainerImage.source = getTrainerSprite(input.text)
    
    def validateTextFields(self):
        return validateFields([self.trainerName, self.trainerType, self.trainerGender])
    
    def resetFields(self):
        self.trainerName.text = ""
        self.trainerImage.source = ""
        self.trainerGender.text = ""
        self.trainerType.text = ""
        self.optionalCheck.active = False
        self.errorLabel.text = ""
    
    def makeTrainerRecord(self, IDLocation: int) -> Trainer | None:
        """validates textfield input, returns 0 if something is wrong, else the trainerObject"""
        trainerRecord = None
        if not self.validateTextFields():
            return 0
        trainerRecord = Trainer(IDLocation, self.trainerType.text, self.trainerName.text, self.trainerGender.text, isOptional = self.optionalCheck.active)
        return trainerRecord
    
    def updateTrainerRecord(self) -> bool:
        return self.validateTextFields()
        


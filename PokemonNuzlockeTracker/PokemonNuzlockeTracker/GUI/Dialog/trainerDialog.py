from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch

from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

from GUI.Dialog.addDialog import AddDialog, EditDialog
from GUI.nuzlockeSpinner import NuzlockeSpinner, NuzlockeLookupSpinner
from GUI.eventBus import eventBus

from Logic.databaseModels.game import newTrainerString, editTrainerString
from Logic.databaseModels.trainer import Trainer
from Logic.games import getTrainerSprite
from Logic.databaseModels.game import NLS
from Logic.utilityFunctions import validateFields
from loggerConfig import logger

class AddTrainerDialog(AddDialog):
    def __init__(self, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = newTrainerString
        self.content = AddEditTrainerBox(size_hint_y = None)
        self.content_cls = self.content
        self.manager = MDApp.get_running_app().windowManager
        super().__init__(**kwargs)
    
    def onOK(self, instance) -> None:
        trainerRecord = self.content.makeTrainerRecord(self.manager.locationRecord.IDLocation)
        if trainerRecord != None:
            if self.manager.insertRecord(trainerRecord):
                eventBus.updateTrainerEvent()
                self.dismiss()
            
    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()
    
class EditTrainerDialog(EditDialog):
    def __init__(self, trainerRecord: Trainer, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = editTrainerString
        self.trainerRecord = trainerRecord
        self.content = AddEditTrainerBox(trainerRecord = self.trainerRecord, size_hint_y = None)
        self.content_cls = self.content
        self.manager = MDApp.get_running_app().windowManager
        super().__init__(**kwargs)
    
    def onOK(self, instance) -> None:
        if self.content.updateTrainerRecord():
            logger.debug("trainer update succeeded")
            eventBus.updateTrainerEvent()
            self.dismiss()
    
    def onDelete(self, instance):
        if self.content.deleteTrainerRecord():
            logger.debug("trainer deletion succeeded")
            eventBus.updateTrainerEvent()
            self.dismiss()
            
    def dismiss(self, *args) -> None:
        self.content.resetFields()
        super().dismiss()
    

class AddEditTrainerBox(MDBoxLayout): 
    def __init__(self, trainerRecord = None, **kwargs):
        """Provides input field to create Trainer object"""
        super().__init__(**kwargs)
        self.height = "200dp"
        self.manager = MDApp.get_running_app().windowManager
        self.trainerRecord = trainerRecord
        self.trainerRemoved = False
        self.errorLabel = MDLabel(size_hint_y = 0.1, theme_text_color = "Error")
        self.trainerType = NuzlockeLookupSpinner(NLS.TRAINERTYPE, hint_text = "trainer type", halign = "left")
        self.trainerName = TextInput(hint_text = "Trainer name")

        self.trainerGender = NuzlockeLookupSpinner(NLS.GENDER, hint_text = "Gender", halign = "left")
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
        if self.trainerRecord != None:
            self.fillLayout()
        
        self.add_widget(self.errorLabel)
        self.add_widget(self.trainerBox)

    def clearLayout(self):
        self.clear_widgets()
        
    def fillLayout(self):
        if self.trainerRecord == None:
            return
        self.trainerImage.source = getTrainerSprite(self.trainerRecord.IDTrainerType)
        self.trainerName.text = self.trainerRecord.name
        self.trainerGender.lookupID = self.trainerRecord.IDGender
        self.trainerType.lookupID = self.trainerRecord.IDTrainerType
        self.optionalCheck.active = self.trainerRecord.isOptional
        
    
    def updateImage(self, input, focus):
        """updates trainer image to last trainertype update"""
        if focus:
           return
        self.trainerImage.source = getTrainerSprite(self.trainerType.text)
    
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
        trainerRecord = Trainer(IDLocation, self.trainerType.lookupID, self.trainerName.text, self.trainerGender.lookupID, isOptional = self.optionalCheck.active)
        return trainerRecord
    
    def updateTrainerRecord(self) -> bool:
        if self.validateTextFields():
            self.trainerRecord.name = self.trainerName.text
            self.trainerRecord.idTrainerType = self.trainerType.lookupID
            self.trainerRecord.idGender = self.trainerGender.lookupID
            self.trainerRecord.isOptional = self.optionalCheck.active
            return self.manager.updateRecord(self.trainerRecord)
        return False
    
    def deleteTrainerRecord(self) -> bool:
        if self.manager.deleteRecord(self.trainerRecord):
            self.trainerRemoved = True
        return True
            
        
        


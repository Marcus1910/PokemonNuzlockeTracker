from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch

from utilityFunctions import checkString, validateTextInput
from loggerConfig import logger
from trainer import Trainer

class AddTrainerBox(MDBoxLayout): 
    def __init__(self, *args, **kwargs):
        """creates a boxlayout, use buildlayout fill in the layout"""
        super().__init__(*args, **kwargs)
        self.height = "200dp"

        self.errorLabel = MDLabel(size_hint_y = 0.1, theme_text_color = "Error")
        self.trainerName = MDTextField(hint_text = "Name")
        self.trainerType = MDTextField(hint_text = "Trainer Type")
        self.trainerGender = MDTextField(hint_text = "Gender: M/F")
        self.bossTrainerLabel = MDLabel(text = "Boss Trainer", pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.bossCheck = MDSwitch(pos_hint = {'center_x': 0.5, 'center_y': 0.5}, width = "64dp")
        #TODO
        self.trainerImage = MDBoxLayout()

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
        self.trainerGender.text = ""
        self.trainerType.text = ""
        self.bossCheck.active = False
        self.errorLabel.text = ""
    
class AddTrainerDialog(MDDialog):
    def __init__(self, addTrainerFunction, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.auto_dismiss = False
        self.title = "Add new Trainer"
        self.type = "custom"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        self.content = AddTrainerBox(size_hint_y = None)
        self.addTrainerFunction = addTrainerFunction

        self.content_cls = self.content
        #makeTrainerObject function also handles the errors
        self.buttons = [MDFlatButton(text = "apply", on_release = self.createTrainer), MDFlatButton(text = "discard", on_release = self.dismiss)]

        super().__init__(**kwargs)
    
    def createTrainer(self, instance):
        trainerObject = self.content.makeTrainerObject()
        if trainerObject != 0:
            #input is correct, create new Object for Area
            if self.addTrainerFunction(trainerObject):
                self.dismiss()

    def dismiss(self, *args):
        self.content.resetFields()
        super().dismiss()


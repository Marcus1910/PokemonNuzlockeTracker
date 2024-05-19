from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from utilityFunctions import checkString, validateTextInput
from loggerConfig import logger
from trainer import Trainer

class AddTrainerBox(MDBoxLayout): 
    def __init__(self, *args, **kwargs):
        """creates a boxlayout, use buildlayout fill in the layout"""
        super().__init__(*args, **kwargs)
        self.height = "200dp"
        self.buildLayout()


    def buildLayout(self):
        """if trainerObject is Not supplied displays empty box meant to add a trainer if trainerObject is supplied fills in details about the trainer so it can be edited""" 

        self.trainerName = MDTextField(hint_text = "Name")
        self.trainerType = MDTextField(hint_text = "Trainer Type")
        self.trainerGender = MDTextField(hint_text = "Gender: M/F")
        #TODO
        self.trainerImage = MDBoxLayout()

        self.trainerInfoBox = MDBoxLayout(orientation = "vertical")
        self.trainerInfoBox.add_widget(self.trainerName)
        self.trainerInfoBox.add_widget(self.trainerType)
        self.trainerInfoBox.add_widget(self.trainerGender)

        self.trainerBox = MDBoxLayout(orientation = "horizontal")
        self.trainerBox.add_widget(self.trainerInfoBox)
        self.trainerBox.add_widget(self.trainerImage)

        self.orientation = "vertical"
        self.add_widget(self.trainerBox)

    def clearLayout(self):
        self.clear_widgets()
    
    def saveTrainerObject(self, *args):
        """function that calls the correct functions from the trainerscreen to edit or add a new trainer to the area object"""
        #check whether the name has been supplied, if empty can't do anything
        name = self.trainerName.text
        #causes multiple instances of New Trainer object to apear which can't be accessed
        if name == "New Trainer":
            logger.info("You sneaky, sneaky bastard")
            return
        
        if checkString(name):
            logger.error(f"No name has been supplied for the new trainer, please enter name")
            return
        #check if there is a trainerobject that needs to be modified or if a new object must be created
        self.trainerObject = Trainer(name = name)

        #decorate object
        self.trainerObject.gender = validateTextInput(self.trainerGender.text)
        self.trainerObject.trainerType = validateTextInput(self.trainerType.text)
        #add trainer to the game
        # self.trainerScreen.addTrainerToGame(self.trainerObject)
    
class TrainerDialog(MDDialog):
    def __init__(self, **kwargs):
        """Dialog to add trainer. Only use kivymd widgets inside"""
        self.title = "Add new Trainer"
        self.type = "custom"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        content = MDBoxLayout(orientation = "vertical", height = "120dp", size_hint_y = None)
        self.trainerName = MDTextField(hint_text = "Trainer name *")
        self.trainertype = MDTextField(hint_text = "Trainer type")
        self.trainergender = MDTextField(hint_text = "Trainer gender (m/f)")

        content.add_widget(self.trainerName)
        typegender = MDBoxLayout(orientation = "horizontal")
        typegender.add_widget(self.trainertype)
        typegender.add_widget(self.trainergender)

        content.add_widget(typegender)
        self.content_cls = AddTrainerBox(size_hint_y = None)

        self.buttons = [MDFlatButton(text = "apply", on_release = self.checkout), MDFlatButton(text = "discard")]

        super().__init__(**kwargs)

    def checkout(self, instance):
        print("hihihih")
        



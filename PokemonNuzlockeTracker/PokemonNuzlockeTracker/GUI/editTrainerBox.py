from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from loggerConfig import logger
from trainer import Trainer

class EditTrainerBox(BoxLayout): 
    def __init__(self, trainerScreen, *args, **kwargs):
        """creates a boxlayout, use buildlayout fill in the layout"""
        super().__init__(*args, **kwargs)
        self.trainerScreen = trainerScreen
        self.trainerObject = None

    def buildLayout(self, trainerObject = None):
        """if trainerObject is Not supplied displays empty box meant to add a trainer if trainerObject is supplied fills in details about the trainer so it can be edited"""
        self.trainerObject = trainerObject
        self.trainerDefeated = 0 
        self.trainerName = TextInput(hint_text = "Name")
        self.trainerType = TextInput(hint_text = "Trainer Type")
        self.trainerGender = TextInput(hint_text = "Gender: M/F")
        self.trainerDefeatedButton = Button(text = "defeated", on_press = self.setDefeated)
        #TODO
        self.trainerImage = None

        self.confirmButton = Button(text = "confirm", on_press = self.saveTrainerObject)

        self.trainerInfoBox = BoxLayout(orientation = "vertical")
        self.trainerInfoBox.add_widget(self.trainerName)
        self.trainerInfoBox.add_widget(self.trainerType)
        self.trainerInfoBox.add_widget(self.trainerGender)
        self.trainerInfoBox.add_widget(self.trainerDefeatedButton)
        self.trainerInfoBox.add_widget(self.confirmButton)

        self.add_widget(self.trainerInfoBox)

        if self.trainerObject != None:
            self.fillLayout()
    
    def fillLayout(self):
        """fills the layout build by buildlayout with information from the trainerobject"""
        self.trainerDefeated = self.trainerObject.defeated
        self.trainerName.text = self.trainerObject.name
        if self.trainerObject.gender != "n/a" and self.trainerObject.gender != None:
            self.trainerGender.text = self.trainerObject.gender
        if self.trainerObject.trainerType != "n/a" and self.trainerObject.trainerType != None:
            self.trainerType.text = self.trainerObject.trainerType

    def clearLayout(self):
        self.trainerObject = None
        self.clear_widgets()
    
    def saveTrainerObject(self, *args):
        """function that calls the correct functions from the trainerscreen to edit or add a new trainer to the area object"""
        #check whether the name has been supplied, if empty can't do anything
        name = self.trainerName.text
        #used to store newName, default None for function area.editTrainer
        newName = None
        addNewEntry = False
        if self.checkString(name):
            logger.error(f"No name has been supplied for the new trainer, please enter name")
            return
        #check if there is a trainerobject that needs to be modified or if a new object must be created
        if self.trainerObject == None:
            #create new trainerObject from name
            self.trainerObject = Trainer(name = name)
            addNewEntry = True
            
        #check if name needs to be adjusted
        if self.trainerObject.name != self.trainerName.text:
            newName = self.trainerName.text

        #decorate object
        self.trainerObject.gender = self.validateTextInput(self.trainerGender)
        self.trainerObject.trainerType = self.validateTextInput(self.trainerType)
        self.trainerObject.defeated = self.trainerDefeated

        #call correct functions
        if addNewEntry:
            self.trainerScreen.addTrainerToGame(self.trainerObject)
        else:
            self.trainerScreen.editTrainerObject(self.trainerObject, newName)
          
    def setDefeated(self, button):
        logger.info(f"button: {button} pressed to defeta trainer")
    
    def checkString(self, text):
        """function that returns True when the given text consists of only whitespace or is empty"""
        return text.isspace() or text == ""

    def validateTextInput(self, textInput):
        """function that returns None or the supplied TextInput si the input is not empty"""
        return textInput.text if self.checkString(textInput.text) else None
        



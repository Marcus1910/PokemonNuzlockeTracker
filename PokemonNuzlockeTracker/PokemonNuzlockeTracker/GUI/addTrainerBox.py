from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from utilityFunctions import checkString, validateTextInput
from loggerConfig import logger
from trainer import Trainer

class AddTrainerBox(BoxLayout): 
    def __init__(self, trainerScreen, *args, **kwargs):
        """creates a boxlayout, use buildlayout fill in the layout"""
        super().__init__(*args, **kwargs)
        self.trainerScreen = trainerScreen

    def buildLayout(self):
        """if trainerObject is Not supplied displays empty box meant to add a trainer if trainerObject is supplied fills in details about the trainer so it can be edited""" 
        self.trainerName = TextInput(hint_text = "Name", size_hint_y = 0.3)
        self.trainerType = TextInput(hint_text = "Trainer Type", size_hint_y = 0.2)
        self.trainerGender = TextInput(hint_text = "Gender: M/F", size_hint_y = 0.2)
        #TODO
        self.trainerImage = BoxLayout(size_hint_y = 0.8)
        self.confirmButton = Button(text = "confirm", on_press = self.saveTrainerObject, background_color = (0, 1, 0, 0.5))

        self.trainerNameImage = BoxLayout(orientation = "vertical")
        self.trainerNameImage.add_widget(self.trainerName)
        self.trainerNameImage.add_widget(self.trainerImage)

        self.trainerInfoBox = BoxLayout(orientation = "vertical")
        self.trainerInfoBox.add_widget(self.trainerType)
        self.trainerInfoBox.add_widget(self.trainerGender)
    
        self.trainerInfo = BoxLayout(orientation = "horizontal", size_hint_y = 0.4)
        self.trainerInfo.add_widget(self.trainerNameImage)
        self.trainerInfo.add_widget(self.trainerInfoBox)

        self.pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.4)

        self.confirmButtonBox = BoxLayout(orientation = "horizontal")
        self.confirmButtonBox.add_widget(self.confirmButton)

        self.buttonBox = BoxLayout(orientation = "vertical", size_hint_y = 0.2)
        self.buttonBox.add_widget(self.confirmButtonBox)

        self.layout = BoxLayout(orientation = "vertical")
        self.layout.add_widget(self.trainerInfo)
        self.layout.add_widget(self.pokemonBox)
        self.layout.add_widget(self.buttonBox)

        self.add_widget(self.layout)

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
        self.trainerScreen.addTrainerToGame(self.trainerObject)

        



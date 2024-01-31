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
        self.trainerDefeated = False 
        self.trainerName = TextInput(hint_text = "Name", size_hint_y = 0.3)
        self.trainerType = TextInput(hint_text = "Trainer Type", size_hint_y = 0.2)
        self.trainerGender = TextInput(hint_text = "Gender: M/F", size_hint_y = 0.2)
        self.trainerDefeatedButton = Button(text = "defeated", on_press = self.setDefeated, background_color = (1, 0, 0, 0.5), size_hint_y = 0.6)
        self.removeTrainerButton = Button(text = "remove trainer", on_press = self.deleteTrainerFromGame, background_color = (1, 0, 0, 0.5))
        #TODO
        self.trainerImage = BoxLayout(size_hint_y = 0.8)

        self.confirmButton = Button(text = "confirm", on_press = self.saveTrainerObject, background_color = (0, 1, 0, 0.5), size_hint_x = 0.7)
        self.cancelButton = Button(text = "cancel", on_press = self.cancel, background_color = (0.4, 0, 0, 0.5), size_hint_x = 0.3)

        self.trainerNameImage = BoxLayout(orientation = "vertical")
        self.trainerNameImage.add_widget(self.trainerName)
        self.trainerNameImage.add_widget(self.trainerImage)

        self.trainerInfoBox = BoxLayout(orientation = "vertical")
        self.trainerInfoBox.add_widget(self.trainerType)
        self.trainerInfoBox.add_widget(self.trainerGender)
        self.trainerInfoBox.add_widget(self.trainerDefeatedButton)
    
        self.trainerInfo = BoxLayout(orientation = "horizontal", size_hint_y = 0.4)
        self.trainerInfo.add_widget(self.trainerNameImage)
        self.trainerInfo.add_widget(self.trainerInfoBox)

        self.pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.4)

        self.confirmButtonBox = BoxLayout(orientation = "horizontal")
        self.confirmButtonBox.add_widget(self.confirmButton)
        self.confirmButtonBox.add_widget(self.cancelButton)

        self.buttonBox = BoxLayout(orientation = "vertical", size_hint_y = 0.2)
        self.buttonBox.add_widget(self.removeTrainerButton)
        self.buttonBox.add_widget(self.confirmButtonBox)

        self.layout = BoxLayout(orientation = "vertical")
        self.layout.add_widget(self.trainerInfo)
        self.layout.add_widget(self.pokemonBox)
        self.layout.add_widget(self.buttonBox)

        self.add_widget(self.layout)

        self.fillLayout()
    
    def fillLayout(self):
        """fills the layout build by buildlayout with information from the trainerobject"""
        self.trainerDefeated = self.trainerObject.defeated
        self.trainerName.text = self.trainerObject.name
        if self.trainerObject.gender != "n/a" and self.trainerObject.gender != None:
            self.trainerGender.text = self.trainerObject.gender
        if self.trainerObject.trainerType != "n/a" and self.trainerObject.trainerType != None:
            self.trainerType.text = self.trainerObject.trainerType
        self.changeDefeatedButton()

    def clearLayout(self):
        self.trainerObject = None
        self.clear_widgets()

    def cancel(self, *args):
        self.trainerScreen.cancelEditTrainer()

    def setDefeated(self, button):
        logger.info(f"button: {button} pressed to defeta trainer")
        #inverse, 0 -> 1, 1-> 0
        self.trainerDefeated = not self.trainerDefeated
        self.changeDefeatedButton()
    
    def changeDefeatedButton(self):
        if self.trainerDefeated:
            self.trainerDefeatedButton.background_color = ((0, 1, 0, 0.5))
        else:
            self.trainerDefeatedButton.background_color = ((1, 0, 0, 0.5))
    
    def saveTrainerObject(self, *args):
        """function that calls the correct functions from the trainerscreen to edit or add a new trainer to the area object"""
        #check whether the name has been supplied, if empty can't do anything
        name = self.trainerName.text
        #causes multiple instances of New Trainer object to apear which can't be accessed
        if name == "New Trainer":
            logger.info("You sneaky, sneaky bastard")
            return
        #used to store newName, default None for function area.editTrainer
        newName = None
        if self.checkString(name):
            logger.error(f"No name has been supplied for the new trainer, please enter name")
            return
            
        #check if name needs to be adjusted
        if self.trainerObject.name != self.trainerName.text:
            newName = self.trainerName.text

        #decorate object
        self.trainerObject.gender = self.validateTextInput(self.trainerGender)
        self.trainerObject.trainerType = self.validateTextInput(self.trainerType)
        self.trainerObject.defeated = self.trainerDefeated

        #call correct functions
        self.trainerScreen.editTrainerObject(self.trainerObject, newName)
        
    def deleteTrainerFromGame(self, *args):
        logger.debug(f"removing {self.trainerObject.name}")
        self.trainerScreen.removeTrainer(self.trainerObject.name)

    def checkString(self, text):
        """function that returns True when the given text consists of only whitespace or is empty"""
        return text.isspace() or text == ""

    def validateTextInput(self, textInput):
        """function that returns None or the supplied TextInput is the input is not empty"""
        return textInput.text if not self.checkString(textInput.text) else None
        



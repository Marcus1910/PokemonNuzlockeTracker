from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel

from loggerConfig import logger

from GUI.Dialog.addDialog import AddDialog

from Logic.databaseModels.game import Game, newGameString
from Logic.utilityFunctions import validateFields, validateField
from Logic.games import red

class NewGameDialog(AddDialog):
    def __init__(self, screen, **kwargs):
        self.title = newGameString
        self.screen = screen
        self.content = NewGameBox(size_hint_y = None)
        self.content_cls = self.content
        super().__init__(**kwargs)
        
        self.okButton.text = "Add Game"
        self.cancelButton.text = "Close"
        
    def onOK(self, instance):
        if self.content.validateInputFields(): 
            self.createNewGame()
    
    def createNewGame(self) -> None:
        gameName = self.content.getNameInput()
        if self.screen.createNewGame(gameName):
            self.dismiss()
    
    def dismiss(self, *args):
        self.content.resetFields()
        super().dismiss()

class NewGameBox(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.height = "250dp"
        self.newGameLabel = MDTextField(hint_text = "New Game Name")
        self.newGameGeneration = MDTextField(hint_text = "Gen", input_filter = "int")
        self.encountersPerLocation = MDTextField(hint_text = "Encounters per location")
        self.hasPhysicalSpecialSplit = MDSwitch(pos_hint = {'center_x': .5, 'center_y': .4}, width = "128dp")
        self.switchBox = MDBoxLayout(MDLabel(text = "uses physical special split"), self.hasPhysicalSpecialSplit, orientation = "horizontal")
        
        #self.IDParentGame = 
        self.add_widget(self.newGameLabel)
        self.add_widget(self.newGameGeneration)
        self.add_widget(self.encountersPerLocation)
        self.add_widget(self.switchBox)
        
    def getNameInput(self) -> str:
        return self.newGameLabel.text

    def getNewGameGenerationInput(self) -> str:
        return self.newGameGeneration.text
    
    def gameExists(self, instance):
        instance.helperText = ""
        if not validateField(instance):
            instance.error = True
            return          
    
    def resetFields(self) -> None:
        self.newGameLabel.text = ''
        self.newGameGeneration.text = ''
    
    def validateInputFields(self) -> bool:
        if not validateFields([self.newGameLabel, self.newGameGeneration]):
           logger.error("One or more mandatory fields are empty")
           return False 
        return True

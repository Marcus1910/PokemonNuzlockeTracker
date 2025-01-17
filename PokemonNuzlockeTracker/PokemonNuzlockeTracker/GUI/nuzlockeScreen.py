from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from GUI.nuzlockeSpinner import NuzlockeSpinner
from GUI.transparentButton import TransparentButton
from GUI.backgroundScreen import BackgroundScreen
from GUI.Dialog.newAreaBox import NewAreaBox
from loggerConfig import logger
from Logic.databaseModels.game import newLocationString, chooseLocationString, standardColor, opaque, NLS

class NuzlockeScreen(BackgroundScreen):
    """Parent screen, adds the name of the screen at the top, add own widgets into screenBox which is a boxLayout.
    Rebind updateValueschanged or/and valuesChangeFunction if there are other requirements needed on the update/value changed event, don't forget to call super()"""
    
    def __init__(self, screenName, **kwargs):
        super().__init__(**kwargs)
        
        self.currentPokemon = ""
        self.spinnerValues = []
        self.standardColor = standardColor
        self.entered = False
        self.screenName = screenName
        
        self.layout = BoxLayout(orientation= "vertical")
        self.screenInfoBox = BoxLayout(orientation = "vertical", size_hint_y = 0.04)
        screenLabel = Label(text = self.screenName, color = self.standardColor)
        self.screenInfoBox.add_widget(screenLabel)

        self.screenBox = BoxLayout(orientation = "vertical", size_hint_y = 0.88)

        self.areaSpinnerBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.08)
        self.spinner = NuzlockeSpinner(NLS.LOCATION, self.spinnerValueChanged, multiline = False, size_hint_x = 0.85, background_color = opaque, halign = "center")

        self.editAreaButton = TransparentButton(text = "edit area", size_hint_x = 0.15, on_release = self.editArea)
        self.editAreaButton.disabled = True

        self.areaSpinnerBox.add_widget(self.spinner)
        
        if not self.screenName == "Pokemon Info Screen":
            self.areaSpinnerBox.add_widget(self.editAreaButton)

        self.layout.add_widget(self.screenInfoBox)
        self.layout.add_widget(self.areaSpinnerBox)
        self.layout.add_widget(self.screenBox)

        self.add_widget(self.layout)

    def editArea(self, button):
        logger.debug("editing Area, TODO")
    
    def addArea(self, name, badge):
        # if self.manager.gameObject.addArea(name, badge):
        #     #change spinner text to new Area, area object follows due to areaChanged
        #     self.areaSpinner.text = name
        #     #reload area spinner
        #     self.updateAreaSpinner()
        #     return 1
        return 0
    
    def setDefaultArea(self):
        """set area to default if current Area is None"""
        if self.screenName == "Pokemon Info Screen":
            return 0
        if self.manager.locationRecord == None:
            self.spinner.hint_text = chooseLocationString
            return 0 
        self.spinner.text = self.manager.locationRecord.name
        logger.debug("Location is valid, changing spinner text to correct text") 
        return 1  
    
    def updateSpinnerValues(self):
        """updates the values that the spinner uses, used to determine whihc type the lookup spinner needs"""
        if self.screenName == "Pokemon Info Screen":
            self.spinner.nlsType = NLS.POKEMON
        else:
            self.spinner.nlsType = NLS.LOCATION
        self.spinner.updateSpinnerValues()
    
    def on_pre_enter(self):
        """set correct values into the spinner"""
        #compare location name because the ID has raise valueError if None
        if (self.manager.locationRecord == None) or (self.manager.locationRecord.name != self.spinner.text):
            self.updateSpinnerValues()
        return self.setDefaultArea()

    def spinnerValueChanged(self, text: str) -> bool:
        """text is the LocationName, returns 1 if valid Location"""
        self.editAreaButton.disabled = True
        newValue = text
        print(newValue)
        if newValue == chooseLocationString:
            logger.debug("default string for Area, or area invalid not doing anything")
            return 0
        
        if newValue == newLocationString:
            logger.debug("creating popup to add new Location")
            self.editAreaButton.disabled = True
            newAreaBox = NewAreaBox(orientation = "vertical", confirmCallback = self.addArea)
            areaPopup = Popup(title = "add Area", content = newAreaBox)
            newAreaBox.dismiss = areaPopup.dismiss
            
            #newAreaBox.confirmButton.on_release(self.addArea)
            newAreaBox.cancelButton.on_release = lambda : [areaPopup.dismiss(), self.setDefaultArea()]
            
            areaPopup.open()
            return 0
        
        if self.screenName == "Pokemon Info Screen":
           self.currentPokemon = newValue 
        else:
            self.manager.locationRecord = newValue
            self.editAreaButton.disabled = False
            logger.info(f"currentArea changed to {newValue}") 
        
        return 1
        
    def on_enter(self):
        """call function to add next and previous buttons to the bottom of the screen"""
        #return if the function is already called, else create buttons. otherwise creates multiple buttons on each exit
        if self.entered:
            return
        #create buttons to navigate through the screens and add to layout
        exitGameButton = TransparentButton(text = "Exit and save Game", on_press = lambda btn:  self.saveGame(), size_hint_y = 0.08)

        self.layout.add_widget(exitGameButton)
        self.entered = True

    def cleanScreenBox(self):
        self.screenBox.clear_widgets()
    
    def nextScreen(self):
        """go to the next screen"""
        self.manager.screenNumber += 1
        self.manager.transition.direction = "left"

    def previousScreen(self):
        """go to previous screen"""
        self.manager.screenNumber -= 1
        self.manager.transition.direction = "right"
    
    def saveGame(self):
        self.manager.closePokemonGame()

    def on_touch_move(self, touch):
        if abs(touch.oy - touch.y) > 120:
            #could be swiping up or down
            return 
        if 0 < touch.ox - touch.x > 150:
            self.nextScreen()
            
        if 0 > touch.ox - touch.x < -150:
            self.previousScreen()
            




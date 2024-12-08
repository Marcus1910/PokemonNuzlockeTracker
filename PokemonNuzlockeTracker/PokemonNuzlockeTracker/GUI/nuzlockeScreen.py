from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from kivymd.uix.swiper import MDSwiper

from GUI.transparentButton import TransparentButton
from GUI.backgroundScreen import BackgroundScreen
from GUI.Dialog.newAreaBox import NewAreaBox
from loggerConfig import logger
from Logic.databaseModels.game import newLocationString, chooseLocationString, standardColor, opaque

class NuzlockeScreen(BackgroundScreen):
    """Parent screen, adds the name of the screen at the top, add own widgets into screenBox which is a boxLayout."""
    
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
        self.spinnerTextInput = TextInput(multiline = False, size_hint_x = 0.85, background_color = opaque)
        self.spinnerTextInput.bind(focus = self.spinnerTextFocus)
        self.spinnerTextInput.bind(text = self.onTextEntered)
        
        self.spinnerDropDown = DropDown()

        self.editAreaButton = TransparentButton(text = "edit area", size_hint_x = 0.15, on_release = self.editArea)
        self.editAreaButton.disabled = True

        self.areaSpinnerBox.add_widget(self.spinnerTextInput)
        
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
        """set area to default is current Area is None"""
        if self.screenName == "Pokemon Info Screen":
            return
        if self.manager.locationRecord == None:
            self.spinnerTextInput.hint_text = chooseLocationString
            return
        self.spinnerTextInput.hint_text = self.manager.locationRecord.name
        logger.debug("popup skipped and area is valid, changing spinner text to correct text")
    
    def spinnerTextFocus(self, instance, focused):
        if focused:
            self.spinnerDropDown.open(self.spinnerTextInput)
    
    def populateDropDown(self):
        print(f"populating dropdown")
        self.spinnerDropDown.clear_widgets()
        print(len(self.spinnerValues))
        for spinnerValue in self.spinnerValues:
            btn = TransparentButton(text = spinnerValue, size_hint_y = None, height = 20, on_release = self.spinnerValueChanged)
            self.spinnerDropDown.add_widget(btn)
                
    def onTextEntered(self, instance, text):
        self.updateSpinnerValues(text)    
    
    def updateSpinnerValues(self, text = ""):
        """updates the values that the spinner uses"""
        print(f"updating spinner: {text}")
        if self.screenName == "Pokemon Info Screen":
            self.spinnerValues = self.manager.getPokemonNames(text)
        else:
            print("updating locations")
            self.spinnerValues = self.manager.getLocationNames(text)
        self.populateDropDown()
    
    def on_pre_enter(self) -> bool:
        """adjusts Spinner text to area currently selected for regular screens, returns 0 if area == None"""
        self.updateSpinnerValues()
        self.setDefaultArea()

    def spinnerValueChanged(self, button) -> bool:
        """text is the areaName"""
        newValue = button.text
        #gets set to default when popup is canceled, otherwise crashes if the areaObject is None
        if newValue == chooseLocationString:
            logger.debug("default string for Area, or area invalid not doing anything")
            return 0
        
        if newValue == newLocationString:
            logger.debug("creating popup to add new Area")
            self.editAreaButton.disabled = True
            newAreaBox = NewAreaBox(orientation = "vertical", confirmCallback = self.addArea)
            areaPopup = Popup(title = "add Area", content = newAreaBox)
            newAreaBox.dismiss = areaPopup.dismiss
            
            #newAreaBox.confirmButton.on_release(self.addArea)
            newAreaBox.cancelButton.on_release = lambda : [areaPopup.dismiss(), self.setDefaultArea()]
            
            areaPopup.open()
            return 0
        if not self.screenName == "Pokemon Info Screen":
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
            



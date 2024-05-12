from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup


from transparentButton import TransparentButton
from backgroundScreen import BackgroundScreen
from newAreaBox import NewAreaBox
from loggerConfig import logger
import games as gm

class NuzlockeScreen(BackgroundScreen):
    """Parent screen, adds the name of the screen at the top, add own widgets into screenBox which is a boxLayout."""
    
    def __init__(self, screenName, **kwargs):
        super().__init__(**kwargs)
        self.areaSpinnerString = "choose an area"
        self.standardColor = gm.standardColor
        self.entered = False

        self.layout = BoxLayout(orientation= "vertical")
        self.screenInfoBox = BoxLayout(orientation = "vertical", size_hint_y = 0.04)
        screenLabel = Label(text = screenName, color = self.standardColor)
        self.screenInfoBox.add_widget(screenLabel)

        self.screenBox = BoxLayout(orientation = "vertical", size_hint_y = 0.8)

        self.areaSpinnerBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.04)
        self.areaSpinner = Spinner(text = self.areaSpinnerString, values = ["new Area"], size_hint_x = 0.85)
        self.areaSpinner.background_color = gm.opaque
        self.areaSpinner.bind(text = self.areaChanged)

        self.editAreaButton = TransparentButton(text = "edit area", size_hint_x = 0.15, on_release = self.editArea)
        self.editAreaButton.disabled = True

        self.areaSpinnerBox.add_widget(self.areaSpinner)
        self.areaSpinnerBox.add_widget(self.editAreaButton)

        self.layout.add_widget(self.screenInfoBox)
        self.layout.add_widget(self.areaSpinnerBox)
        self.layout.add_widget(self.screenBox)

        self.add_widget(self.layout)

    def editArea(self, button):
        logger.debug("editing Area, TODO")
    
    def addArea(self, name, badge):
        if self.manager.gameObject.addArea(name, badge):
            #change spinner text to new Area, area object follows due to areaChanged
            self.areaSpinner.text = name
            #reload area spinner
            self.updateAreaSpinner()
            return 1
        return 0
    
    def setDefaultArea(self):
        """set area to default is current Area is None"""
        if self.manager.currentArea == None:
            logger.debug("setting area to default")
            self.areaSpinner.text = self.areaSpinnerString
            return
        self.areaSpinner.text = self.manager.currentArea.name
        logger.debug("popup skipped and area is valid, changing spinner text to correct text")
    
    def updateAreaSpinner(self):
        """updates the values that the spinner uses"""
        routeList = [route.name for route in self.manager.areaList]
        routeList.insert(0, gm.newAreaString)
        self.areaSpinner.values = routeList
    
    def on_pre_enter(self) -> bool:
        """adjusts areaSpinner text to area currently selected, returns 0 if area == None"""
        self.updateAreaSpinner()
        if self.manager.currentArea == None:
            logger.debug("No area selected")
            return 0
        self.areaSpinner.text = self.manager.currentArea.name
        return 1

    def areaChanged(self, spinner, text) -> bool:
        """text is the areaName"""
        #gets set to default when popup is canceled, otherwise crashes if the areaObject is None
        print(self.screenBox.size)
        if text == self.areaSpinnerString or self.manager.gameObject == None:
            logger.debug("default string for Area, or area invalid not doing anything")
            return 0
        
        if text == gm.newAreaString:
            logger.debug("creating popup to add new Area")
            self.editAreaButton.disabled = True
            newAreaBox = NewAreaBox(orientation = "vertical", confirmCallback = self.addArea)
            areaPopup = Popup(title = "add Area", content = newAreaBox)
            newAreaBox.dismiss = areaPopup.dismiss
            
            #newAreaBox.confirmButton.on_release(self.addArea)
            newAreaBox.cancelButton.on_release = lambda : [areaPopup.dismiss(), self.setDefaultArea()]
            
            areaPopup.open()
            return 0
        
        self.manager.currentArea = text
        self.editAreaButton.disabled = False
        logger.info(f"currentArea changed to {text}")
        return 1
        
    def on_enter(self):
        """call function to add next and previous buttons to the bottom of the screen"""
        #return if the function is already called, else create buttons. otherwise creates multiple buttons on each exit
        if self.entered:
            return
        #create buttons to navigate through the screens and add to layout
        self.buttons = BoxLayout(orientation = "horizontal", size_hint_y = 0.12)
        continueButton = TransparentButton(text = "next", size_hint_x = 0.2)
        continueButton.bind(on_press = self.nextScreen)
        exitGameButton = TransparentButton(text = "Exit and save Game", size_hint_x = 0.6, size_hint_y = 0.5, on_press = self.saveGame)
        previousButton = TransparentButton(text = "previous", size_hint_x = 0.2, pos_hint = {"x" : 0.8})
        previousButton.bind(on_press = self.previousScreen)
        self.buttons.pos_hint = {"y": 0, "x": 0}

        self.buttons.add_widget(previousButton)
        self.buttons.add_widget(exitGameButton)
        self.buttons.add_widget(continueButton)

        self.layout.add_widget(self.buttons)
        self.entered = True

    def cleanScreenBox(self):
        self.screenBox.clear_widgets()
    
    def nextScreen(self, instance):
        """go to the next screen"""
        self.manager.screenNumber += 1

    def previousScreen(self, instance):
        """go to previous screen"""
        self.manager.screenNumber -= 1
    
    def saveGame(self, button):
        self.manager.gameObject.writeToFile()
        self.manager.current = "selectGameScreen"
        #set the screennumber to 0 manually, setter instantly shows screen
        self.manager._screenNumber = 0



from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner


from transparentButton import TransparentButton
from backgroundScreen import BackgroundScreen
from loggerConfig import logger
import games as gm

class NuzlockeScreen(BackgroundScreen):
    """Parent screen, adds the name of the screen at the top, add self.layout which is a boxLayout. Can also add background for all screens except first screen, total of 0.2 size_hint_y"""
    
    def __init__(self, screenName, **kwargs):
        super().__init__(**kwargs)
        self.standardColor = gm.standardColor
        self.entered = False

        self.layout = BoxLayout(orientation= "vertical")
        self.screenBox = BoxLayout(orientation = "vertical", size_hint_y = 0.04)
        screenLabel = Label(text = screenName, color = self.standardColor)
        self.screenBox.add_widget(screenLabel)

        self.areaSpinner = Spinner(text = "choose an area", values = ["new Area"], size_hint_y = 0.04)
        self.areaSpinner.background_color = gm.opaque
        self.areaSpinner.scroll_timeout = 0.2
        self.areaSpinner.bind(text = self.areaChanged)

        self.layout.add_widget(self.screenBox)
        self.layout.add_widget(self.areaSpinner)


        self.add_widget(self.layout)

    def on_pre_enter(self):
        """adjusts areaSpinner text to area currently selected, returns 0 if area == None"""
        self.areaSpinner.values = [area.name for area in self.manager.areaList]
        if self.manager.currentArea == None:
            logger.debug("No area selected")
            return 0
        self.areaSpinner.text = self.manager.currentArea.name
        return 1

    def areaChanged(self, spinner, text):
        """text is the areaName"""
        self.manager.currentArea = text
        logger.info(f"currentArea changed to {text}")
        

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
    
    def nextScreen(self, instance):
        """go to the next screen"""
        self.manager.screenNumber += 1

    def previousScreen(self, insatnce):
        """go to previous screen"""
        self.manager.screenNumber -= 1
    
    def saveGame(self, button):
        self.manager.gameObject.writeToFile()
        self.manager.current = "selectGameScreen"
        #set the screennumber to 0 manually, setter instantly shows screen
        self.manager._screenNumber = 0



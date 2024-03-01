from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

import games as gm
from backgroundScreen import BackgroundScreen
from loggerConfig import logger
import platform as platform
from fileRetriever import FileRetriever
from games import MainGame

class SelectGameScreen(BackgroundScreen):
    def __init__(self, operatingSystem, **kwargs):
        super().__init__(**kwargs)
        self.game = None
        self.attempt = None
        self.fileRetriever = FileRetriever(operatingSystem)
        
        layout = BoxLayout(orientation= "vertical", spacing = 10, padding = 10)
        layout.size = Window.size
        layout.pos = self.pos
        #select the game
        gameSelection = BoxLayout(orientation = "vertical", size_hint_y= 0.05)
        self.gameDDM = Spinner(text = "Select the game", values = self.fileRetriever.checkGames())
        self.gameDDM.bind(text = self.gameChanged)
        self.gameDDM.background_color = gm.opaque

        gameSelection.add_widget(self.gameDDM)
        
        #select attempt, gets filled as soon as the gameselection is filled in
        attemptSelection = BoxLayout(orientation= "vertical", size_hint_y= 0.05)
        self.attemptSpinner = Spinner(text = "Select Attempt")
        self.attemptSpinner.bind(text = self.attemptSelected)
        self.attemptSpinner.background_color = gm.opaque
        self.attemptSpinner.disabled = True

        attemptSelection.add_widget(self.attemptSpinner)

        #gather info on attempt and display it
        attemptInfo = BoxLayout(orientation= "vertical", size_hint_y = 0.8)
        infoLabel = Label(text = "information about the attempt")
        attemptInfo.add_widget(infoLabel)

        #continue button
        continueBox = BoxLayout(orientation= "vertical", size_hint_y = 0.1)
        self.continueButton = Button(text = "Continue with attempt")
        self.continueButton.bind(on_press = self.startAttempt)
        self.continueButton.background_color = gm.opaque
        self.continueButton.disabled = True

        continueBox.add_widget(self.continueButton)
        
        layout.add_widget(gameSelection)
        layout.add_widget(attemptSelection)
        layout.add_widget(attemptInfo)
        layout.add_widget(continueBox)

        self.add_widget(layout)

    def gameChanged(self, instance, game : str) -> None:
        self.game = game
        self.continueButton.disabled = True
        if game == "New game":
            logger.info("TODO, implement popup for a new game")
            return
        self.retrieveSaveFile(game)
    
    def retrieveSaveFile(self, game : str) -> None:
        """updates save file spinner"""
        self.attemptSpinner.values = self.fileRetriever.getSaveFilesList(game)
        self.attemptSpinner.text = "select the attempt"
        self.attemptSpinner.disabled = False

    def attemptSelected(self, instance, attempt: str) -> None:
        """verifies the attempt selected and disables continuebutton"""
        if self.attemptSpinner.text == "select the attempt":
            return
        self.continueButton.disabled = False
        self.attempt = attempt
        self.continueButton.text = f"{self.game}: {self.attempt}"

    def startAttempt(self, instance) -> None:
        """create Game object and give it to windowManager"""
        #create Game Object, pass to new screen
        self.manager.attempt = self.attempt
        self.manager.gameObject = MainGame(self.fileRetriever, self.game, self.attempt)
        logger.info(f"loading {self.game} {self.attempt}")
        self.manager.current = "attemptInfoScreen"
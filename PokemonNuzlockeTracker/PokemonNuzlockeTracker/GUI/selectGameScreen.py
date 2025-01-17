from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout

import platform as platform

from GUI.backgroundScreen import BackgroundScreen
from GUI.Dialog.newGameDialog import NewGameDialog
from GUI.transparentButton import TransparentButton
from GUI.nuzlockeSpinner import NuzlockeSpinner

from Logic.dataRetriever import DataRetriever
from Logic.databaseModels.game import NLS
from Logic.games import newGameString, selectGameString, selectAttemptString, newAttemptString, opaque

from loggerConfig import logger

class SelectGameScreen(BackgroundScreen):
    def __init__(self, operatingSystem, **kwargs):
        super().__init__(**kwargs)
        self.GameRecord = None
        self.attemptNumber = -1

        self.newGameDialog = NewGameDialog(self)
        
        layout = BoxLayout(orientation= "vertical", spacing = 10, padding = 10)
        layout.size = Window.size
        layout.pos = self.pos
        #select the game
        gameSelection = BoxLayout(orientation = "vertical", size_hint_y= 0.05)

        self.gameDDM = NuzlockeSpinner(NLS.GAME, self.beforeGameChange, self.afterGameChange, hint_text = selectGameString, halign = "center", background_color = opaque)
        # self.gameDDM = Spinner(text = selectGameString, values = self.dataRetriever.retrieveGameList())
        # self.gameDDM.background_color = opaque

        gameSelection.add_widget(self.gameDDM)
        
        #select attempt, gets filled as soon as the gameselection is filled in
        attemptSelection = BoxLayout(orientation= "vertical", size_hint_y= 0.05)
        self.attemptSpinner = NuzlockeSpinner(NLS.ATTEMPT, self.attemptSelected, hint_text = selectAttemptString, halign = "center", background_color = opaque, disabled = True)

        attemptSelection.add_widget(self.attemptSpinner)

        #gather info on attempt and display it
        attemptInfo = BoxLayout(orientation= "vertical", size_hint_y = 0.8)
        infoLabel = Label(text = "information about the attempt", halign = "center")
        attemptInfo.add_widget(infoLabel)

        #continue button
        continueBox = BoxLayout(orientation= "vertical", size_hint_y = 0.1)
        self.settingsButton = TransparentButton(text = "TODO settings", size_hint_y = 0.4)
        self.continueButton = TransparentButton(text = "Continue with attempt", size_hint_y = 0.6)
        self.continueButton.bind(on_press = self.startAttempt)
        self.continueButton.disabled = True

        continueBox.add_widget(self.settingsButton)
        continueBox.add_widget(self.continueButton)
        
        layout.add_widget(gameSelection)
        layout.add_widget(attemptSelection)
        layout.add_widget(attemptInfo)
        layout.add_widget(continueBox)

        self.add_widget(layout)
        
    def beforeGameChange(self, gameName):
        self.continueButton.disabled = True
        if gameName == newGameString:
            self.newGameDialog.open()
            return 0
        return 1

    def afterGameChange(self) -> None:
        self.GameRecord = self.manager.getGameRecord(self.gameDDM.lookupID)
        if self.GameRecord == None:
            logger.error("Game not valid")
            return 0
        self.retrieveSaveFile(self.GameRecord.IDGame)
        return 1

    def createNewGame(self, gameName: str) -> bool:
        """checks if game already exists otherwise creates the directories, updates the gameList"""
        #check if game is already present
        if self.gameExists(gameName):
            newGameName = self.getGameName(gameName)
            self.gameDDM.text = newGameName
            self.newGameDialog.dismiss()
            return 0
            
        #create new game, folders and all
        gameRecord = self.manager.addGame(gameName, self.newGameDialog.content.getNewGameGenerationInput())
        if gameRecord != None:
            self.GameRecord = gameRecord
            self.gameDDM.text = self.getGameName(gameRecord.name)
            self.updateGameSpinnerValues()
            self.continueButton.disabled = False
            return 1
        return 0

    def gameExists(self, gameName: str) -> bool:
        """returns is the game exists using a database call"""
        return self.manager.gameExists(gameName)

    def updateGameSpinnerValues(self) -> None:
        """refresh list of games"""
        self.gameDDM.updateSpinnerValues()

    def getGameName(self, gameName: str) -> str:
        """returns the name already present in the spinner values, returns given string if the game is not found, eg a new game"""
        capGameName = gameName.lower()
        for name in self.gameDDM.spinnerValues.values():
            if name.lower() == capGameName:
                return name
        return gameName

    def retrieveSaveFile(self, IDGame : int) -> None:
        """updates save file spinner"""
        logger.debug(f"retrieving IDGame:{IDGame} savefiles")
        self.attemptSpinner.IDParam1 = IDGame
        self.attemptSpinner.disabled = False
        self.continueButton.disabled = False

    def attemptSelected(self, attempt: str) -> None:
        """verifies the attempt selected and updates continuebutton text"""
        if self.attemptSpinner.text == selectAttemptString:
            return 0
        
        self.attemptNumber = -1 if attempt == newAttemptString else int(attempt.strip("attempt "))
        self.continueButton.text = f"{self.GameRecord.name}: {newAttemptString if self.attemptNumber == -1 else attempt}"
        return 1

    def startAttempt(self, instance) -> None:
        """create Game object and give it to windowManager"""
        logger.info(f"loading {self.GameRecord.name} {self.attemptNumber}")
        
        if self.attemptNumber == -1:
            attemptRecord = self.manager.newAttempt(self.GameRecord.IDGame)
        else:
            attemptRecord = self.manager.getAttemptRecord(self.attemptSpinner.lookupID)
        
        if attemptRecord == None:
            logger.error("Attempt not found")
            return
        self.manager.startPokemonGame(attemptRecord)
        

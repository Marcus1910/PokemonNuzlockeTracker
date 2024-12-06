from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout

import platform as platform

from GUI.backgroundScreen import BackgroundScreen
from GUI.Dialog.newGameDialog import NewGameDialog
from GUI.transparentButton import TransparentButton

from Logic.dataRetriever import DataRetriever
import Logic.games as gm
from Logic.games import newGameString, selectGameString, selectAttemptString, newAttemptString, opaque

from loggerConfig import logger

class SelectGameScreen(BackgroundScreen):
    def __init__(self, operatingSystem, **kwargs):
        super().__init__(**kwargs)
        self.GameRecord = None
        self.attemptNumber = -1
        self.dataRetriever = DataRetriever(operatingSystem)

        self.newGameDialog = NewGameDialog(self)
        
        layout = BoxLayout(orientation= "vertical", spacing = 10, padding = 10)
        layout.size = Window.size
        layout.pos = self.pos
        #select the game
        gameSelection = BoxLayout(orientation = "vertical", size_hint_y= 0.05)

        self.gameDDM = Spinner(text = selectGameString, values = self.dataRetriever.retrieveGameList())
        self.gameDDM.bind(text = self.gameChanged)
        self.gameDDM.background_color = gm.opaque

        gameSelection.add_widget(self.gameDDM)
        
        #select attempt, gets filled as soon as the gameselection is filled in
        attemptSelection = BoxLayout(orientation= "vertical", size_hint_y= 0.05)
        self.attemptSpinner = Spinner(text = selectAttemptString)
        self.attemptSpinner.bind(text = self.attemptSelected)
        self.attemptSpinner.background_color = gm.opaque
        self.attemptSpinner.disabled = True
        #self.attemptSpinner.text_autoupdate = True

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

    def gameChanged(self, instance, gameName: str) -> None:
        self.continueButton.disabled = True
        
        if gameName == newGameString:
            self.newGameDialog.open()
            return
        
        self.GameRecord = self.dataRetriever.getGameRecordFromGameName(gameName)
        print(self.GameRecord)
        if self.GameRecord == None:
            logger.error("Game not valid")
            return
        
        self.retrieveSaveFile(self.GameRecord.IDGame)

    def createNewGame(self, gameName: str) -> bool:
        """checks if game already exists otherwise creates the directories, updates the gameList"""
        newGameName = self.getGameName(gameName)
        
        #check if game is already present
        if self.gameExists(newGameName):
            logger.info(f"{gameName} is already a game")
            self.gameDDM.text = newGameName
            self.newGameDialog.dismiss()
            return 0
            
        #create new game, folders and all
        gameRecord = self.dataRetriever.addGame(gameName, self.newGameDialog.content.getNewGameGenerationInput())
        print(gameRecord)
        if gameRecord != None:
            self.GameRecord = gameRecord
            self.gameDDM.text = self.getGameName(gameRecord.name)
            self.updateGameSpinnerValues()
            self.continueButton.disabled = False
            return 1
        
        return 0

    def gameExists(self, gameName: str) -> bool:
        """returns is the game exists using a database call"""
        return self.dataRetriever.gameExists(gameName)

    def updateGameSpinnerValues(self) -> None:
        self.gameDDM.values = self.dataRetriever.retrieveGameList()

    def getGameName(self, gameName: str) -> str:
        """returns the name already present in the spinner values, returns given string if the game is not found, eg a new game"""
        capGameName = gameName.capitalize()
        for name in self.gameDDM.values:
            if name.capitalize() == capGameName:
                return name
        return gameName

    def retrieveSaveFile(self, IDGame : int) -> None:
        """updates save file spinner"""
        logger.debug(f"retrieving IDGame:{IDGame} savefiles")
        self.attemptSpinner.values = self.dataRetriever.getSaveFilesList(IDGame)
        self.attemptSpinner.text = self.attemptSpinner.values[0]
        self.attemptSpinner.disabled = False
        self.continueButton.disabled = False

    def attemptSelected(self, instance, attempt: str) -> None:
        """verifies the attempt selected and updates continuebutton text"""
        print("updating attempt selected")
        if self.attemptSpinner.text == "select the attempt":
            return
        self.attemptNumber = -1 if attempt == newAttemptString else int(attempt.strip("attempt "))
        self.continueButton.text = f"{self.GameRecord.name}: {newAttemptString if self.attemptNumber == -1 else attempt}"

    def startAttempt(self, instance) -> None:
        """create Game object and give it to windowManager"""
        logger.info(f"loading {self.GameRecord.name} {self.attemptNumber}")
        
        if self.attemptNumber == -1:
            attemptRecord = self.dataRetriever.newAttempt(self.GameRecord.IDGame)
        else:
            attemptRecord = self.dataRetriever.getAttemptRecord(self.GameRecord.IDGame, self.attemptNumber)
        
        if attemptRecord == None:
            logger.error("Attempt not found")
            return
        self.manager.startPokemonGame(attemptRecord, self.dataRetriever)
        

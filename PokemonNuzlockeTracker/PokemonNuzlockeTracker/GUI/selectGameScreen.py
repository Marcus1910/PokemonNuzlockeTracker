from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

import games as gm
from backgroundScreen import BackgroundScreen
import os
from loggerConfig import logger
import platform as platform
from android.storage import app_storage_path



class SelectGameScreen(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # pathToImage = os.path.join(os.path.dirname(os.getcwd()), "images", "bg.jpg")
        # print(pathToImage)
        self.game = None
        self.attempt = None
        
        layout = BoxLayout(orientation= "vertical", spacing = 10, padding = 10)
        layout.size = Window.size
        layout.pos = self.pos
        #select the game
        gameSelection = BoxLayout(orientation = "vertical", size_hint_y= 0.05)
        self.gameDDM = Spinner(text = "Select the game", values = gm.checkGames())
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

        #export button to export
        self.exportButton = Button(text = "Export saves", on_release = self.exportSaves)
        self.importButton = Button(text = "Import saves", on_release = self.importSaves)

        #continue button
        continueBox = BoxLayout(orientation= "vertical", size_hint_y = 0.1)
        self.continueButton = Button(text = "Continue with attempt")
        self.continueButton.bind(on_press = self.startAttempt)
        self.continueButton.background_color = gm.opaque
        self.continueButton.disabled = True

        continueBox.add_widget(self.exportButton)
        continueBox.add_widget(self.importButton)
        continueBox.add_widget(self.continueButton)
        
        layout.add_widget(gameSelection)
        layout.add_widget(attemptSelection)
        layout.add_widget(attemptInfo)
        layout.add_widget(continueBox)

        self.add_widget(layout)

    def gameChanged(self, instance, game:str):
        self.game = game
        self.continueButton.disabled = True
        if game == "new":
            return
        self.retrieveSaveFile(game)
    
    def retrieveSaveFile(self, game):
        """updates save file spinner"""
        self.attemptSpinner.values = gm.getSaveFiles(game)
        self.attemptSpinner.text = "select the attempt"
        self.attemptSpinner.disabled = False

    def attemptSelected(self, instance, attempt):
        """verifies the attempt selected and disables continuebutton"""
        if self.attemptSpinner.text == "select the attempt":
            return
        self.continueButton.disabled = False
        self.attempt = attempt
        self.continueButton.text = f"{self.game}: {self.attempt}"
    
    def exportSaves(self, *args):
        """Determine on which platform it runs and change the way in which the saves are exported"""
        #should be earlier in the code, so loading is also affected, perhaps the gameObject class
        OS = platform.system()
        # print(OS)
        # if OS == "Linux":
        #     storagePath = app_storage_path()
        #     print(storagePath)
        #     newFile = os.path.join(storagePath, "kankerget.txt")
        #     with open(newFile, "w") as file:
        #         file.write("kankerget")
        #     print(f"created {newFile}")

        print(os.getcwd())
    
    def importSaves(self, *args):
        OS = platform.system()
        if OS == "Linux":
            storagePath = app_storage_path()
            print(storagePath)
            newFile = os.path.join(storagePath, "kankerget.txt")
            print(f"reading {newFile}")
            with open(newFile, "r") as file:
                print(file.read())

    def startAttempt(self, instance):
        """create Game object and give it to windowManager"""
        #create Game Object, pass to new screen
        self.manager.attempt = self.attempt
        self.manager.gameObject = gm.MainGame(self.game, self.attempt)
        logger.info(f"loading {self.game} {self.attempt}")
        # print(self.manager.gameObject)
        # GameObject = self.manager.gameObject.retrieveGameData()
        # #list = GameObject.
        # print(GameObject)
        self.manager.current = "attemptInfoScreen"
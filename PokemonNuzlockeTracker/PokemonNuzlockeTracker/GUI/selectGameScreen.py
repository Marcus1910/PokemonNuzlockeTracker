from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

import games as gm
import os


class SelectGameScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectGameScreen, self).__init__(**kwargs)
        # pathToImage = os.path.join(os.path.dirname(os.getcwd()), "images", "bg.jpg")
        # print(pathToImage)
        self.game = None
        self.attempt = None

        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background.jpg"))
        bgImage.size = Window.size
        bgImage.pos = self.pos
        
        layout = BoxLayout(orientation= "vertical", spacing = 10, padding = 10)
        layout.size = Window.size
        layout.pos = self.pos

        #select the game
        gameSelection = BoxLayout(orientation = "vertical", size_hint_y= 0.05)
        self.gameDDM = Spinner(text = "Select the game", values = gm.checkGames())
        self.gameDDM.bind(text = self.gameChanged)

        gameSelection.add_widget(self.gameDDM)
        
        #select attempt, gets filled as soon as the gameselection is filled in
        attemptSelection = BoxLayout(orientation= "vertical", size_hint_y= 0.05)
        self.attemptSpinner = Spinner(text = "Select Attempt")
        self.attemptSpinner.bind(text = self.attemptSelected)
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
        self.continueButton.disabled = True
        continueBox.add_widget(self.continueButton)
        
        layout.add_widget(gameSelection)
        layout.add_widget(attemptSelection)
        layout.add_widget(attemptInfo)
        layout.add_widget(continueBox)

        self.add_widget(bgImage)
        self.add_widget(layout)

    def gameChanged(self, instance, game:str):
        self.game = game
        self.continueButton.disabled = True
        if game == "new":
            return
        self.retrieveSaveFile(game)
    
    def retrieveSaveFile(self, game):
        self.attemptSpinner.values = gm.getSaveFiles(game)
        self.attemptSpinner.text = "select the attempt"
        

        self.attemptSpinner.disabled = False

    def attemptSelected(self, instance, attempt):
        if self.attemptSpinner.text == "select the attempt":
            return
        self.continueButton.disabled = False
        self.attempt = attempt
        self.continueButton.text = f"{self.game}: {self.attempt}"

    def startAttempt(self, instance):
        #create Game Object, pass to new screen
        self.manager.gameObject = gm.MainGame(self.game, self.attempt)
        # print(self.manager.gameObject)
        # GameObject = self.manager.gameObject.retrieveGameData()
        # #list = GameObject.
        # print(GameObject)
        self.manager.current = "attemptInfoScreen"
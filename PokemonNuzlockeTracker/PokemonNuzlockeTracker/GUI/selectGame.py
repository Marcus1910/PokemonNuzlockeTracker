from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle

import games as gm
import os

#define different screens
class TrainerScreen(Screen):
    def on_enter(self):
        self.background_color = (1, 0, 0, 1)  # Red background

class ItemScreen(Screen):
    pass

class EncounterScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class SelectGame(App):
    def build(self):
        self.game = None
        self.attempt = None
        root = Widget()

        # pathToImage = os.path.join(os.path.dirname(os.getcwd()), "images", "bg.jpg")
        # print(pathToImage)

        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background.jpg"))
        bgImage.size = Window.size
        bgImage.pos = root.pos
        
        layout = BoxLayout(orientation= "vertical", spacing = 10, padding = 10)
        layout.size = Window.size
        layout.pos = root.pos

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
        self.continueButton.disabled = True
        continueBox.add_widget(self.continueButton)
        
        layout.add_widget(gameSelection)
        layout.add_widget(attemptSelection)
        layout.add_widget(attemptInfo)
        layout.add_widget(continueBox)

        root.add_widget(bgImage)
        root.add_widget(layout)


        return root
    
    def gameChanged(self, instance, game:str):
        self.game = game
        self.continueButton.disabled = True
        print(f"changed game to {self.game}")
        if self.game == "new":
            return
        self.retrieveSaveFile(game)
    
    def retrieveSaveFile(self, game):
        self.attemptSpinner.values = gm.getSaveFiles(game)
        self.attemptSpinner.text = "select the attempt"
        

        self.attemptSpinner.disabled = False

    def attemptSelected(self, instance, attempt):
        if self.attemptSpinner.text == "select the attempt":
            print("doe niks")
            return
        self.continueButton.disabled = False
        self.attempt = attempt
        self.continueButton.text = f"game: {self.game}, attempt: {self.attempt}"
        print(f"game: {self.game}, attempt: {self.attempt}")



    
        # self.sm = WindowManager()
        # screen1 = TrainerScreen()
        # screen2 = ItemScreen()
        # screen3 = EncounterScreen()
        # self.sm.add_widget(screen1(name = "first"))
        # self.sm.add_widget(screen2)
        # self.sm.add_widget(screen3)
        # self.sm.current = "first"
        # return self.sm


# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.button import Button

# class MyApp(App):
#     def build(self):
#         # Create the main horizontal BoxLayout
#         layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

#         # Create and add the first part
#         part1 = BoxLayout(orientation='horizontal')
#         label1 = Label(text="Part 1")
#         button1 = Button(text="Button 1")
#         part1.add_widget(label1)
#         part1.add_widget(button1)

#         # Create and add the second part
#         part2 = BoxLayout(orientation='horizontal')
#         label2 = Label(text="Part 2")
#         button2 = Button(text="Button 2")
#         part2.add_widget(label2)
#         part2.add_widget(button2)

#         # Create and add the third part
#         part3 = BoxLayout(orientation='vertical')
#         label3 = Label(text="Part 3")
#         button3 = Button(text="Button 3")
#         part3.add_widget(label3)
#         part3.add_widget(button3)

#         # Create and add the fourth part
#         part4 = BoxLayout(orientation='vertical')
#         label4 = Label(text="Part 4")
#         button4 = Button(text="Button 4")
#         part4.add_widget(label4)
#         part4.add_widget(button4)

#         # Add the four parts to the main layout
#         layout.add_widget(part1)
#         layout.add_widget(part2)
#         layout.add_widget(part3)
#         layout.add_widget(part4)

#         return layout

# if __name__ == '__main__':
#     MyApp().run()
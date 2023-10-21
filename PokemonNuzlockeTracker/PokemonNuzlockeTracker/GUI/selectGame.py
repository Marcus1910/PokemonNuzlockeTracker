from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window

import games as gm
from selectGameScreen import SelectGameScreen
import os
import time

#define different screens
class TrainerScreen(Screen):
    def on_enter(self):
        self.background_color = (1, 0, 0, 1)  # Red background

class ItemScreen(Screen):
    pass

class EncounterScreen(Screen):
    pass

class WindowManager(ScreenManager):
    attempt = None
    _gameObject = None
    areaList = None


    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self, gameObject):
        self._gameObject = gameObject
        print("gathering data")
        self.areaList = self._gameObject.retrieveGameData()

class NuzlockeScreen(Screen):
    """adds the name of the screen at the top, add self.layout which is a boxLayout. Can also add background for all screens except first screen"""
    def __init__(self, screenName, **kwargs):
        
        super(NuzlockeScreen, self).__init__(**kwargs)

        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background.jpg"))
        bgImage.size = Window.size
        bgImage.pos = self.pos

        self.layout = BoxLayout(orientation= "vertical")
        self.screenBox = BoxLayout(orientation = "vertical", size_hint_y = 0.05)
        screenLabel = Label(text = screenName, color = (0, 0, 0, 1))

        self.screenBox.add_widget(screenLabel)
        self.layout.add_widget(self.screenBox)

        self.add_widget(bgImage)
        self.add_widget(self.layout)


class AttemptInfoScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(AttemptInfoScreen, self).__init__(screenName = screenName, **kwargs)



        self.badgeLabel = Label(text = "gathering data", color = (0, 0, 0, 1), size_hint_y = 0.2)
        self.areaLabel = Label(text = "gathering data", color = (0, 0, 0, 1), size_hint_y = 0.15)

        self.pcBox = BoxLayout(orientation= "vertical", size_hint_y = 0.3)
        pcLabel = Label(text = "Pokemon still available Placeholder", color = (0, 0, 0, 1))
        self.pcBox.add_widget(pcLabel)

        self.graveBox = BoxLayout(orientation = "vertical", size_hint_y = 0.3)
        graveLabel = Label(text = "Fainted pokemon placeholder", color = (0, 0, 0, 1))
        self.graveBox.add_widget(graveLabel)

        
        self.layout.add_widget(self.areaLabel)
        self.layout.add_widget(self.badgeLabel)
        self.layout.add_widget(self.pcBox)
        self.layout.add_widget(self.graveBox)

    def on_enter(self):
        #print(self.manager.gameObject.retrieveGameData())
        badge = self.manager.gameObject.badge
        self.badgeLabel.text = f"amount of badges: {badge}"

        AreaList = self.manager.gameObject.areaList
        self.areaLabel.text = f"current area: {AreaList[6].name}"









class SelectGame(App):

    def build(self):
        #given by selectgameWindow
        

        sm = WindowManager()
        selectGameScreen = SelectGameScreen(name = "selectGameScreen")
        trainerScreen = TrainerScreen(name = "trainerScreen")
        attemptInfoScreen = AttemptInfoScreen(name = "attemptInfoScreen", screenName = f"Info on current attempt")
        #attemptInfoScreen = NuzlockeScreen(name = "attemptInfoScreen", )

        sm.add_widget(selectGameScreen)
        sm.add_widget(trainerScreen)
        sm.add_widget(attemptInfoScreen)

        sm.current = "selectGameScreen"
        return sm
    

    




    
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
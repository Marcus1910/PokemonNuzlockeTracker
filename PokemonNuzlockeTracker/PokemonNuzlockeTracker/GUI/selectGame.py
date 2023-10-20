from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
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
        root = BoxLayout()
        # pathToImage = os.path.join(os.path.dirname(os.getcwd()), "images", "bg.jpg")
        # print(pathToImage)
        bgImage = Image(source = os.path.join(os.path.dirname(os.getcwd()), "images", "background.jpg"))
        bgImage.allow_stretch = True
        bgImage.keep_ratio = True
        root.add_widget(bgImage)
        # layout = BoxLayout(orientation='vertical')
        # label = Label(text=f"{gm.checkGames()}")
        # layout.add_widget(label)

        return root
        # self.sm = WindowManager()
        # screen1 = TrainerScreen()
        # screen2 = ItemScreen()
        # screen3 = EncounterScreen()
        # self.sm.add_widget(screen1(name = "first"))
        # self.sm.add_widget(screen2)
        # self.sm.add_widget(screen3)
        # self.sm.current = "first"
        # return self.sm

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import games as gm

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


class KivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text=f"{gm.checkGames()}")
        layout.add_widget(label)

        return layout
        # self.sm = WindowManager()
        # screen1 = TrainerScreen()
        # screen2 = ItemScreen()
        # screen3 = EncounterScreen()
        # self.sm.add_widget(screen1(name = "first"))
        # self.sm.add_widget(screen2)
        # self.sm.add_widget(screen3)
        # self.sm.current = "first"
        # return self.sm


if __name__ == "__main__":
    app = KivyApp()
    app.run()
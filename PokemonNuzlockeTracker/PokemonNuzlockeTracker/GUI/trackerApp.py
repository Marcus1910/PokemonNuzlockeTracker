from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

from GUI.windowmanager import WindowManager
from GUI.selectGameScreen import SelectGameScreen
from Logic.dataRetriever import DataRetriever

from loggerConfig import logger

import sys

def excepthook(type, value, traceback):
    # Handle the exception
    print(f"Type:{type}, Error: {value}, traceback: {traceback}")

sys.excepthook = excepthook


class TrackerApp(MDApp):
    def __init__(self, operatingSystem, **kwargs):
        super().__init__(**kwargs)
        self.operatingSystem = operatingSystem
        self.windowManager = None

    def build(self):
            #use OS to change view to that of android
            self.game = None

            if self.operatingSystem == "Windows":
                logger.info("detected windows")
                Window.size = (390, 780)
            elif self.operatingSystem == "Linux":
                Window.size = (700, 1000)
            else:
                Window.Fullscreen = True
            
            dataRetriever = DataRetriever(self.operatingSystem)
            self.windowManager = WindowManager(dataRetriever)
            selectGameScreen = SelectGameScreen(operatingSystem = self.operatingSystem, name = "selectGameScreen")
            self.windowManager.add_widget(selectGameScreen)

            self.windowManager.current = "selectGameScreen"
            return self.windowManager

    # def on_stop(self, *args):
    #     print("opening exit dialog")
    #     exitDialog = MDDialog('fuck')
    #     exitDialog.open() 
    #     return True
        
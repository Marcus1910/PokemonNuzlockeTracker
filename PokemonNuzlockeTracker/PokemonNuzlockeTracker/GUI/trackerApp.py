from kivymd.app import MDApp
from kivy.core.window import Window

from GUI.windowmanager import WindowManager
from GUI.selectGameScreen import SelectGameScreen

from loggerConfig import logger


class TrackerApp(MDApp):
    def __init__(self, operatingSystem, **kwargs):
        super().__init__(**kwargs)
        self.operatingSystem = operatingSystem
        self.dataRetriever = None

    def build(self):
        #use OS to change view to that of android
        self.game = None

        if self.operatingSystem == "Windows":
            logger.info("detected windows")
            Window.size = (390, 780)

        sm = WindowManager(self.operatingSystem)
        selectGameScreen = SelectGameScreen(operatingSystem = self.operatingSystem, name = "selectGameScreen")
        sm.add_widget(selectGameScreen)

        sm.current = "selectGameScreen"
        return sm
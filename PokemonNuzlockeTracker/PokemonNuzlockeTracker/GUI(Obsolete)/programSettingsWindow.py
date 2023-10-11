import tkinter as tk
from templateWindow import TemplateWindow

class ProgramSettingsWindow(TemplateWindow):
    def __init__(self, x, y, parent=None):
        super().__init__(x, y, parent)
        self._master.title("Program Settings")
        textLabel = tk.Label(self._master, text = "hier moeten de opties komen die uit 'settings.py' gehaald worden").grid(row = 0, column = 0)
        self.update()
        self.run()
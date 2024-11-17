from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton

class NewGameDialog(MDDialog):
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.title = "Add new game"
        self.auto_dismiss = False
        self.type = "custom"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.65}
        self.content = NewGameBox(size_hint_y = None)
        self.buttons = [MDFlatButton(text = "Add game", on_release = self.createNewGame), MDFlatButton(text = "dismiss", on_release = self.dismiss)]
        self.content_cls = self.content
        super().__init__(**kwargs)
    
    def open(self, *args, **kwargs):
        super().open()
    
    def createNewGame(self, instance) -> None:
        gameName = self.content.getInput()
        if self.screen.createNewGame(gameName):
            self.dismiss()

class NewGameBox(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.height = "100dp"
        self.newGameLabel = MDTextField(hint_text = "New Game Name")
        self.add_widget(self.newGameLabel)
    
    def getInput(self) -> str:
        return self.newGameLabel.text

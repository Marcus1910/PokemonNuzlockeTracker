from templateWindow import TemplateWindow

class TestWindow(TemplateWindow):
    def __init__(self):
        super().__init__(400, 500)
        self.master.geometry("650x450")
        super().update()
        
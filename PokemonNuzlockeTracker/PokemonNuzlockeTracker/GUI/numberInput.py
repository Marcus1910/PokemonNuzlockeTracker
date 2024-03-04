from kivy.uix.textinput import TextInput

class NumberInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 1:
            return
        if not substring.isdigit():
            return
        super(NumberInput, self).insert_text(substring, from_undo=from_undo)

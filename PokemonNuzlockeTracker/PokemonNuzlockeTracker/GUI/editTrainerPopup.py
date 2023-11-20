from kivy.uix.popup import Popup


class EditTrainerPopup(Popup):
    def __init__(self, trainerObject = None, **kwargs):
        """returns a trainerObject or None when popup is closed"""
        super().__init__(**kwargs)
        trainerName = None if trainerObject == None else trainerObject.name
        print(trainerName)

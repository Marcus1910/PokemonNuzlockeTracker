from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivymd.app import MDApp 
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import dropdownitem
from kivymd.uix.textfield import MDTextField

from GUI.transparentButton import TransparentButton

from Logic.databaseModels.game import NLS, opaque, standardColor

class NuzlockeLookupSpinner(TextInput):
    def __init__(self, nlsType: NLS, **kwargs):
        super().__init__(**kwargs)
        self.manager = MDApp.get_running_app().windowManager
        self.nlsType = nlsType
        self.background_color = opaque
        self._spinnerValues = {}
        self._lookupID = None
        self._IDParam1 = None #used for advanced filtering -> attempt from game
        self.dropdown = DropDown()
        self.updateSpinnerValues()
        
        self.bind(focus = self.spinnerTextFocus)
        self.bind(text = self.updateSpinnerValues)

    @property
    def spinnerValues(self) -> dict:
        return self._spinnerValues

    @spinnerValues.setter
    def spinnerValues(self, spinnerValues: dict):
        if self._spinnerValues != spinnerValues:
            self._spinnerValues = spinnerValues
            self.populateDropDown()
    @property
    def lookupID(self):
        if self._lookupID is None:
            raise ValueError("lookupID is None")
        return self._lookupID
    
    @lookupID.setter
    def lookupID(self, lookupID):
        self._lookupID = lookupID
        print(self.spinnerValues)
        self.text = (self.spinnerValues[lookupID])
    
    @property
    def IDParam1(self):
        return self._IDParam1
    
    @IDParam1.setter
    def IDParam1(self, IDParam1):
        self._IDParam1 = IDParam1     

    def openSpinnerDropDown(self, open: bool):
        if open:
            self.dropdown.open(self)
        else:
            self.dropdown.dismiss()

    def populateDropDown(self):
        self.dropdown.clear_widgets()     
        for IDSpinnervalue, spinnerValue in self.spinnerValues.items():
            btn = TransparentButton(text = spinnerValue, size_hint_y = None, height = 50, on_release = lambda btn, spv = spinnerValue, id = IDSpinnervalue: self.spinnerValueChanged(spv, id))
            self.dropdown.add_widget(btn)
    
    def spinnerValueChanged(self, text: str, IDSpinnerValue):
        self.text = text
        self.lookupID = IDSpinnerValue
        self.openSpinnerDropDown(False)
    
    def spinnerTextFocus(self, instance, focused):
        #add all values when nothing is selected
        if self.text == "":
            self.updateSpinnerValues()       
        self.openSpinnerDropDown(focused)
    
    def updateSpinnerValues(self, instance = None, text: str = ""):
        self.spinnerValues = self.manager.getLookupValues(self.nlsType, text, self.IDParam1)

class NuzlockeSpinner(NuzlockeLookupSpinner):
    def __init__(self, nlsType: NLS, valuesChangedFunction: callable, afterValidation: callable = None, **kwargs):
        super().__init__(nlsType, **kwargs)
        self.valueChangedFunction = valuesChangedFunction
        self.afterValidation = afterValidation

    def spinnerValueChanged(self, text: str, IDSpinnerValue):
        if self.valueChangedFunction(text):
            super().spinnerValueChanged(text, IDSpinnerValue)
            if callable(self.afterValidation):
                self.afterValidation()
            
        
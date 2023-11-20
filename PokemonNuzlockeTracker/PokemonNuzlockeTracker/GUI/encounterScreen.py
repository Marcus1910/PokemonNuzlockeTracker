from nuzlockeScreen import NuzlockeScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class EncounterScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        self.encounterBox = BoxLayout(orientation= 'vertical', size_hint_y = 0.8)
        
        self.encounterTypeList = []
        self.areaSelectionBox = BoxLayout(orientation = "horizontal", size_hint_y = 0.2, pos_hint = {"top": 1})
        self.catchableEncounterBox = BoxLayout(orientation= 'horizontal', size_hint_y = 0.8)

        self.encounterBox.add_widget(self.areaSelectionBox)
        self.encounterBox.add_widget(self.catchableEncounterBox)

        self.layout.add_widget(self.encounterBox)
    
    def areaChanged(self, spinner, text):
        super().areaChanged(spinner, text)
        self.clearLayout()
        self.encounterTypeList = []
        self.encounters = self.manager.currentArea.encounters
        self.updateEncounters()

    def updateEncounters(self):
        for index, encounterType in enumerate(self.encounters):
            print(encounterType)
            self.encounterTypeList.append(encounterType[0])
            button = Button(text = encounterType[0], size_hint_x = 0.2)
            button.bind(on_press = lambda instance, encounterType = encounterType: self.showEncounterType(encounterType))
            self.areaSelectionBox.add_widget(button)
    
    def showEncounterType(self, encounterType):
        for encounter in encounterType[1]:
            print(encounter.name)
        
    def clearLayout(self):
        self.areaSelectionBox.clear_widgets()
        self.catchableEncounterBox.clear_widgets()
        
        

            
        
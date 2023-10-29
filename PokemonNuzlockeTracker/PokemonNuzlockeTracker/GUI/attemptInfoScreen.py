from nuzlockeScreen import NuzlockeScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class AttemptInfoScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super(AttemptInfoScreen, self).__init__(screenName = screenName, **kwargs)

        
        self.areaLabel = Label(text = "gathering data", color = (0, 0, 0, 1), size_hint_y = 0.125)
        self.badgeLabel = Label(text = "gathering data", color = (0, 0, 0, 1), size_hint_y = 0.175)

        self.pcBox = BoxLayout(orientation= "vertical", size_hint_y = 0.25)
        pcLabel = Label(text = "Pokemon still available Placeholder", color = (0, 0, 0, 1))
        self.pcBox.add_widget(pcLabel)

        self.graveBox = BoxLayout(orientation = "vertical", size_hint_y = 0.25)
        graveLabel = Label(text = "Fainted pokemon placeholder", color = (0, 0, 0, 1))
        self.graveBox.add_widget(graveLabel)

        self.layout.add_widget(self.areaLabel)
        self.layout.add_widget(self.badgeLabel)
        self.layout.add_widget(self.pcBox)
        self.layout.add_widget(self.graveBox)
    
    def areaChanged(self, spinner, text):
        super().areaChanged(spinner, text)
        #print(self.manager.gameObject.retrieveGameData())
        badge = self.manager.gameObject.badge
        self.badgeLabel.text = f"amount of badges: {badge}"

        AreaList = self.manager.gameObject.areaList
        self.areaLabel.text = f"current area: {self.manager.currentArea.name}"

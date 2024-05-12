from nuzlockeScreen import NuzlockeScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class AttemptInfoScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)

        self.areaLabel = Label(text = "gathering data", color = self.standardColor, size_hint_y = 0.125)
        self.badgeLabel = Label(text = "gathering data", color = self.standardColor, size_hint_y = 0.175)

        self.pcBox = BoxLayout(orientation= "vertical", size_hint_y = 0.25)
        pcLabel = Label(text = "Pokemon still available Placeholder", color = self.standardColor)
        self.pcBox.add_widget(pcLabel)

        self.graveBox = BoxLayout(orientation = "vertical", size_hint_y = 0.25)
        graveLabel = Label(text = "Fainted pokemon placeholder", color = self.standardColor)
        self.graveBox.add_widget(graveLabel)

        self.screenBox.add_widget(self.areaLabel)
        self.screenBox.add_widget(self.badgeLabel)
        self.screenBox.add_widget(self.pcBox)
        self.screenBox.add_widget(self.graveBox)
    
    def areaChanged(self, spinner, text):
        if not super().areaChanged(spinner, text):
            #area has not been changed succesfully
            return
        badge = self.manager.gameObject.badge
        self.badgeLabel.text = f"amount of badges: {badge}"
        self.areaLabel.text = f"current area: {self.manager.currentArea.name}"

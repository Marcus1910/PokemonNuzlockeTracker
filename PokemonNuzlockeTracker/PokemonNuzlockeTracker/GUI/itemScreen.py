from nuzlockeScreen import NuzlockeScreen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label

class ItemScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        self.items = None

        # Create a scroll view
        self.scroll_view = ScrollView(do_scroll_y = True, do_scroll_x = False, size_hint=(1, 1))
        self.boxWithItems = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=5)
        self.boxWithItems.bind(minimum_height=self.boxWithItems.setter('height'))

        # Add the box layout to the scroll view
        self.scroll_view.add_widget(self.boxWithItems)
        # self.itemBox.add_widget(self.scroll_view)
        # self.itemBox.add_widget(outerBox)

        self.layout.add_widget(self.scroll_view)
    
    def areaChanged(self, spinner, text):
        """when the area changes update all items on screen"""
        if not super().areaChanged(spinner, text):
            return
        self.items = self.manager.currentArea.items
        self.updateLayout()
    
    def updateLayout(self):
        self.clearLayout()
        for index, itemObject in enumerate(self.items):
            print(itemObject)
            pass

    def clearLayout(self):
        self.boxWithItems.clear_widgets()


class ItemBox(BoxLayout):
    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.itemObject = item


        
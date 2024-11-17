from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from .nuzlockeScreen import NuzlockeScreen
from .expandableBox import ItemBox
from .transparentButton import TransparentButton
from .addDialog import AddItemDialog

from loggerConfig import logger

class ItemScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)
        
        self.areaObject = None
        self.items = None
        self.boxWithItems = GridLayout(cols = 1, size_hint_y = None)
        self.itemScroll = ScrollView(size = (self.boxWithItems.width, self.boxWithItems.height))
        self.boxWithItems.bind(minimum_height=self.boxWithItems.setter('height'))
        # Add the box layout to the scroll view
        self.itemScroll.add_widget(self.boxWithItems)

        self.addItemButton = TransparentButton(text = "add item", on_release = lambda btn: self.addItem(), size_hint_y = 0.1)
        self.addItemButton.disabled = True

        self.screenBox.add_widget(self.itemScroll)
        self.screenBox.add_widget(self.addItemButton)
    
    def areaChanged(self, spinner, text):
        """when the area changes update all items on screen"""
        if not super().areaChanged(spinner, text):
            self.addItemButton.disabled = True
            return
        self.items = self.manager.currentArea.items
        self.areaObject = self.manager.currentArea
        self.updateItems()
        self.addItemButton.disabled = False

    def updateItems(self):
        self.clearLayout()
        for itemName, itemObject in self.items.items():
            self.boxWithItems.add_widget(ItemBox(itemObject, size_hint_y = None))

    def clearLayout(self):
        self.boxWithItems.clear_widgets()

    def addItem(self):
        dialog = AddItemDialog(self.addItemToGame)
        dialog.open()
    
    def addItemToGame(self, itemObject) -> bool:
        logger.debug(f"adding {itemObject.name} to {self.areaObject.name}")
        if not self.areaObject.addItem(itemObject):
            return 0
        
        itemObject.area = self.areaObject
        self.updateItems()
        return 1


    



    



        
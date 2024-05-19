from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

import os


class ExpandableBox(BoxLayout):
    def __init__(self, header: Widget, content: Widget, button = None, **kwargs):
        """internal use only for trainer, item and encounter boxes, supply content and header. header must be a button or boxlayout. 
        Use the button parameter to provide a reference to the button, open call will be binded to it automatically"""
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.opened = False
        self.headerY = 0.999
        self.contentY = 0.001

        self.header = header
        self.content = content
        self.button = button 
        self.checkHeader()

        #box that will contain the content
        self.contentBox = BoxLayout(size_hint_y = self.contentY)

        self.add_widget(self.header)
        self.add_widget(self.contentBox)
    
    def checkHeader(self) -> None:
        if isinstance(self.header, Button):
            print("header is button, appending function")
            self.header.on_release = self.open
        elif isinstance(self.header, BoxLayout):
            print("header is Boxlayout")
            if self.button != None:
                print("button provided, appending open function")
                self.button.on_release = self.open
            else:
                print("adding button")
                bttn = Button(text = "open", on_release = self.open, size_hint_y = self.headerY)
                self.header.add_widget(bttn)
    
    def adjustSizes(self, headerSize : float, contentSize: float, size_hint_y: float, increase: bool = True):
        """adjust the sizes of contentBox and header to open or close the box"""
        self.header.size_hint_y = headerSize
        self.contentBox.size_hint_y = contentSize
        if increase:
            self.size_hint_y += size_hint_y
            return
        self.size_hint_y -= size_hint_y

    def open(self, instance = None) -> None:
        """open the Box showing the content"""
        #reverse opened, starts at False
        self.opened = not self.opened 
        if not self.opened:
            self.close()
            return
        self.adjustSizes(0.2, 0.8, 5)
        self.contentBox.add_widget(self.content)

    def close(self) -> None:
        """removes content from contentBox, then changes sizes to make contentBox disappear"""
        self.contentBox.clear_widgets()
        self.adjustSizes(self.headerY, self.contentY, 5, False)
    
    def isOpened(self) -> bool:
        return self.opened

class ExpandableTrainerBox(ExpandableBox):
    def __init__(self, trainerObject, **kwargs):
        self.button = None
        header = self.createHeader()
        content = BoxLayout(orientation = "vertical")

        super().__init__(header = header, content = content, button = self.button, **kwargs)

    def createHeader(self) -> Widget:
        """creates and returns header, also creates self.button"""
        #TODO add edit trainer button
        header = BoxLayout(orientation = "horizontal")
        nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
        nameLabel = Label(text = "Morty", size_hint_y = 0.2)
        trainerPic = os.path.join(os.getcwd(), "PokemonNuzlockeTracker", "localTesting", "swipeTest", "sprite.png")
        trainerImage = Image(source = trainerPic, fit_mode = "contain", pos_hint = {"left": 1})
        self.button = Button(text = "show trainer's pokemon")

        nameImageBox.add_widget(trainerImage)
        nameImageBox.add_widget(nameLabel)


        header.add_widget(nameImageBox)
        header.add_widget(self.button)
        return header
    
    def createContent(self) -> Widget:
        return
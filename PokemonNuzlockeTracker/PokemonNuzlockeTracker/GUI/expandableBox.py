from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image

import os
from loggerConfig import logger
from pokemonDialog import AddPokemonDialog


class ExpandableBox(BoxLayout):
    def __init__(self, header: Widget, content: Widget, button: None | Button = None, **kwargs):
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
            logger.debug("header is button, appending function")
            self.header.on_release = self.open
        elif isinstance(self.header, BoxLayout):
            logger.debug("header is Boxlayout")
            if self.button != None:
                logger.debug("button provided, appending open function")
                self.button.on_release = self.open
            else:
                logger.debug("adding button")
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
            logger.debug("closing")
            self.close()
            return
        logger.debug("opening")
        self.adjustSizes(0.2, 0.8, 5)
        self.updateContent()

    def close(self) -> None:
        """removes content from contentBox, then changes sizes to make contentBox disappear"""
        self.contentBox.clear_widgets()
        self.adjustSizes(self.headerY, self.contentY, 5, False)
    
    def isOpened(self) -> bool:
        return self.opened

    def updateContent(self) -> None:
        logger.debug("updating content")

class ExpandableTrainerBox(ExpandableBox):
    def __init__(self, trainerObject, **kwargs):
        self.button = None
        self.trainerObject = trainerObject
        header = self.createHeader()
        content = self.createContent()

        super().__init__(header = header, content = content, button = self.button, **kwargs)

    def createHeader(self) -> Widget:
        """creates and returns header, also creates self.button"""
        #TODO add edit trainer button
        nameLabel = Label(text = self.trainerObject.name, size_hint_y = 0.2)
        trainerPic = os.path.join(os.getcwd(), "../","localTesting", "swipeTest", "sprite.png")
        trainerImage = Image(source = trainerPic, fit_mode = "contain", pos_hint = {"left": 1})
        self.button = Button(text = f"show {self.trainerObject.name}'s pokemon")

        nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
        nameImageBox.add_widget(trainerImage)
        nameImageBox.add_widget(nameLabel)

        header = BoxLayout(orientation = "horizontal")
        header.add_widget(nameImageBox)
        header.add_widget(self.button)

        return header
    
    def createContent(self) -> Widget:
        content = BoxLayout(orientation = "vertical")
        pokemonAmount = len(self.trainerObject.pokemon)
        for pokemon in self.trainerObject.pokemon:
            content.add_widget(self.createPokemonBox(pokemon))
        #add button beneath pokemon
        if pokemonAmount < 6:  
            addPokemonButton = Button(text = f"Add pokemon to {self.trainerObject.name}", on_release = self.addPokemonPopup)  
            content.add_widget(addPokemonButton)
        #check for 5 pokemon as the last slot will be used for the button
        for emptySpace in range(5 - pokemonAmount):
            content.add_widget(Label())

        return content

    def addPokemonPopup(self, instance):
        dia = AddPokemonDialog(self.trainerObject, self)
        dia.open()
    
    def createPokemonBox(self, pokemonObject):
        #TODO class
        
        defeatedButton = Button(background_color = "green" if pokemonObject.defeated else "red", size_hint_x = 0.1)
        pokemonImage = Image(source = os.path.join(os.getcwd(), "../", "images", "sprites", "pokemonMinimalWhitespace", f"{pokemonObject.name.lower()}.png"), fit_mode = "contain", size_hint_x = 0.2)
        pokemonName = Label(text = pokemonObject.name)
        pokemonLevel = Label(text = f"Lv. {pokemonObject.level}")
        pokemonAbility = Label(text = f"{pokemonObject.ability}")
        pokemonHeldItem = Label(text = f"{pokemonObject.heldItem}")

        typingBox = BoxLayout(orientation = "horizontal")
        typingBox.add_widget(Label(text = "todo"))

        pokemonInfoBox = BoxLayout(orientation = "vertical", size_hint_x = 0.2)
        pokemonInfoBox.add_widget(pokemonName)
        pokemonInfoBox.add_widget(pokemonLevel)
        pokemonInfoBox.add_widget(typingBox)

        pokemonInfoBox2 = BoxLayout(orientation = "vertical", size_hint_x = 0.2)
        pokemonInfoBox2.add_widget(pokemonAbility)
        pokemonInfoBox2.add_widget(pokemonHeldItem)


        pokemonMoves = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
        for index in range(4):
            try: 
                move = pokemonObject.moves[index]
            except IndexError as e:
                move = ""

            pokemonMoves.add_widget(Label(text = move))

        pokemonBox = BoxLayout(orientation = "horizontal")
        pokemonBox.add_widget(defeatedButton)
        pokemonBox.add_widget(pokemonImage)
        pokemonBox.add_widget(pokemonInfoBox)
        pokemonBox.add_widget(pokemonInfoBox2)
        pokemonBox.add_widget(pokemonMoves)
        return pokemonBox

    def updateContent(self) -> None:
        self.contentBox.clear_widgets()
        self.contentBox.add_widget(self.createContent())




# def showGlobalView(self):
    #     if len(self.currentTrainerObject.pokemon) == 0:
    #         #add new pokemon by showing empty detailedpokemonBox
    #         # addPokemonLabel = Label(text = "No pokemon found", size_hint_y = 0.6)
    #         # addPokemonButton = Button(text = "add pokemon", on_press = self.addFirstPokemon, size_hint_y = 0.4)
    #         # self.trainerBox.add_widget(addPokemonLabel)
    #         # self.trainerBox.add_widget(addPokemonButton)
    #         return
        
    #     for index, pokemonObject in enumerate(self.currentTrainerObject.pokemon):
    #         #gather pokemon data and put it in Labels
    #         pokemonBox = BoxLayout(orientation = "horizontal", size_hint_y = (1 - 0.05)/ (len(self.currentTrainerObject.pokemon)), padding = (0, 0, 0, 10))
    #         #create Image with name underneath
    #         imageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
    #         pokemonImage = Image(source = os.path.join(self.spriteFolder, f"{pokemonObject.name.lower()}.png"))
    #         pokemonImage.fit_mode = "contain"
    #         nameLevelLabel = MDLabel(text = f"{pokemonObject.name} lvl {pokemonObject.level}", color = self.standardColor, pos_hint = {"right": 1})
            
    #         itemAbilityBox = BoxLayout(orientation = "vertical", size_hint_x = 0.1)
    #         abilityInput = MDLabel(text = f"{pokemonObject.ability}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"top" : 1})
    #         heldItemInput = MDLabel(text = f"{pokemonObject.heldItem}", color = self.standardColor, size_hint_y = 0.5, pos_hint = {"bottom" : 1})
            
    #         moveBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)

    #         for moveIndex in range(4): 
    #             moveSlot = MDLabel(text = f"Not revealed", color = self.standardColor)
    #             if moveIndex < len(pokemonObject.moves):
    #                 moveSlot.text = f"{pokemonObject.moves[moveIndex]}"
    #             moveBox.add_widget(moveSlot)

    #         imageBox.add_widget(pokemonImage)
    #         imageBox.add_widget(nameLevelLabel)
    #         pokemonBox.add_widget(imageBox)

    #         itemAbilityBox.add_widget(abilityInput)
    #         itemAbilityBox.add_widget(heldItemInput)

    #         pokemonBox.add_widget(itemAbilityBox)
    #         pokemonBox.add_widget(moveBox)
        
    #         self.trainerBox.add_widget(pokemonBox)
    #     logger.debug("created global view")
    
    # def showDetailedView(self):
    #     self.detailedPokemonBox.buildLayout(self.currentTrainerObject)
    #     self.trainerBox.add_widget(self.detailedPokemonBox)

    # def editTrainer(self, *args):
    #     """gives trainerobject to self.editTrainerBox for editing"""
    #     logger.debug(f"editing {self.currentTrainerObject.name}")
    #     self.editTrainerBox.buildLayout(self.currentTrainerObject)
    #     #clear the previous layout
    #     self.clearTrainerBox()
    #     #show new layout
    #     self.trainerBox.add_widget(self.editTrainerBox)
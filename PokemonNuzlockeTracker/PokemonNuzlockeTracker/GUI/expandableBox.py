from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from transparentButton import TransparentButton

import os
from loggerConfig import logger
from pokemonDialog import AddPokemonDialog
from detailedPokemonBox import DetailedPokemonBox
from games import pokemonSprites, trainerSprites, itemSprites


# class ExpandableBox(BoxLayout):
#     pass

class ExpandableBox(BoxLayout):
    def __init__(self, header: Button | BoxLayout, content: Widget, button: None | Button = None, **kwargs):
        """supply content and header. header must be a button or boxlayout. 
        Use the button parameter to provide a reference to the button, open call will be binded to it automatically
        set headerClose, headerOpen and contentOpen in child class otherwise defaults to default heights"""
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.opened = False

        #set height to standard values or values already defined, TODO settings for standard
        self.headerClosed = self.headerClosed if hasattr(self, 'headerClosed') else 150
        self.contentClosed = 1
        self.headerOpen = self.headerOpen if hasattr(self, "headerOpen") else 100

        #TODO dynamically calculate based on content height
        self.contentOpen = self.contentOpen if hasattr(self, "contentOpen") else 600

        self.header = header
        self.header.size_hint_y = None
        self.header.height = self.headerClosed

        self.button = button
        self.content = content
        #box that will contain the content
        self.contentBox = BoxLayout()
        self.contentBox.size_hint_y = None
        self.contentBox.height = self.contentClosed

        self.size_hint_y = None
        self.height = self.headerClosed + self.contentClosed
        self.checkHeader()

        self.add_widget(self.header)
        self.add_widget(self.contentBox)
    
    def checkHeader(self) -> None:
        #TODO error handling, label
        #or change header to boxlayout if not already boxlayout
        if isinstance(self.header, Button):
            # logger.debug("header is button, appending function")
            self.header.on_release = self.open
        elif isinstance(self.header, BoxLayout):
            # logger.debug("header is Boxlayout")
            if self.button != None:
                # logger.debug("button provided, appending open function")
                self.button.on_release = self.open
            else:
                # logger.debug("adding button")
                bttn = Button(text = "open", on_release = self.open)
                self.header.add_widget(bttn)
        else:
            logger.critical(f"header provided is not a button or boxlayout")
            exit(2)
    
    def adjustSizes(self, headerSize : float, contentSize: float):
        """adjust the sizes of contentBox and header to open or close the box"""
        self.header.height = headerSize
        self.contentBox.height = contentSize
        self.height = headerSize + contentSize

    def open(self, instance = None) -> None:
        """open the Box showing the content"""
        #reverse opened, starts at False
        self.opened = not self.opened 
        if not self.opened:
            # logger.debug("closing")
            self.close()
            return
        # logger.debug("opening")
        self.adjustSizes(self.headerOpen, self.contentOpen)
        self.updateContent()

    def close(self) -> None:
        """removes content from contentBox, then changes sizes to make contentBox disappear"""
        self.contentBox.clear_widgets()
        self.adjustSizes(self.headerClosed, self.contentClosed)

    def updateContent(self) -> None:
        logger.debug("updating content")
        self.contentBox.clear_widgets()
        self.contentBox.add_widget(self.createContent())
        #resize widget as the add_widget does not update the size of the area given
        self.adjustSizes(self.headerOpen, self.contentOpen)
    
    def updateHeader(self) -> None:
        logger.debug("updating Header")
        self.header.clear_widgets()
        self.header.add_widget(self.createHeader())
    
    def createContent(self) -> Widget:
        """meant for override by child classes but used by updateContent
        Content height should be defined in this function,"""
        return BoxLayout()

    def createHeader(self) -> Widget:
        """used in child classes"""
        return BoxLayout()

class ExpandableTrainerBox(ExpandableBox):
    def __init__(self, trainerObject, **kwargs):
        """works with height and width rather than size_hint"""
        self.trainerObject = trainerObject
        #add updateHeader to the observer list so it gets called when defeated changes
        self.trainerObject.addDefeatedObserver(self.updateHeader)
        self.headerClosed = 300
        self.headerOpen = 300
        header = self.createHeader()
        content = self.createContent()

        super().__init__(header = header, content = content, button = self.button, **kwargs)

    def createHeader(self) -> Widget:
        """creates and returns header, also creates self.button"""
        #TODO add edit trainer button
        nameButton = TransparentButton(text = self.trainerObject.name, size_hint_y = 0.3, on_release = lambda btn: self.trainerObject.removeTrainer())
        trainerPic = os.path.join(trainerSprites, f"{self.trainerObject.trainerType}.png" if self.trainerObject.trainerType is not None else "hiker.png")
        trainerImage = Image(source = trainerPic, fit_mode = "contain", pos_hint = {"left": 1}, size_hint_y = 0.7)
        self.button = TransparentButton(text = f"show {self.trainerObject.name}'s pokemon")
        #change button color based on defeated status of trainer
        self.button.greenColor() if self.trainerObject.defeated else self.button.redColor()

        nameImageBox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
        nameImageBox.add_widget(trainerImage)
        nameImageBox.add_widget(nameButton)

        header = BoxLayout(orientation = "horizontal")
        header.add_widget(nameImageBox)
        header.add_widget(self.button)

        return header
    
    def createContent(self) -> Widget:
        content = GridLayout(cols = 1, size_hint_y = None)
        contentScroller = ScrollView(size = (content.width, content.height))
        content.bind(minimum_height = content.setter("height"))
        pokemonAmount = len(self.trainerObject.pokemon)
        self.contentOpen = 0
        for pokemon in self.trainerObject.pokemon:
            pokemonBox = ExpandablePokemonBox(pokemon, self)
            content.add_widget(pokemonBox)
            self.contentOpen += pokemonBox.headerClosed + 1 #contentclosed is 1

        #add button beneath pokemon
        if pokemonAmount < 6:  
            addPokemonButton = TransparentButton(text = f"Add pokemon to {self.trainerObject.name}", on_release = self.addPokemonPopup, size_hint_y = None) 
            content.add_widget(addPokemonButton)
            self.contentOpen += 300

        contentScroller.add_widget(content)
        return contentScroller

    def addPokemonPopup(self, instance):
        dia = AddPokemonDialog(self.trainerObject, self)
        dia.open()

class ExpandablePokemonBox(ExpandableBox):
    def __init__(self, pokemonObject, trainerBox, **kwargs):
        self.pokemonObject = pokemonObject
        self.trainerBox = trainerBox
        self.headerClosed = 250
        self.headerOpen = 250
        self.contentOpen = 700

        header = self.createHeader()
        content = self.createContent()
        super().__init__(header = header, content = content, button = self.pokemonName, **kwargs)
    
    def createHeader(self) -> Widget:
        header = BoxLayout(orientation = "horizontal")
        defeatedButton = TransparentButton(size_hint_x = 0.1, on_release = lambda btn: [self.changeDefeated(btn), self.trainerBox.updateHeader()], background_color = "white")
        #change button color
        self.changeWidgetColor(defeatedButton)
        pokemonImage = Image(source = os.path.join(pokemonSprites, f"{self.pokemonObject.name.lower()}.png"), fit_mode = "contain", size_hint_x = 0.2)

        self.pokemonName = TransparentButton(text = self.pokemonObject.name)
        pokemonLevel = Label(text = f"Lv. {self.pokemonObject.level}")
        pokemonAbility = Label(text = f"{self.pokemonObject.ability}")
        pokemonHeldItem = Label(text = f"{self.pokemonObject.heldItem}")

        typingBox = BoxLayout(orientation = "horizontal")
        typingBox.add_widget(Label(text = "todo"))

        pokemonInfoBox = BoxLayout(orientation = "vertical", size_hint_x = 0.2)
        pokemonInfoBox.add_widget(self.pokemonName)
        pokemonInfoBox.add_widget(pokemonLevel)
        pokemonInfoBox.add_widget(typingBox)

        pokemonInfoBox2 = BoxLayout(orientation = "vertical", size_hint_x = 0.2)
        pokemonInfoBox2.add_widget(pokemonAbility)
        pokemonInfoBox2.add_widget(pokemonHeldItem)

        pokemonMoves = BoxLayout(orientation = "vertical", size_hint_x = 0.3)
        for index in range(4):
            try: 
                move = self.pokemonObject.learnedMoves[index]
            except IndexError as e:
                move = ""
            pokemonMoves.add_widget(Label(text = move))

        header.add_widget(defeatedButton)
        header.add_widget(pokemonImage)
        header.add_widget(pokemonInfoBox)
        header.add_widget(pokemonInfoBox2)
        header.add_widget(pokemonMoves)
        return header

    def createContent(self) -> Widget:
        content = DetailedPokemonBox(self.pokemonObject, self.updateHeader, self.trainerBox.updateContent)
        return content

    def changeDefeated(self, instance) -> None:
        """changes pokemon defeated status"""
        self.pokemonObject.changeDefeated()
        #change button colour
        self.changeWidgetColor(instance)
    
    def changeWidgetColor(self, widget):
        """changes button color to green or red based on pokemon defeated status"""
        widget.greenColor() if self.pokemonObject.defeated else widget.redColor()

    def updateHeader(self) -> None:
        super().updateHeader()
        self.button = self.pokemonName
        self.checkHeader()

    
class EncounterTypeBox(ExpandableBox):
    def __init__(self, encounterType, encounters, **kwargs):
        """encounters is a dict of encounterType: encounters"""
        self.encounterType = encounterType
        self.encounters = encounters
        header = self.createHeader()
        content = self.createContent()
        super().__init__(header, content, button = self.openButton, **kwargs)
    
    def createHeader(self) -> Widget:
        self.openButton = TransparentButton(text = self.encounterType)
        return self.openButton

    def createContent(self) -> Widget:
        content = BoxLayout(orientation = "vertical")
        for encounter in self.encounters:
            content.add_widget(EncounterBox(encounter))
        return content
    

class EncounterBox(BoxLayout):
    #TODO get from central point
    def __init__(self, pokemonObject, *args, **kwargs):
        """expects pokemonObject"""
        super().__init__(*args, **kwargs)
        self.pokemonObject = pokemonObject
        self.orientation = "horizontal"
        self.catchButton = TransparentButton(text = "catch", on_press = self.catch, size_hint_x = 0.2)
        image = os.path.join(pokemonSprites, f"{pokemonObject.name.lower()}.png")
        self.pokemonImage = Image(source = image, pos_hint = {"top": 1}, size_hint_x = 0.2)
        self.pokemonImage.fit_mode = "contain"
        self.infoBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        self.percentageLabel = Label(text = f"percentage: {pokemonObject.percentage}")
        self.levelsLabel = Label(text = f"levels: {pokemonObject.levels}")
        self.moreInfoButton = TransparentButton(text = "more info", on_press = self.showMoreInfo, size_hint_x = 0.2)
        
        self.infoBox.add_widget(self.percentageLabel)
        self.infoBox.add_widget(self.levelsLabel)

        self.add_widget(self.catchButton)
        self.add_widget(self.pokemonImage)
        self.add_widget(self.infoBox)
        self.add_widget(self.moreInfoButton)

    def catch(self, button):
        logger.debug(f"catching {self.pokemonObject.name}, TODO")
    
    def showMoreInfo(self, button):
        logger.debug(f"show more info, TODO")

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
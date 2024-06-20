from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from transparentButton import TransparentButton

from collections.abc import Callable

import os
from loggerConfig import logger
from pokemonDialog import AddPokemonDialog
from detailedPokemonBox import DetailedPokemonBox
from editTrainerBox import EditTrainerBox
from games import pokemonSprites, itemSprites, getTrainerSprite


# class ExpandableBox(BoxLayout):
#     pass

class ExpandableBox(BoxLayout):
    def __init__(self, header: Button | BoxLayout, button: None | Button = None, **kwargs):
        """supply header. header must inherit from ButtonBehaviour or be a boxlayout. 
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
        """add open functionality to given button or add own button with open functionality"""
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
        if self.opened:
            logger.debug("closing")
            self.close()
            return
        logger.debug("opening")
        self.adjustSizes(self.headerOpen, self.contentOpen)
        self.updateContent()
        self.opened = True

    def close(self) -> None:
        """removes content from contentBox, then changes sizes to make contentBox disappear"""
        self.contentBox.clear_widgets()
        self.adjustSizes(self.headerClosed, self.contentClosed)
        self.opened = False

    def updateContent(self, content = None) -> None:
        """give content function that returns a widget with the content"""
        if content == None:
            content = self.createContent
        logger.debug("updating content")
        self.contentBox.clear_widgets()
        self.contentBox.add_widget(content())
        #resize widget as the add_widget does not update the size of the area given
        self.adjustSizes(self.headerOpen, self.contentOpen)
    
    def updateHeader(self) -> None:
        logger.debug("updating Header")
        self.header.clear_widgets()
        self.header.add_widget(self.createHeader())
        self.checkHeader()
    
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
        self.trainerObject.addAttributeObserver(self.updateHeader)
        self.trainerObject.addDefeatedObserver(self.updateHeader)
        self.headerClosed = 300
        self.headerOpen = 200
        header = self.createHeader()
        #used for showing trainer content
        self.showingTrainer = False

        super().__init__(header = header, button = self.button, **kwargs)

    def createHeader(self) -> Widget:
        """creates and returns header, also creates self.button"""
        #TODO add edit trainer button to Image with buttonbehaviour
        nameButton = TransparentButton(text = self.trainerObject.name, size_hint_y = 0.3, on_release = lambda btn: self.showTrainerContent())
        trainerPic = getTrainerSprite(self.trainerObject.trainerType)
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
            pokemonBox = ExpandableTrainerPokemonBox(pokemon)
            content.add_widget(pokemonBox)
            pokemon.addRemoveObserver(self.updateContent)
            self.contentOpen += pokemonBox.headerClosed + 1 #contentclosed is 1

        #add button beneath pokemon
        if pokemonAmount < 6:  
            addPokemonButton = TransparentButton(text = f"Add pokemon to {self.trainerObject.name}", on_release = self.addPokemonPopup, size_hint_y = None, height = 200) 
            content.add_widget(addPokemonButton)
            #*3 dirty for phone
            self.contentOpen += 200 * (6 - pokemonAmount)

        contentScroller.add_widget(content)
        return contentScroller

    def createEditTrainerContent(self):
        trainerContent = EditTrainerBox(self.trainerObject)
        return trainerContent

    def showTrainerContent(self):
        #content is already opened
        if self.opened:
            #show trainer details
            if not self.showingTrainer:
                self.updateContent(self.createEditTrainerContent)
                self.showingTrainer = True
                return
            #close content
            self.close()
            self.showingTrainer = False
            return
        #show trainer details
        self.open()
        self.updateContent(self.createEditTrainerContent)
        self.showingTrainer = True
        return

    def addPokemonPopup(self, instance):
        dia = AddPokemonDialog(self.trainerObject, self)
        dia.open()

class ExpandableTrainerPokemonBox(ExpandableBox):
    def __init__(self, pokemonObject, **kwargs):
        self.pokemonObject = pokemonObject
        self.pokemonObject.addAttributeObserver(self.updateHeader)
        self.headerClosed = 250
        self.headerOpen = 250
        self.contentOpen = 900

        header = self.createHeader()
        super().__init__(header = header, button = self.pokemonName, **kwargs)
    
    def createHeader(self) -> Widget:
        header = BoxLayout(orientation = "horizontal")
        defeatedButton = TransparentButton(size_hint_x = 0.1, on_release = lambda btn: [self.changeDefeated(btn)], background_color = "white")
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
        content = DetailedPokemonBox(self.pokemonObject)
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
        super().__init__(header, button = self.openButton, **kwargs)
    
    def createHeader(self) -> Widget:
        self.openButton = TransparentButton(text = self.encounterType)
        return self.openButton

    def createContent(self) -> Widget:
        content = GridLayout(cols = 1, size_hint_y = None)
        contentScroller = ScrollView(size = (content.width, content.height))
        content.bind(minimum_height = content.setter("height"))

        self.contentOpen = 0
        for encounter in self.encounters:
            encounterBox = ExpandableEncounterPokemonBox(encounter)
            content.add_widget(encounterBox)
            self.contentOpen += encounterBox.contentOpen + 1
        contentScroller.add_widget(content)
        return contentScroller

class ExpandableEncounterPokemonBox(ExpandableBox):
    def __init__(self, pokemonObject, **kwargs):
        self.pokemonObject = pokemonObject
        self.contentOpen = 200
        header = self.createHeader()

        super().__init__(header = header, button = self.moreInfoButton, **kwargs)

    def createHeader(self) -> Widget:
        header = BoxLayout(orientation = "horizontal")
        catchButton = TransparentButton(text = "catch", on_press = self.catch, size_hint_x = 0.2)

        image = os.path.join(pokemonSprites, f"{self.pokemonObject.name.lower()}.png")
        pokemonImage = Image(source = image, pos_hint = {"top": 1}, size_hint_x = 0.2)
        pokemonImage.fit_mode = "contain"
        infoBox = BoxLayout(orientation = "vertical", size_hint_x = 0.4)
        percentageLabel = Label(text = f"percentage: {self.pokemonObject.percentage}")
        levelsLabel = Label(text = f"levels: {self.pokemonObject.levels}")
        self.moreInfoButton = TransparentButton(text = "more info", size_hint_x = 0.2)

        infoBox.add_widget(percentageLabel)
        infoBox.add_widget(levelsLabel)

        header.add_widget(catchButton)
        header.add_widget(pokemonImage)
        header.add_widget(infoBox)
        header.add_widget(self.moreInfoButton)

        return header

    def createContent(self) -> Widget:
        content = BoxLayout()
        return content

    def catch(self, btn):
        pass

    

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
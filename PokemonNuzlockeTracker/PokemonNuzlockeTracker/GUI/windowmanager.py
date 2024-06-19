from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock

from trainerScreen import TrainerScreen
from attemptInfoScreen import AttemptInfoScreen
from encounterScreen import EncounterScreen
from itemScreen import ItemScreen
from pokemonInfoScreen import PokemonInfoScreen

import os
from pympler import asizeof
import subprocess

from loggerConfig import logger
import games as gm
from trainer import Trainer
from pokemon import TrainerPokemon

class WindowManager(ScreenManager):

    def __init__(self, os, **kwargs):
        super().__init__(**kwargs)
        self.os = os
        #global game object
        self._gameObject = None
        self.areaList = None
        #gets replaced with the area object as soon as it is chosen
        self._currentArea = None

        self._screenNumber = 0
        self.screenList = []

        Clock.schedule_interval(self.updateObject, 5)


    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self, gameObject):
        self._gameObject = gameObject
        self.areaList = self._gameObject.areaList
    
    @property
    def screenNumber(self):
        return self._screenNumber
    
    @screenNumber.setter
    def screenNumber(self, number):
        self._screenNumber = number
        self.updateScreen()

    def updateScreen(self):
        screenNumber = self.screenNumber % len(self.screenList)
        self.current = self.screenList[screenNumber].name

    @property
    def currentArea(self):
        return self._currentArea
    
    @currentArea.setter
    def currentArea(self, newAreaName):
        """function expects a name, retrieves the AreaObject from the corresponding name"""
        for areaObject in self.areaList:
            if areaObject.name == newAreaName:
                self._currentArea = areaObject
                logger.debug(f"found {newAreaName} in areaList")
                break
        else:
            logger.error(f"{newAreaName} could not be loaded, not found in areaList")
            return
        logger.debug(f"{self._currentArea.name} Object loaded in manager")
    
    def addPokemonToArea(self, pokemonObject, areaName):
        """add pokemon to encounters list of specified areaName"""
        for area in self.areaList:
            if area.name == areaName:
                area.encounters = pokemonObject
                logger.info(f"added {pokemonObject.name} to {areaName}")
                return 1
        else:
            logger.error(f"{pokemonObject.name} could not be added to {areaName}")
            return 0
    
    def addPokemonToArena(self, pokemonObject) -> None:
        self.addPokemonToArea(pokemonObject, "Arena")

    def addPokemonToRetirement(self, pokemonObject) -> None:
        self.addPokemonToArea(pokemonObject, "Retirement")

    def addPokemonToLostAndFound(self, pokemonObject) -> None:
        self.addPokemonToArea(pokemonObject, "lost&found")

    def startPokemonGame(self, gameObject):
        self.gameObject = gameObject
        attemptInfoScreen = AttemptInfoScreen(name = "attemptInfoScreen", screenName = "Info on current attempt")
        trainerScreen = TrainerScreen(name = "trainerScreen", screenName = "Trainer Screen")
        encounterScreen = EncounterScreen(name = "encounterScreen", screenName = "Encounter Screen")
        itemScreen = ItemScreen(name = "itemScreen", screenName = "Item Screen")
        pokemonInfoScreen = PokemonInfoScreen(name = "pokemonInfoScreen", screenName = "Pokemon Info Screen")

        self.add_widget(trainerScreen)
        self.add_widget(attemptInfoScreen)
        self.add_widget(encounterScreen)
        self.add_widget(itemScreen)
        self.add_widget(pokemonInfoScreen)
        #attempt info screen as first so it has index 0
        self.screenList = [attemptInfoScreen, trainerScreen, encounterScreen, itemScreen, pokemonInfoScreen]
        self.current = attemptInfoScreen.name
    
    def closePokemonGame(self):
        """reset all variables and remove widgets from windowManager"""
        for screen in self.screenList:
            self.remove_widget(screen)
        self.screenList = []
        self.current = "selectGameScreen"
        #bypass setter as we don't want to update the current screen
        self._currentArea = None
        self._screenNumber = 0
        self._gameObject = None
        self.areaList = None
    
    # Function to get memory usage of the current process
    def get_memory_usage(self):
        if self.os == "Windows":
            import psutil
            
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
        else:
            process = subprocess.Popen(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)
            stdout, _ = process.communicate()
            meminfo = stdout.decode('utf-8')
            lines = meminfo.split('\n')
            for line in lines:
                # print(line)
                if line.startswith("Active"):
                    return int(line.split()[1]) * 100
            # return meminfo
        return memory_info.rss  # Resident Set Size: total memory used by the process

    def calculate_memory_usage(self, obj):
        return asizeof.asizeof(obj)
    
    def bytesToMB(self, bytes):
        return int(bytes) / (10**6)
    
    def updateObject(self, dt) -> None:
        totalMem = round(self.bytesToMB(self.get_memory_usage()), 1)
        string = f"total: {totalMem}"
        if self.gameObject != None:
            gameMem = round(self.bytesToMB(self.calculate_memory_usage(self.gameObject)), 1)
            string += f", game: {gameMem}"
        print(string)
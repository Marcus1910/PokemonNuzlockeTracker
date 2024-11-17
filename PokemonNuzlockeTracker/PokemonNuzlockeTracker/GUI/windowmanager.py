from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock

import os
from pympler import asizeof
import subprocess

from .trainerScreen import TrainerScreen
from .attemptInfoScreen import AttemptInfoScreen
from .encounterScreen import EncounterScreen
from .itemScreen import ItemScreen
from .pokemonInfoScreen import PokemonInfoScreen

from loggerConfig import logger
import Logic.games as gm

class WindowManager(ScreenManager):

    def __init__(self, os, **kwargs):
        super().__init__(**kwargs)
        self.os = os

        self._attemptRecord = None
        self._locationList = []
        self._locationRecord = None

        self._screenNumber = 0
        self.screenList = []
        # Clock.schedule_interval(self.updateObject, 5)

    @property
    def attemptRecord(self):
        return self._attemptRecord
    
    @attemptRecord.setter
    def attemptRecord(self, attemptRecord):
        self._attemptRecord = attemptRecord
        self.refreshLocationList()
        #MDApp.get_running_app().game = self._gameObject

    @property
    def locationRecord(self):
        return self._locationRecord
    
    @locationRecord.setter
    def locationRecord(self, locationName):
        """uses the locationName and IDGame to get the correct locationRecord"""
        self.fileRetriever.getLocationRecord(locationName, self.attemptRecord.IDGame)  
    
    @property
    def locationList(self):
        return self._locationList
    
    @locationList.setter
    def locationList(self, locationList: list[str]):
        self._locationList = locationList
    
    def refreshLocationList(self):
        self.locationList = self.fileRetriever.getLocationNames(self.attemptRecord.IDGame)
        
    
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

    def startPokemonGame(self, attemptRecord, fileRetriever):
        self.fileRetriever = fileRetriever
        self.attemptRecord = attemptRecord
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
        self._locationRecord = None
        self._screenNumber = 0
        self._attemptRecord = None
        self.locationList = []
    
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
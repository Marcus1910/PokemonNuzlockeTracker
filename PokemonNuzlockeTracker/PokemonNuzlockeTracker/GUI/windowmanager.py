from kivy.uix.screenmanager import ScreenManager

from loggerConfig import logger
import games as gm
from trainer import Trainer
from pokemon import TrainerPokemon

class WindowManager(ScreenManager):
    attempt = None
    #global game object
    _gameObject = None
    areaList = None
    #gets replaced with the area object as soon as it is chosen
    _currentArea = None

    _screenNumber = 0
    screenList = []

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
        self._screenNumber = number % len(self.screenList)
        self.current = self.screenList[self._screenNumber]

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

    
    def showError(self, text):
        pass
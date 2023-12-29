from kivy.uix.screenmanager import ScreenManager
from loggerConfig import logger
from trainer import Trainer
from trainerPokemon import TrainerPokemon

class WindowManager(ScreenManager):
    attempt = None
    #global game object
    _gameObject = None
    areaList = None
    #gets replaced with the area object as soon as it is chosen
    _currentArea = None

    _screenNumber= 0
    screenList = []

    

    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self, gameObject):
        self._gameObject = gameObject
        self.areaList = self._gameObject.retrieveGameData()
    
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
    def currentArea(self, areaName):
        """function expects a name, retrieves the AreaObject from the corresponding name"""
        for area in self.areaList:
            if area.name == areaName:
                self._currentArea = area
                break
        else:
            logger.error(f"{areaName} could not be loaded, not found in areaList")
        logger.debug(f"{self._currentArea.name} Object loaded in manager")
    
    def saveCurrentArea(self):
        """overwrite area object in areaList"""
        pass

    def updateCurrentArea(self):
        logger.info(f"updating area")
    
    def saveTrainer(self):
        trainer = Trainer("Maarten")
        politoed = TrainerPokemon("Politoed", 57)
        trainer.pokemon = politoed
        self.gameObject.areaList[0].addTrainer(trainer)
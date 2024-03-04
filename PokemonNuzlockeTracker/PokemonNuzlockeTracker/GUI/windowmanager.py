from kivy.uix.screenmanager import ScreenManager
from loggerConfig import logger
import games as gm
from trainer import Trainer
from trainerPokemon import TrainerPokemon

class WindowManager(ScreenManager):
    attempt = None
    #global game object
    _gameObject = None
    areaDict = None
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
        self.areaDict = self._gameObject.areaDict
    
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
        for areaObject in self.areaDict.values():
            if areaObject.name == newAreaName:
                self._currentArea = areaObject
                logger.debug(f"found {newAreaName} in areaDict")
                break
        else:
            logger.error(f"{newAreaName} could not be loaded, not found in areaDict")
            return
        logger.debug(f"{self._currentArea.name} Object loaded in manager")
    
    def saveCurrentArea(self):
        """overwrite area object in areaDict"""
        pass

    def updateCurrentArea(self):
        logger.info(f"updating area")
    
    def saveTrainer(self):
        trainer = Trainer("Maarten")
        politoed = TrainerPokemon("Politoed", 57)
        trainer.pokemon = politoed
        self.gameObject.areaDict[0].addTrainer(trainer)
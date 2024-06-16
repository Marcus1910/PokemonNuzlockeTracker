import json
from loggerConfig import logicLogger as logger
class BasePokemon():
    def __init__(self, name):
        """Minimum pokemon requirements, name, dexno and gender"""
        self._name = name.title()
        self._dexNo = None
        
        #used for display of moves that it can learn, lvl: move
        self._levelupMoves = {}
    
    #getters and setters
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name.title()

    @property
    def dexNo(self):
        return self._dexNo
    
    @dexNo.setter
    def dexNo(self, dexNo):
        self._dexNo = dexNo

    def storeToDataFile(self):
        """returns a dictionary consisting of the name, dexno and gender of the pokemon"""
        #TODO dexno needed, lookup json file pokemon changed and use dexno as ID?
        variableDict = {"_name": self.name, "_dexno": self.dexNo}
        return variableDict
    
    def __str__(self):
        returnString = f"name: {self._name}, dexNo: {self.dexNo}"
        return returnString

class Pokemon(BasePokemon):
    def __init__(self, name, level):
        super().__init__(name)
        self._level = level
        self._gender = None
        self._learnedMoves = []
        self._ability = None
        self._heldItem = None
    
    @property
    def level(self):
        return self._level
        
    @level.setter
    def level(self, level):
        self._level = level

    @property
    def gender(self):
        return self._gender
    
    @gender.setter
    def gender(self, gender):
        if gender is None:
            self._gender = None
        else:
            gender = str(gender).upper()
            if gender == "F" or gender == "M":
                self._gender = gender
            else:
                logger.error("enter valid gender, options are M or F")

    @property
    def learnedMoves(self):
        return self._learnedMoves
        
    @learnedMoves.setter
    def learnedMoves(self, move):
        if len(self.learnedMoves) < 4 and move not in self.learnedMoves:
            self._learnedMoves.append(move)
        else:
            logger.error("This pokemon already has this move")

    def deleteLearnedMove(self, move):
        #TODO return bool
        if move in self.learnedMoves:
            self.learnedMoves.remove(move)
            logger.info(f"removed {move} from {self._name}")
        else:
            logger.error(f"{self._name} has no move {move}")

    @property
    def ability(self):
        return self._ability
        
    @ability.setter
    def ability(self, ability):
        self._ability = ability

    @property
    def heldItem(self):
        return self._heldItem
        
    @heldItem.setter
    def heldItem(self, heldItem):
        self._heldItem = heldItem
    
    def storeToDataFile(self):
        variableDict = super().storeToDataFile()
        variableDict.update({"_level": self.level, "_learnedMoves": self.learnedMoves, "_ability": self.ability, "heldItem": self.heldItem, "gender": self._gender})
        return variableDict

class TrainerPokemon(Pokemon):
    #different class for future additions like health, pp, ai% of move chosen etc
    defaultDefeated = False
    def __init__(self, name, level, defeated = False):
        super().__init__(name, level)
        self._defeated = defeated #savefile
        self._trainer = None #internal use

    @property
    def defeated(self):
        return self._defeated
    
    @defeated.setter
    def defeated(self, bool):
        self._defeated = bool
    
    def changeDefeated(self):
        """change the defeated status of the pokemon, inverts it"""
        self.defeated = not self.defeated
        self.trainer.checkDefeated()
    
    @property
    def trainer(self):
        return self._trainer

    def trainer(self, trainerObject) -> bool:
        if trainerObject == None:
            logger.error(f"pokemon could not be added to trainer, trainer is not valid")
            return 0
        self._trainer = trainerObject
        logger.info(f"{self.name} added to {trainerObject.name}")
        return 1
    
    def storeToSaveFile(self):
        if self.defeated != self.defaultDefeated:
            variableDict = {"_name": self.name, "_defeated": self.defeated}
            return variableDict
        return None
    
    def __str__(self):
        parentStr = super().__str__()
        childStr = f", defeated: {self._defeated}"
        return parentStr + childStr

class PlayerPokemon(Pokemon):
    def __init__(self, name, level):
        """pokemon object caught by player"""
        super().__init__(name, level)
    
class EncounteredPokemon(BasePokemon):
    defaultCaptureStatus = 0
    
    def __init__(self, name, state = 0, percentage = "n/a", levels = "n/a"):
        """pokemon object used to display capture statuses"""
        super().__init__(name)
        self._captureStatus = state
        self._percentage = percentage
        self._levels = levels
    
    @property
    def captureStatus(self):
        return self._captureStatus

    @captureStatus.setter
    def captureStatus(self, state):
        self._captureStatus = state
    
    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        self._percentage = percentage

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, levels):
        #remove whitespace
        while " " in levels:
            levels = levels.replace(" ", "")
        if "\n" in levels:
            levels = levels.replace("\n", "")
        self._levels = levels
    
    def storeToDataFile(self):
        variableDict = super().storeToDataFile()
        variableDict.update({"_levels": self.levels, "_percentage": self.percentage})
        return variableDict

    # def storeToSaveFile(self):
    #     if self.captureStatus != self.defaultCaptureStatus:
    #         variableDict = {"_name": self.name, "_levels": self.levels, "_captureStatus": self.captureStatus, "_percentage": self.percentage}
    #         return variableDict
    #     return None
    

"""
example json encountered pokemon
"_encounteredPokemon": {
   "Shellder": {
    "_name": "Shellder",
    "_level": 1,
    "_dexNo": null,
    "_gender": null,
    "_moves": [],
    "_ability": null,
    "_heldItem": null,
    "_captureStatus": 2,
    "_percentage": "n/a",
    "_levels": "n/a"
   },
   "Chinchou": {
    "_name": "Chinchou",
    "_level": 1,
    "_dexNo": null,
    "_gender": null,
    "_moves": [],
    "_ability": null,
    "_heldItem": null,
    "_captureStatus": 1,
    "_percentage": "n/a",
    "_levels": "n/a"
   },
"""
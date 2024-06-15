import json
from loggerConfig import logicLogger as logger
class Pokemon():
    def __init__(self, name, level):
        self._name = name.title()
        self._level = level
        self._dexNo = None
        self._gender = None
        self._moves = []
        self._ability = None
        self._heldItem = None
    
    #getters and setters
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name.title()
    
    @property
    def level(self):
        return self._level
        
    @level.setter
    def level(self, level):
        self._level = level

    @property
    def dexNo(self):
        return self._dexNo
    
    @dexNo.setter
    def dexNo(self, dexNo):
        self._dexNo = dexNo

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
                print("enter valid gender, options are M or F")

    @property
    def moves(self):
        return self._moves
        
    @moves.setter
    def moves(self, move):
        if len(self._moves) < 4 and move not in self._moves:
            self._moves.append(move)
        else:
            print("This pokemon already has this move")
    #return something TODO
    def deleteMove(self, move):
        if move in self._moves:
            self._moves.remove(move)
            print(f"removed {move} from {self._name}")
        else:
            print(f"{self._name} has no move {move}")
        
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
        variableDict = {"_name": self.name, "_level": self.level, "_dexno": self.dexNo, "_gender": self.gender, "_moves": self.moves, "_ability": self.ability, "_heldItem": self.heldItem}
        return variableDict
    
    def __str__(self):
        returnString = f"name: {self._name}, dexNo: {self.dexNo}, gender: {self._gender}, level: {self._level}, moves: {self._moves}, ability: {self._ability}, held item: {self._heldItem}"
        return returnString

class TrainerPokemon(Pokemon):
    #different class for future additions like health, pp, ai% of move chosen etc
    defaultDefeated = False
    def __init__(self, name, level, defeated = False):
        self._defeated = defeated
        self._trainer = None
        super().__init__(name, level)
    
    @property
    def defeated(self):
        return self._defeated
    
    @defeated.setter
    def defeated(self, bool):
        self._defeated = bool
    
    def changeDefeated(self):
        """change the defeated status of the pokemon, inverts it"""
        self._defeated = not self._defeated
    
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
            variableDict = {"_name": self.name, "_moves": self.moves, "_defeated": self.defeated}
            return variableDict
        return None
    
    def __str__(self):
        parentStr = super().__str__()
        childStr = f", defeated: {self._defeated}"
        return parentStr + childStr
    
class EncounteredPokemon(Pokemon):
    defaultCaptureStatus = 0
    
    def __init__(self, name, level = 1, state = 0, percentage = "n/a", levels = "n/a"):
        super().__init__(name, level)
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
        self._levels = levels

    def storeToSaveFile(self):
        if self.captureStatus != self.defaultCaptureStatus:
            variableDict = {"_name": self.name, "_level": self.level, "_captureStatus": self.captureStatus, "_percentage": self.percentage}
            return variableDict
        return None
    

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
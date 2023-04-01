import json
class Pokemon():
    def __init__(self, name, level):
        self._name = name.title()
        self._level = level
        self._dexNo = None
        self._gender = None
        self._moves = []
        self._ability = None
        self._heldItem = None
    
    ##getters and setters
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
        returnString = f"name: {self._name}, gender: {self._gender}, level: {self._level}, moves: {self._moves}, ability: {self._ability}, held item: {self._heldItem}"
        return returnString

class TrainerPokemon(Pokemon):
    #different class for future additions like health, pp, ai% of move chosen etc
    defaultDefeated = False
    def __init__(self, name, level, defeated = False):
        self._defeated = defeated
        super().__init__(name, level)
    
    @property
    def defeated(self):
        return self._defeated
    
    @defeated.setter
    def defeated(self, bool):
        self._defeated = bool
    
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


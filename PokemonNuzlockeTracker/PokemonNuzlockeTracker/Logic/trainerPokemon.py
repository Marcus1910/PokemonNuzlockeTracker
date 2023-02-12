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
    #TODO title() names before putting in variable
    

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
    
    def toJson(self):
        return json.dumps(self, default = vars)
    
    def __str__(self):
        returnString = f"name: {self._name}, gender: {self._gender}, level: {self._level}, moves: {self._moves}, ability: {self._ability}, held item: {self._heldItem}"
        return returnString

class TrainerPokemon(Pokemon):
    def __init__(self, name, level):
        super().__init__(name, level)

class EncounteredPokemon(Pokemon):
    def __init__(self, name, level, state = 1):
        super().__init__(name, level)
        self._captureStatus = state
    
    @property
    def captureStatus(self):
        return self._captureStatus

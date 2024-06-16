from loggerConfig import logicLogger as logger

class Trainer():
    defaultDefeated = False
    def __init__(self, name, defeated = False):
        self._name = name
        self._area = None
        self._trainerType = None
        self._gender = None
        self._pokemon = []#List of pokemon otherwise trainers can't have the same pokemon twice
        self._defeated = defeated
        self._defeatedObservers = []
        self._removeObservers = []
        #check now, also checked whenever a pokemon is added
        self.checkDefeated()
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def area(self):
        return self._area
    
    @area.setter
    def area(self, areaObject):
        self._area = areaObject
    
    def removeTrainer(self) -> bool:
        if self.area == None:
            logger.error("Trainer has no Area")
            return 0
        if self.area.removeTrainer(self):
            self.notifyRemoveObservers()
            return 1
        return 0

    @property
    def trainerType(self):
        return self._trainerType
    
    @trainerType.setter
    def trainerType(self, type):
        self._trainerType = type

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if gender == None:
            self._gender = None
        else:
            gender = str(gender).upper()
            #print(f"gender: {gender}")
            if gender == "F" or gender == "M":
                self._gender = gender
            else:
                logger.error("enter valid gender, options are M or F")
    
    @property
    def pokemon(self):
        return self._pokemon
    
    @pokemon.setter
    def pokemon(self, pokemon):
        """expects a pokemon object"""
        if len(self._pokemon) < 6:
            pokemon.trainer = self
            self._pokemon.append(pokemon)
            self.checkDefeated()
            logger.debug(f"added {pokemon} to {self._name}")
        else:
            logger.error(f"{self._name} already has 6 pokemon")
    
    def removePokemon(self, PokemonObject):
        """Removes Pokemon from trainer. Returns 1 on success, 0 on failure"""
        for pokemon in self.pokemon:
            if pokemon is PokemonObject:
                self.pokemon.remove(pokemon)
                return 1
        else:
            logger.error(f"{self.name} has no pokemon {PokemonObject.name}")
            return 0

    @property
    def defeated(self):
        return self._defeated
    
    @defeated.setter
    def defeated(self, bool):
        self._defeated = bool
        self.notifyDefeatedObservers()
    
    def getNumberOfDefeatedPokemon(self) -> list:
        """returns a list of bool values"""
        return [pokemon.defeated for pokemon in self.pokemon if pokemon.defeated]
    
    def checkDefeated(self) -> bool:
        """function that checks if all pokemon have been defeated, changes self.defeated and return True or False"""
        if len(self.pokemon) == len(self.getNumberOfDefeatedPokemon()):
            #all pokemon have been defeated
            self.defeated = True
            return 1
        self.defeated = False
        return 0
        
    def storeToDataFile(self):
        variableDict = {"_name": self.name, "_trainerType": self.trainerType, "_gender": self.gender, "_pokemon": [pokemon.storeToDataFile() for pokemon in self.pokemon]}
        return variableDict

    def storeToSaveFile(self):
        """checks whether the trainer needs to be stored in the saveFile, if it is not defeated, or no pokemon are defeated It shouldn't"""
        #get a list of True or False
        logger.debug(f"saving {self._name}")
        
        variableDict = {"_name": self.name}
        
        self.checkDefeated()

        #add defeated status to json
        variableDict["_defeated"] = self.defeated

        #trainer has been defeated
        if self._defeated != self.defaultDefeated: 
            logger.debug(f"trainer has been defeated, only saving name and defeatedStatus")
            return variableDict
        
        if self.getNumberOfDefeatedPokemon() >= 1:
            #add pokemon to variable list as at least one pokemon has been defeated but the trainer hasn't
            logger.debug("adding pokemon to saveFile")
            variableDict["_pokemon"] = [pokemonJson for pokemon in self._pokemon if (pokemonJson := pokemon.storeToSaveFile()) is not None]
            return variableDict
        
        #no pokemon have been defeated and the trainer hasn't been defeated
        logger.debug("skipping trainer, has not been fought")
        return None

    def __str__(self):
        returnString = f"name : {self._name}. trainerType: {self._trainerType}. gender: {self._gender}. defeated: {self.defeated}\n"
        for pokemon in self._pokemon:
            returnString += pokemon.__str__() + "\n"
        return returnString
    
    def addObserver(self, callback, list) -> None:
        if callback not in list:
            list.append(callback)
    
    def notifyObservers(self, list)-> None:
        for callback in list:
            callback()


    def addDefeatedObserver(self, callback) -> None:
        self.addObserver(callback, self._defeatedObservers)
    
    def notifyDefeatedObservers(self) -> None:
        self.notifyObservers(self._defeatedObservers)
    
    def addRemoveObserver(self, callback) -> None:
        self.addObserver(callback, self._removeObservers)
    
    def notifyRemoveObservers(self) -> None:
        self.notifyObservers(self._removeObservers)
    
"""example json trainer
"Larry": {
    "_name": "Larry",
    "_trainerType": "Youngster",
    "_gender": "M",
    "_pokemon": [
     {
      "_name": "Charizard",
      "_level": "58",
      "_dexno": "n/a",
      "_gender": "n/a",
      "_moves": [
       "Flamethrower",
       "quick attack"
      ],
      "_ability": "drought",
      "_heldItem": "n/a"
     },
     {
      "_name": "Magikarp",
      "_level": "58",
      "_dexno": "n/a",
      "_gender": "n/a",
      "_moves": [
       "Splash",
       "quick attack"
      ],
      "_ability": "drizzle",
      "_heldItem": "heat rock"
     }
    ]
   }
"""
from loggerConfig import logicLogger as logger

class Trainer():
    defaultDefeated = False
    def __init__(self, name, defeated = False):
        self._name = name
        self._trainerType = None
        self._gender = None
        self._pokemon = []#List of pokemon otherwise trainers can't have the same pokemon twice
        self._defeated = defeated
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
    
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
                print("enter valid gender, options are M or F")
    
    @property
    def pokemon(self):
        return self._pokemon
    
    @pokemon.setter
    def pokemon(self, pokemon):
        """expects a pokemon object"""
        if len(self._pokemon) < 6:
            pokemon.trainer = self
            self._pokemon.append(pokemon)
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

    def storeToDataFile(self):
        variableDict = {"_name": self.name, "_trainerType": self.trainerType, "_gender": self.gender, "_pokemon": [pokemon.storeToDataFile() for pokemon in self.pokemon]}
        return variableDict

    def storeToSaveFile(self):
        """checks whether the trainer needs to be stored in the saveFile, if it is not defeated, or no pokemon are defeated It shouldn't"""
        #get a list of True or False
        logger.debug(f"saving {self._name}")
        numberOfDefeatedPokemon = [pokemon.defeated for pokemon in self.pokemon]
        variableDict = {"_name": self.name}
        
        #all checks for boolean values
        if all(numberOfDefeatedPokemon):
            #all pokemon have been defeated
            logger.debug(f"all pokemon have been defeated, changing trainers defeated status to True")
            self._defeated = True

        #add defeated status to json
        variableDict["_defeated"] = self.defeated

        #trainer has been defeated
        if self._defeated != self.defaultDefeated: 
            logger.debug(f"trainer has been defeated, only saving name and defeatedStatus")
            return variableDict
        
        if any(numberOfDefeatedPokemon):
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
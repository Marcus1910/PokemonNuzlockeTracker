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
            self._pokemon.append(pokemon)
            logger.debug(f"added {pokemon} to {self._name}")
        else:
            logger.error(f"{self._name} already has 6 pokemon")
        
    def editPokemon(self, pokemonObject, index = None, newPokemonName = None):
        """Edit pokemon Object and changes name if specified, returns 1 on success and 0 on failure"""
        pokemonName = pokemonObject.name
        pokemonAmount, pokemonIndexes = self.getPokemonIndex(pokemonName)
        #pokemon exists, change pokemon Objects
        if pokemonAmount == 0:
            logger.error(f"{self._name} does not have a Pokemon named: {pokemonName}")
            return 0
        #exactly one
        if pokemonAmount == 1:
            if newPokemonName != None:
                pokemonObject.name = newPokemonName
            popIndex = pokemonIndexes[0]
        #more than one pokemon
        if pokemonAmount > 1:
            if index == None:
                logger.error(f"More than 1 pokemon and index not specified")
                return 0
            if index in pokemonIndexes:
                popIndex = index
            else:
                logger.error(f"Index: {index} specified is not correct")

        #pop object from list
        self._pokemon.pop(popIndex)
        #insert new Object
        self._pokemon.insert(popIndex, pokemonObject)
        infoString = f"succesfully updated {pokemonName}"
        if index != None: infoString += f" to {newPokemonName}"
        logger.info(infoString)
        return 1
    
    def removePokemon(self, pokemonName, index=None):
        """Removes Pokemon from trainer based on index or name. Returns 1 on success, 0 on failure"""
        pokemonAmount, pokemonIndexes = self.getPokemonIndex(pokemonName)
    
        if pokemonAmount == 0:
            logger.error(f"{self._name} does not have a Pokemon named: {pokemonName}")
            return 0
        # Only one Pokemon with the given name
        if pokemonAmount == 1:
            pokemonIndex = pokemonIndexes[0]
        # More than one Pokemon with the given name
        elif pokemonAmount > 1:
            if index is None:
                logger.error(f"{self._name} has more than one Pokemon named {pokemonName}, please specify an index")
                return 0
    
            if index in pokemonIndexes:
                pokemonIndex = index
            else:
                logger.error(f"Specified index {index} does not match any Pokemon with name: {pokemonName}")
                return 0

        # Remove the Pokemon from the trainer
        self._pokemon.pop(pokemonIndex)
        return 1
    
    def getPokemonIndex(self, pokemonName):
        """Checks if the Pokemon exists for the trainer and returns Pokemon amount and indexes"""
        pokemonIndexes = [i for i, pokemon in enumerate(self._pokemon) if pokemon.name == pokemonName]
        pokemonAmount = len(pokemonIndexes)
        return pokemonAmount, pokemonIndexes

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
        #get a list of None or json formats
        NumberOfDefeatedPokemon = [pokemon.storeToSaveFile() for pokemon in self.pokemon]
        variableDict = {"_name": self.name}
        #want all the pokemon data if one pokemon, checks if all the pokemon in numberofdefeated pokemon are defeated, true
        if self._defeated != self.defaultDefeated or not all(pokemon is None for pokemon in NumberOfDefeatedPokemon): 
            variableDict["_pokemon"] = self.pokemon
            variableDict["_defeated"] = self.defeated
            return variableDict  
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
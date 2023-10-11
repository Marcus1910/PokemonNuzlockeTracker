
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
        if gender is None:
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
        else:
            print(f"{self._name} already has 6 pokemon")
    
    def removePokemon(self, pokemon):
        #TODO figure out how to remove specific pokemon
        self._pokemon.remove(pokemon)
    
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
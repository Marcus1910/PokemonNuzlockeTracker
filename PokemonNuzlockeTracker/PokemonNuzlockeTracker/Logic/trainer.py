
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
        #TODO figure out how to remove specifik pokemon
        self._pokemon.remove(pokemon)

    def __str__(self):
        returnString = f"name : {self._name}. trainerType: {self._trainerType}. gender: {self._gender}.\n"
        for pokemon in self._pokemon:
            #x = str(print(pokemon))
            returnString += pokemon.__str__() + "\n"
        return returnString
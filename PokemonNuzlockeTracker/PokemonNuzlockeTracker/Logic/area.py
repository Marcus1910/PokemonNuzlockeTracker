import json
from loggerConfig import logicLogger as logger

class Area():

    pokemonCatchLimit = 1 #TODO get from settings.py
    defaultCanCatchPokemon = False
    defaultStartLine = 0
    def __init__(self, name):
        self._name = name
        self._startLine = None #needed for initial reading, also useful for debugging
        self._encounters = [] #list with encounterpokemon objects
        self._trainers = {} #dict of trainer name - object
        self._items = {} # dict of item name - object
        self._accessible = 0 #how many badges are needed to access this area, default 0
        self._encounteredPokemon = {} #dict with pokemon objects name: object
        self._canCatchPokemon = True #replace code to somewhere it isnt immediatly called : False if len(self._encounteredPokemon) >= pokemonCatchLimit else True
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def startLine(self):
        return self._startLine
    
    @startLine.setter
    def startLine(self, line):
        self._startLine = line
    
    @property
    def encounters(self):
        return self._encounters
    
    @encounters.setter
    def encounters(self, encounter):
        self.encounters.append(encounter)
    
    def removeEncounter(self, encounter):
        #TODO remove correct encounter
        self._encounters.remove(encounter)

    @property
    def trainers(self):
        return self._trainers

    def addTrainer(self, trainerObject):
        """adds trainer to self._trainers dictionary, returns 0 if the trainer already exists and 1 if succesfull"""
        if trainerObject.name in self._trainers.keys():
            logger.error(f"{trainerObject.name} already exists")
            return 0
        self._trainers[trainerObject.name] = trainerObject
        logger.debug(f"added {trainerObject.name} to trainer list of {self._name}")
        return 1

    def editTrainer(self, trainerObject, newTrainerName = None):
        """edits the trainerObject and updates name if given, returns 1 on success and 0 on failure"""
        #check if trainer exists before editing
        if trainerObject.name not in self._trainers.keys():
            logger.error(f"{trainerObject.name} is not on this area")
            return 0
        #trainer is in the list
        #no new name needed so overwrite trainer object
        if newTrainerName == None:
            self._trainers[trainerObject.name] = trainerObject
            logger.info(f"updated {trainerObject.name}")
            return 1
        #check if new name is not already used by other trainer
        if newTrainerName in self._trainers.keys():
            logger.error(f"this area already has a trainer named: {newTrainerName}")
            return 0
        
        #remove old trainerObject to create new key value pair
        oldTrainerObject = self._trainers.pop(trainerObject.name)
        oldName = trainerObject.name
        oldTrainerObject.name = newTrainerName
        #add New trainerObject to trainers
        self.addTrainer(oldTrainerObject)
        logger.info(f"changed {oldName} to {newTrainerName} and updated its content")
        return 1
    
    def removeTrainer(self, trainerName):
        """removes trainerObject from trainer dict, return 1 on succes, 0 on failure"""
        if trainerName in self._trainers.keys():
            self._trainers.pop(trainerName)
            logger.info(f"removed {trainerName} from {self._name}")
            return 1
        logger.error(f"{trainerName} does not exist and cannot be removed")
        return 0

    @property
    def items(self):
        return self._items
    
    def removeItem(self, item):
        for items in self._items:
            if item.name == items.name:
                self._items.remove(item)
                logger.debug(f"removed {item}")
                break
        else:
            logger.error(f"{item} does not exist")

    @property
    def accessible(self):
        return self._accessible
    
    @accessible.setter
    def accessible(self, accessible):
        if self._accessible < accessible:
            logger.info(f"current gym badges required are {self._accessible}, changed it to {accessible}")
        else:
            self._accessible = accessible
    
    @property
    def encounteredPokemon(self):
        #remove pokemon that are not actually captured and have captureStatus 0
        self._encounteredPokemon = {pokemonName: pokemonObject for pokemonName, pokemonObject in self._encounteredPokemon.items()}# if pokemonObject.captureStatus != pokemonObject._defaultCaptureStatus}
        #print(f"F{self._encounteredPokemon}")
        return self._encounteredPokemon

    @encounteredPokemon.setter
    def encounteredPokemon(self, encounteredPokemon :dict): #pokemon object
        """expects a dictionary of name : pokemonObject and updates the first with the new pokemon"""
        #remove encounters with a '0' as status
        removelist = []
        for pokemon in encounteredPokemon.values():
            if pokemon.captureStatus == 0:
                removelist.append(pokemon.name)

        for pokemonName in removelist:
            #remove it from previous list as wel as the to be added list
            encounteredPokemon.pop(pokemonName)
            self._encounteredPokemon.pop(pokemonName)

        self._encounteredPokemon.update(encounteredPokemon)
        #scaffolding
        print("list of pokemon caught here")
        for key in self._encounteredPokemon.keys():
            print(key)
    
    @property
    def canCatchPokemon(self):
        return self._canCatchPokemon

    def createDictForSaving(self, dictionary, data = True):
        """function meant for the storeToDataFile or StoreToSaveFile, default is DataFile"""
        if data:
            #check whether the itemObject is empty, if it is empty ity is not included
            vars = {itemName: itemObject.storeToDataFile() for itemName, itemObject in dictionary.items()}
        else:
            #savedObject so function is only called once
            vars = {itemName: savedObject for itemName, itemObject in dictionary.items() if (savedObject := itemObject.storeToSaveFile()) is not None}
        return vars
    
    def storeToSaveFile(self):
        """function that will return a dictionary which stores all the variables meant to be stored into the savefile"""
        return {"_name": self.name, "_trainers": self.createDictForSaving(self.trainers, 0), \
                "_items": self.createDictForSaving(self.items, 0), "_encounteredPokemon": self.createDictForSaving(self.encounteredPokemon, 0)}

    def storeToDataFile(self):
        return {"_name": self.name, "_accessible": self.accessible, "_trainers": self.createDictForSaving(self.trainers),\
                 "_items": self.createDictForSaving(self.items), "_encounters": self.encounters}

    def __str__(self):
        returnString = f"{self._name} has {len(self._trainers)} trainers\n"
        for trainer in self._trainers:
            returnString += trainer.__str__()
        return returnString





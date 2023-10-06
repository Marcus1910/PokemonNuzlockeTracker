import json

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
    
    @trainers.setter
    def trainers(self, trainer):
        """setter expects an item object as parameter"""
        self._trainers[trainer.name] = trainer

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, item):
        """setter expects an item object as parameter"""
        self._items[item.name] = item
    
    def removeItem(self, item):
        for items in self._items:
            if item.name == items.name:
                print("needs to be deleted")
                self._items.remove(item)
                break
        else:
            print("item does not exist")

    @property
    def accessible(self):
        return self._accessible
    
    @accessible.setter
    def accessible(self, accessible):
        if self._accessible < accessible:
            print(f"current gym badges required are {self._accessible}, changed it to {accessible}")
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
            vars = {itemName: itemObject.storeToSaveFile() for itemName, itemObject in dictionary.items() if itemObject.storeToSaveFile() is not None}
        return vars
    
    def storeToSaveFile(self):
        """function that will return a dictionary which stores all the variables meant to be stored into the savefile"""
        return {"_name": self.name, "_trainers": self.createDictForSaving(self.trainers, 0), \
                "_items": self.createDictForSaving(self.items, 0), "_encounteredPokemon": self.createDictForSaving(self.encounteredPokemon, 0)}

    def storeToDataFile(self):
        return {"_name": self.name, "_trainers": self.createDictForSaving(self.trainers),\
                 "_items": self.createDictForSaving(self.items), "_encounters": self.encounters, "_accessible": self.accessible}

    def __str__(self):
        returnString = f"{self._name} has {len(self._trainers)} trainers\n"
        for trainer in self._trainers:
            returnString += trainer.__str__()
        return returnString





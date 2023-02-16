from trainer import Trainer
from trainerPokemon import TrainerPokemon
import json

class Area():
    def __init__(self, name):
        self._name = name
        self._startLine = None
        self._encounters = [] #list with encounterpokemon objects
        self._trainers = [] #list of trainer objects
        self._items = [] # list of item objects
        self._accessible = 0 #how many badges are needed to access this area, default 0
        self._encounteredPokemon = {} #dict with pokemon objects name: object
        pokemonCatchLimit = 1
        self.canCatchPokemon = True #replace code to somewhere it isnt immediatly called : False if len(self._encounteredPokemon) >= pokemonCatchLimit else True
    
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
        #TODO append correct trainer and no duplicates
        self._trainers.append(trainer)

    @property
    def item(self):
        return self._items

    def appendItem(self, item):
        for items in self._items:
            if item.name == items.name:
                print("item already exists")
                break
        #not found, also works if no items in list
        else: 
            self._items.append(item)
    
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


    def __str__(self):
        returnString = f"{self._name} has {len(self._trainers)} trainers\n"
        for trainer in self._trainers:
            returnString += trainer.__str__()
        return returnString





from games.trainer import Trainer
from games.pokemon import Pokemon
import json

class Area():
    def __init__(self, name):
        self._name = name
        self._startLine = None
        self._encounters = []
        self._trainers = []
        self._items = []
    
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

    @item.setter
    def item(self, item):
        if len(self._items) == 0:
            self._items.append(item)
        else:
            for index, items in enumerate(self._items):
                if item.name == items.name:
                    break
                elif index == len(self._items)-1:
                    self._items.append(item)
    
    def __str__(self):
        returnString = f"{self._name} has {len(self._trainers)} trainers\n"
        for trainer in self._trainers:
            returnString += trainer.__str__()
        return returnString





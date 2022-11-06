from addDeleteWindow import AddDeleteWindow
from ..Logic.trainer import Trainer
from ..Logic.trainerPokemon import TrainerPokemon
from ..Logic.encounterPokemon import EncounterPokemon
from ..Logic.area import Area
from ..Logic.item import Item

class AddDeleteTrainerWindow(AddDeleteWindow):
    def __init__(self, parent, list, currentRoute, delete, attribute):
        super().__init__(parent, list, currentRoute, delete, attribute)
    
    def createNewAttribute(self, input):
        newTrainer = Trainer(input)
        self._list.append(newTrainer)
        self._parent._listOfTrainers = self._list

    def deleteNewAttribute(self, input):
        self._list.remove(input)
        self._parent._listOfTrainers = self._list
    

class AddItemWindow(AddDeleteWindow):
    def __init__(self, parent, list, currentRoute, delete, attribute):
        super().__init__(parent, list, currentRoute, delete, attribute)
    
    def createNewAttribute(self, input):
        newItem = Item(input)
        self._list.append(newItem)
        self._parent._listOfItems = self._list
    
    def deleteNewAttribute(self, input):
        self._list.remove(input)
        self._parent._listOfItems = self._list
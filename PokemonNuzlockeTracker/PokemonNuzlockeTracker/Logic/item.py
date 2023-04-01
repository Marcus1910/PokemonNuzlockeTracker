class Item():
    defaultGrabbed = False
    def __init__(self, name, grabbed = False):
        self._name = name
        self._description = None
        self._location = None
        self._grabbed = grabbed
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, description):
        self._description = description

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location
    
    @property
    def grabbed(self):
        return self._grabbed
    
    @grabbed.setter
    def grabbed(self, bool):
        self._grabbed = bool
    
    def storeToDataFile(self):
        variableDict = {"_name": self.name, "_description": self.description, "_location": self.location}
        return variableDict


    

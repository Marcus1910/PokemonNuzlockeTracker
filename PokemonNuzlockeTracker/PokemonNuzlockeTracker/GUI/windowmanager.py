from kivy.uix.screenmanager import ScreenManager

class WindowManager(ScreenManager):
    attempt = None
    #global game object
    _gameObject = None
    areaList = None
    #gets replaced with the area object as soon as it is chosen
    _currentArea = None

    _screenNumber= 0
    screenList = []

    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self, gameObject):
        self._gameObject = gameObject
        print("gathering data")
        self.areaList = self._gameObject.retrieveGameData()
    
    @property
    def screenNumber(self):
        return self._screenNumber
    
    @screenNumber.setter
    def screenNumber(self, number):
        self._screenNumber = number % len(self.screenList)
        self.current = self.screenList[self._screenNumber]

    @property
    def currentArea(self):
        return self._currentArea
    
    @currentArea.setter
    def currentArea(self, areaName):
        """function expects a name, creates an AreaObject from that name"""
        for area in self.areaList:
            if area.name == areaName:
                self._currentArea = area
                break
        else:
            print(f"Area {areaName} not found")
        print(self._currentArea.name)
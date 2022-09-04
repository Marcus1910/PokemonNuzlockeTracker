from tkinter import *

class EncounterWindow():
    def __init__(self, encounterList, parent):
        #create window 
        self._master = Toplevel(parent)
        self._master.attributes("-topmost", True)   
        
        #determine what should be in window
        print(len(encounterList))
        for type in encounterList:
            #type[0] name of type
            #type[1] list of encounters

            print(type[1])

    
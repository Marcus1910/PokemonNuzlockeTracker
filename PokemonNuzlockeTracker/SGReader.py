from games.area import Area
from games.encounterPokemon import EncounterPokemon
import pdfplumber
import re


class SacredGoldWriter():
    def __init__(self):
        self._areaTypes = ["Tower", "Route", "City", "Town", "Cave", "Mt", "Room", "Outside", "Ruins", "Well", "Forest", "Park", "Lake", "Island", "Path", "Den", "Falls", "Road", "Tunnel"]
        self._areaList = []
        self._data = None
        pass

    def openPdf(self):
        with pdfplumber.open("Pokemon Locations.pdf") as pdf:
            file = open("sacredGoldEncounters.txt", "w") 
            file.truncate()
            for page in pdf.pages:
                text = page.extract_text()
                #pdf extract gives word as wwwwoooorrrrdddd so remove every character that repeats itself 4 times
                duplicateChars = re.findall(r"(.)\1{3}", text)
                for char in duplicateChars:
                    if char * 4 in text:
                        text = text.replace(char * 4, char)   
                file.write(text)
                #break
            file.close()
    
    def readFile(self):
        with open("sacredGoldEncounters.txt") as file:
            self._data = file.readlines()

    def writeToFile(self):
        with open("newData.txt", "w") as file:
            for line in self._data:
                file.write(line + '\n')

x = SacredGoldWriter()
#x.openPdf()
x.readFile()

x.writeToFile()
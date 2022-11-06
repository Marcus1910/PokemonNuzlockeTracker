from area import Area
from encounterPokemon import EncounterPokemon
import copy


class readFormattedData():
    def __init__(self, file):
        self._areaTypes = ["Tower", "Route", "City", "Town", "Cave", "Mt", "Room", "Outside", "Ruins", "Well", "Forest", "Park", "Lake", "Island", "Path", "Den", "Falls", "Road", "Tunnel"]
        self._file = file
        self._data = None
        self._areaList = []

    def readFile(self):
        with open(f"{self._file}.txt") as file:
            self._data = file.readlines()

    def indexAreas(self):
        for index, line in enumerate(self._data):
            for area in self._areaTypes:
                if area in line:
                    if ":" not in line and "," not in line and "(" not in line:
                        while "  " in line:
                            line = line.replace("  ", " ")
                        if line[-1:] == " ":
                            line = line[:-1]
                        newArea = Area(line)
                        newArea.startLine = index
                        self._areaList.append(newArea)
    
    def areaList(self):
        returnString = ""
        for area in self._areaList:
            returnString += f"{area.name} {area.startLine}\n"
        return returnString
    
    def removeDuplicateNames(self):
        alreadySeen = []
        newAreaList = []
        for area in self._areaList:
            if "\n" in area.name:
                #print(f"{area.name} has '\n' in it")
                area.name = area.name.replace("\n", "")
                if area.name[-1] == " ":
                    area.name = area.name.rstrip()
            if area.name not in alreadySeen:
                alreadySeen.append(area.name)
                newAreaList.append(area)
                self._areaList = newAreaList
    
    def createEncounterLists(self):
        #area loop
        for areaNumber, area in enumerate(self._areaList):
            formattedList = []
            #areaname is already known
            beginLine = area.startLine + 1
            #create boundaries for each area
            try:
                nextLine = self._areaList[areaNumber + 1].startLine
            except IndexError:
                nextLine = len(self._data)
            #data loop
            for line in range(nextLine - beginLine):  
                encounterList = []

                currentLine = self._data[beginLine+line]
                separatedLine = currentLine.split(':')
                terrainType = separatedLine[0]
                if "Wild Level" in separatedLine[0]:
                    level = separatedLine[1]
                    if "ï¿½" in level:
                        level = level.replace(" ï¿½ " , " - " )
                    else:
                        level = "N/A"
                    #continue otherwise wild levels will be seen as an encounter type
                    continue
                pokemons = separatedLine[1].split(',')
                #create pokemon object loop
                for index, pokemon in enumerate(pokemons):
                    pokemon = pokemon.split("(", 1)
                    #remove left-over spaces from pokemon species
                    species = pokemon[0].strip()
                    try:
                        percentage = pokemon[1].split(')')[0]
                    except IndexError:
                        percentage = "N\A"
                    encounter = EncounterPokemon(species, level, percentage)
                    encounterList.append(encounter)
                formattedList.append([terrainType, encounterList])
            self._areaList[areaNumber]._encounters = copy.deepcopy(formattedList) 


    def returnAreaList(self):
        """function that reads all encounterdata and returns a list [areaname [ terrainType, [ encounterlist ] ], [ [ ] ] ]"""
        self.readFile()
        self.indexAreas()
        self.removeDuplicateNames()
        self.createEncounterLists()
        return self._areaList





# x = readFormattedData('sacredGoldCorrectData')
# x.readFile()
# x.indexAreas()
# x.removeDuplicateNames()
# x.createEncounterLists()


    

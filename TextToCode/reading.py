from area import Area
from encounterPokemon import EncounterPokemon
import re

class BlazeBlack2ReduxReader():
    def __init__(self):
        self.places= []
        self.seasons = ["Spring", "Autumn", "Summer", "Winter"]
        self.areaNames = ["Route", "City", "Town", "Ranch", "Tower", "Shrine", "Bay", "Mountain", "Road", \
            "Castle", "Complex", "Sewers", "Passage", "Resort", "Forest", "Bridge", "Tunnel", "Cave", "House"]
        self.extraNames = ["Fish", "Surf", "Special Event", "Dust", "Spots", "Normal", "Cloud", "Normal"]
        self.finalLine = 0


    def openFile(self, textFile):
        with open(textFile) as file:  
            self.data = file.readlines()
    
    def removeEmptyLines(self):
        popList = []
        for index, readLine in enumerate(self.data):
            #remove filler lines and \n lines
            if "--" in readLine or "==" in readLine or len(readLine) == 1:
                self.data.remove(readLine)
            #remove all newline characters and remove double spaces
            self.data[index] = self.data[index].replace('\n', '').replace("  ", "")
            #remove leftover ""
            if len(self.data[index]) == 0:
                #removing index
                popList.append(index)
        popList.reverse()
        for item in popList:
            self.data.pop(item)    
    
    def createSeperateLists(self):
        mainStart =0
        postStart =0
        grottoStart =0
        createrList = []
        for index, readLine in enumerate(self.data):
            if "Main Story" in readLine:
                mainStart = index
                createrList.append(mainStart)
            if "Postgame" in readLine:
                postStart = index
                createrList.append(postStart)
            if "Hidden Grotto Guide" in readLine:
                #need only the last
                grottoStart = index      
        createrList.append(grottoStart)
        createrList.append(len(self.data))
        createrList.sort()
        for item in range(len(createrList)-1):
            for index in range(createrList[item], createrList[item+1]):
                print(self.data[index])
    #TODO create Main, post and grotto lists

        print(createrList)
            
            #put in list, sort list on size, create lists

    def createAreas(self):
        #create area objects and give them a name and lineNumber attribute
        for index, readLine in enumerate(self.data):  
            if "Postgame" in readLine:
                self.finalLine = index
            for area in self.areaNames:
                if area in readLine:
                    #skip over lines that contain "cave" but are about encounters
                    if ":" not in readLine:# and index < self.finalLine:
                        #found correct area
                        #remove spaces aroudn the name
                        place = readLine.replace("~", "")[1:-1]
                        line = index
                        areaObject = Area(place, line)
                        self.places.append(areaObject)
                        #print(f"{index} : {place}")
        #for place in self.places:
        #    print(place.name)

    
    def createPokemonBlocks(self):
        #grab lines between areas to make correct encounter tables
        for index in range(len(self.places)):
            pokemonBlock = []
            nextIndex = index + 1
            startingLine = self.places[index].startingLine
            try: 
                #dont grab name line
                lastLine = self.places[nextIndex].startingLine
            except IndexError:
                lastLine = self.finalLine
            
            print(f"take {startingLine} untill {lastLine}")
            for index in range(startingLine, lastLine):
                pokemonBlock.append(self.data[index])
            print(pokemonBlock)

    def writeDataToFile(self):
        with open("data.txt", "w") as file:
            file.truncate()
            for index, readLine in enumerate(self.data):
                file.write(f"{index}, {readLine}\n")
        #remove all lines which do not contain any data

        # cleanUpList = []
        # for place in range(len(self.places)):
        #     placeName = self.places[place]
        #     start = self.places[place].line
        #     nextPlace = place
        #     nextPlace += 1
            
        #     if nextPlace == len(self.places):
        #         #print("yes")
        #         end = self.finalLine
        #     else:
        #         end = self.places[nextPlace].line
        #     #    pass
        #     #print(f"nextPlace: {nextPlace}")
            
        #     difference = end - start
        #     #remove duplicate names which have no encounters within them, got created because they contained 2 keywords
        #     if difference == 0:
        #         cleanUpList.append(start)
        #     #print(f"start: {start}, end: {end}, difference: {difference}")
        #     encounterBlock = []
        #     for encounters in range(start,end,1):
        #         encounterBlock.append(self.data[encounters])

        #     #put correct pokemon in the lists
        #     self.createEncounterList(encounterBlock, placeName)

        # for index in range(len(cleanUpList)):
        #     self.places.pop(index)
           


    def createEncounterList(self, encounterBlock, placeName):
        # ':' twice or % twice == double row
        # if len(readLine) == 0:
        #             removeList.append(index)
        #         else:
        name = placeName
        encounters = []
        lists = -1

        for encounter in encounterBlock:
            #print(encounter)
            #check for single line
            if "Hidden Grotto" in encounter:
                #call function with current place name
                #left or right check
                pass
            if encounter.count(":") == 1:
                areaType = encounter
                encounters.append([areaType])
                lists += 1

            if encounter.count("%") == 1:
                encounters[lists].append(encounter)

            if encounter.count(":") == 2:
                #make two lists
                
                dualLines = encounter.split(":",1)
                leftName = dualLines[0]
                #.replace ugly solution for now
                rightName = dualLines[1].replace(" ", "") 
                encounters.append([rightName])
                encounters.append([leftName])
                lists += 2

            if encounter.count("%") == 2:
                #remove
                dualLines = encounter.split("  ",1)
                left = dualLines[0]
                #.replace ugly solution for now
                right = dualLines[1]
                encounters[lists].append(left)
                encounters[lists-1].append(right)
                
    
            else:
                pass
        #give area object all available pokemon in a encounterlist
        name.encountersList = encounters

    def createPokemonObjectList(self):
        for place in range(len(self.places)):
            #amount of lists in encounters
            list = self.places[place].encountersList
            for type in range(len(list)):
                areaType = self.places[place].encountersList[type]
                #don't need areaName
                for pokemon in range(1,len(areaType)):
                    #print(f"place: {place}, areatype: {type}, pokemon: {pokemon}")
                    #print(areaType[pokemon])
                    line = list[type][pokemon]
                    separatedLine = re.split("Lv. |" ",", line)
                    name = separatedLine[0]
                    name = name.replace(" ", "")
                    #remove whitespaces
                    while separatedLine[1][-1:] == " ":
                        separatedLine[1] = separatedLine[1][:-1]
                    levels = separatedLine[1][0:-4]
                    rarity = separatedLine[1][-4:]
                    encounterPokemon = EncounterPokemon(name, levels, rarity)

                    #update places list to contain pokemon objects
                    self.places[place].encountersList[type][pokemon] = encounterPokemon
                    



    def __str__(self):
        returnString = []
        for place in self.places:
            returnString.append(place.__str__())
        return "\n".join(returnString)


#     if "Postgame" in readLine:
        #         postgame = True
        #         postgameLine = index

        #     if "Grotto Guide" in readLine:
        #         print("grotto")
        #         grotto = True
        #         grottoLine = index
        # #remove lines between postgame an hidden grotto
        # if postgame == True and grotto == True:
        #     print("deleting")
        #     popList = []
        #     #remove lines between
        #     deleteLines = abs(grottoLine - postgameLine)

        #     if grottoLine < postgameLine:
        #         startingValue = grottoLine
        #     else:
        #         startingValue = postgameLine

        #     for index in range(deleteLines):
        #         popIndex = index + startingValue
        #         popList.append(popIndex)
        #     #remove last line first
        #     popList.reverse()

        #     for index in popList:
        #         print(f"popped index : {index}")
        #         self.data.pop(index)



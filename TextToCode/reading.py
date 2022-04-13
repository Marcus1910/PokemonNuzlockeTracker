import time
from area import Area


class BlazeBlack2ReduxReader():
    def __init__(self):
        self.places= []
        self.seasons = ["Spring", "Autumn", "Summer", "Winter"]
        self.areaNames = ["Route", "City", "Town", "Ranch", "Tower", "Shrine", "Bay", "Mountain", "Road", \
            "Castle", "Complex", "Sewers", "Passage", "Resort", "Forest", "Bridge", "Tunnel", "Cave", "House"]
        self.finalLine = 0

    def openFile(self, textFile):
        with open(textFile) as file:  
            self.data = file.readlines()
    
    def removeEmptyLines(self):
        for readLine in self.data:
            if "--" in readLine:
                self.data.remove(readLine)
            #remove newline characters
            if len(readLine) == 1:
                self.data.remove(readLine)

    def createAreas(self):
        #create area objects and give them a name and lineNumber attribute
        readLineNumber = 0
        for readLine in self.data:
            if "Postgame" in readLine:
                self.finalLine = readLineNumber
                break
            for area in self.areaNames:
                if area in readLine:
                    if "Fish" in readLine or "Surf" in readLine or "Special Event" in readLine or "Dust" in readLine or "Spots" in readLine or "Normal" in readLine:
                        #not needed, documentation fucked up
                        pass
                    else:
                        #fuck those spaces at the end
                        place = readLine.replace("~", "").replace("\n", "")[:-1]
                        areaObject = Area(place)
                        areaObject.line = readLineNumber
                        self.places.append(areaObject)
            readLineNumber += 1

    
    def createPokemonBlocks(self):
        #print(f"len places: {len(self.places)}")
        cleanUpList = []
        for place in range(len(self.places)):
            placeName = self.places[place]
            start = self.places[place].line
            nextPlace = place
            nextPlace += 1
            
            if nextPlace == len(self.places):
                #print("yes")
                end = self.finalLine
            else:
                end = self.places[nextPlace].line
            #    pass
            #print(f"nextPlace: {nextPlace}")
            
            difference = end - start
            #remove duplicate names which have no encounters within them, got created because they contained 2 keywords
            if difference == 0:
                cleanUpList.append(start)
            #print(f"start: {start}, end: {end}, difference: {difference}")
            encounterBlock = []
            for encounters in range(start,end,1):
                encounterBlock.append(self.data[encounters])

            #put correct pokemon in the lists
            self.createEncounterList(encounterBlock, placeName)

        for index in range(len(cleanUpList)):
            self.places.pop(index)
           


    def createEncounterList(self, encounterBlock, placeName):
        # ':' twice or % twice == double row
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

        name.allEncounters = encounters
        print(name.allEncounters)
            

        for i in range(len(encounters)):
            print(encounters[i])
        

        #check if list is empty apart from name otherwise dispose of it
   



    def __str__(self):
        returnString = []
        for place in self.places:
            returnString.append(place.__str__())
        return "\n".join(returnString)


textfile = "area.txt"
textfile1 = "Wild Area Changes.txt"
textfile2 = "Wild Area Changes Final.txt"
x = BlazeBlack2ReduxReader()
x.openFile(textfile)
x.removeEmptyLines()
x.createAreas()
x.createPokemonBlocks()
#print(x.data)
#print(x)


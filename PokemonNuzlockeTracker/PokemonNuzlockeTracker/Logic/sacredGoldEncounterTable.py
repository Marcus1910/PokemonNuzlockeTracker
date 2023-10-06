from area import Area
from trainerPokemon import EncounterPokemon
import pdfplumber
import re

write = False
class SacredGoldWriter():
    def __init__(self):
        self._areaTypes = ["Tower", "Route", "City", "Town", "Cave", "Mt", "Room", "Outside", "Ruins", "Well", "Forest", "Park", "Lake", "Island", "Path", "Den", "Falls", "Road", "Tunnel"]
        self._areaList = []
        self._data = None
        pass

    def areaList(self):
        returnString = ""
        for area in self._areaList:
            returnString += f"{area.name} {area.startLine}\n"
        return returnString
    
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

    def removeLines(self):
        removeList = []
        """format data by removing unneccessary tokens"""
        for index, line in enumerate(self._data):
            #check for space at front of line
            #empty lines
            if line == ' \n' or line == '\n' or line == '  \n':
                removeList.append(index)
            elif '\n' in line:
                while '\n' in line:
                    line = line.replace('\n', '')
                    self._data[index] = line
            if line[0:1] == ' ':
                self._data[index] = line[1:]
        removeList.reverse()
        for line in removeList:
            self._data.pop(line)
    
    def formatData(self):
        self.removeLines()
        for index, line in enumerate(self._data):
            for area in self._areaTypes:
                #incorrect pdf layout, areaName stuck at end of previous line
                if area in line[-10:] and ":" in line:
                    if area == "Cave":
                        newLine = re.split("The ", line)
                        self._data[index] = newLine[0]
                        self._data.insert(index + 1, newLine[1])
                    if area == "Route":
                        newLine = re.split(area, line)
                        self._data[index] = newLine[0]
                        newLine[1] = "Route" + newLine[1]
                        self._data.insert(index + 1, newLine[1])
    
    def indexAreas(self):
        for index, line in enumerate(self._data):
            for area in self._areaTypes:
                if area in line:
                    if ":" not in line and "," not in line and "(" not in line: #and "[" not in line
                        while "  " in line:
                            line = line.replace("  ", " ")
                        if line[-1:] == " ":
                            line = line[:-1]
                        newArea = Area(line)
                        newArea.startLine = index
                        self._areaList.append(newArea)
        
        # for area in self._areaList:
        #     print(area)
        # print(len(self._areaList))
    
    def putEncounterOnOneLine(self):
        #sort list on startline
        removeList = []
        x = 0
        self._areaList.sort(key = lambda x: x.startLine)
        #remove text before 1st area encounter
        while x < self._areaList[0].startLine:
            removeList.append(x)
            x += 1

        for index, area in enumerate(self._areaList):
            startLine = area.startLine + 1
            try:
                finishLine = self._areaList[index + 1].startLine
            except IndexError:
                finishLine = len(self._data)
            lines = finishLine - startLine
            #print(f"lines {lines}")
            for line in range(lines):
                lineNumber = startLine + line
                dataLine = self._data[lineNumber]
                previousLine = self._data[lineNumber - 1]
                if ":" not in dataLine and '[' not in dataLine:
                    previousLine += dataLine
                    self._data[lineNumber - 1] = previousLine
                    removeList.append((lineNumber))
        removeList.reverse()
        for item in removeList:
            self._data.pop(item)
        self._areaList = []
    
    def createEncounters(self):
        for index, area in enumerate(self._areaList):
            startLine = area.startLine
            try:
                finalLine = self._areaList[index + 1].startLine
            except IndexError:
                finalLine = len(self._data)
            difference = finalLine - startLine
            #skip name of area
            #print(self._data[startLine])
            # for line in range(1, difference):
            #     currentLine = startLine + line
            #     data = self._data[currentLine]
            #     if ":" not in data:
            #         pass
            #         #print(data, currentLine)
            #     #print(self._data[startLine + line])
            #     pass
    def test(self):
        for index, line in enumerate(self._data):
            if ":" in line and "[" in line:
                #remove [] from line
                #make new area with same name as previous area
                nextLine = index + 1
                print(line)
                print(self._data[nextLine])
                return







game = SacredGoldWriter()
#game.openPdf()
game.readFile()
game.formatData()
game.indexAreas()
game.putEncounterOnOneLine()
#give [3f] correct names
#game.addFloors()
#give correct starting lines
game.indexAreas()
game.createEncounters()

game.writeToFile()
# game.test()
print(game.areaList())

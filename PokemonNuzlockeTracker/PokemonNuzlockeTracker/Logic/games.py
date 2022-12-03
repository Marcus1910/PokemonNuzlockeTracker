from area import Area
from trainer import Trainer
from trainerPokemon import TrainerPokemon
from encounterPokemon import EncounterPokemon
from item import Item
from readFormattedData import readFormattedData

import json
import os

txtfile = "trainerData.txt"

class MainGame():
    def __init__(self, gameName):
        self.areaList = []
        self.readData = None
        self.areaList = []
        self.areaNamesList = []
        self.trainerList = []
        self.itemList = []

        self.gameName = gameName
        self.gamePath = os.path.join(os.path.dirname(os.getcwd()), f"games/{self.gameName}")
        self.dataFolder = os.path.join(self.gamePath, "data")
        self.saveFileFolder = os.path.join(self.gamePath, "saveFiles")
        self.dataFile = os.path.join(self.dataFolder, f"{self.gameName}GameData.txt")

    def getAreaNamesList(self):
        if len(self.areaNamesList) <= 0:
            for area in self.areaList:
                self.areaNamesList.append(area.name)
                print(area.name)
        else:
            print("no area Names")
        return self.areaNamesList

    def writeToFile(self):
        with open(self.dataFile, "w") as file:
            file.truncate()
            file.write(json.dumps(self.areaList, default = vars, indent = 1))

    def retrieveGameData(self):
        try:
            with open(self.dataFile, "r") as file:
                try:
                    self.readData = json.load(file)
                    self.convertDataToObjects()
                except json.JSONDecodeError:
                    #json failed to load so file is empty or invalid, reloading from correctdata
                    self.retrieveEncounterData()
        except FileNotFoundError:
            print(f"there is no GameData for {self.gameName}, collecting it from {self.gameName}CorrectData.txt")
            self.retrieveEncounterData()

    
    def retrieveEncounterData(self):
        #TODO correct path
        #only needed to create the json dumps and backup if file cannot be read
        self.areaList = readFormattedData(f"{self.dataFolder}\{self.gameName}CorrectData.txt").returnAreaList()
        print(self.areaList)
                
    def convertDataToObjects(self):  
        #get all the data from the json dump
        #TODO different file for cleaner code?
        #add logic to add encounterpokemon, encounterpokemon window are only available when running from empty 'SacredGoildGameData.txt' file
        for area in self.readData:
            alreadyexists = False
            areaName = area["_name"]
            startLine = area["_startLine"]
            
            #check if route exists by looping through entire list
            for route in self.areaList:
                if areaName == route.name:
                    wildArea = route
                    alreadyexists = True
                    break
            #if not found in areaList
            else:
                wildArea = Area(areaName)
                
            wildArea.startLine = startLine
            
            '''retrieve encounters from json dump in sacredGoldGameData.txt'''
            terrainTypes = area["_encounters"]
            for terrain in terrainTypes:
                encounterList = []
                terrainName = terrain[0]
                pokemonList = terrain[1]
                for pokemon in pokemonList:
                    encounterName = pokemon["name"]
                    encounterLevels = pokemon["levels"]
                    encounterPercentage = pokemon["percentage"]
                    encounterPokemon = EncounterPokemon(encounterName, encounterLevels, encounterPercentage)
                    encounterList.append(encounterPokemon)
                wildArea._encounters.append([terrainName, encounterList])
                #print(wildArea.encounters)
                encounterList = [terrainName, pokemonList]
            

            """retrieve all area attributes"""
            items = area["_items"]
            for item in items:
                itemName = item["_name"]
                areaItem = Item(itemName)
                areaItem.description = item["_description"]
                areaItem.location = item["_location"]
                wildArea.item = areaItem
            
            """retrieve all trainer attributes"""
            trainers = area["_trainers"]
            for trainer in trainers:
                trainerName = trainer["_name"]
                pokemonTrainer = Trainer(trainerName)
                pokemonTrainer.trainerType = trainer["_trainerType"]
                pokemonTrainer.gender = trainer["_gender"]
                
                """retrieve pokemon attributes"""
                for pokemon in trainer["_pokemon"]:
                    pokemonName = pokemon["_name"]
                    pokemonLevel = pokemon["_level"]
                    trainerPokemon = TrainerPokemon(pokemonName, pokemonLevel)
                    trainerPokemon._gender = pokemon["_gender"]
                    trainerPokemon._ability = pokemon["_ability"]
                    trainerPokemon._heldItem = pokemon["_heldItem"]
                    trainerPokemon._dexNo = pokemon["_dexNo"]
                    #give the moves to the pokemon
                    moves = pokemon["_moves"]
                    for move in range(len(moves)):
                        trainerPokemon.moves = moves[move]
                    pokemonTrainer.pokemon = trainerPokemon
                wildArea.trainers = pokemonTrainer
            if not alreadyexists:
                self.areaList.append(wildArea)

    def checkForSaveFileDirectory(self):
        """checks if the directory existst otherwise creates it"""

        #if savefile directory doesn't exists
        if not os.path.isdir(self.saveFileFolder):
            print(f"creating new directory {self.saveFileFolder}")
            os.mkdir(self.saveFileFolder)

    
    def getSaveFiles(self):
        """returns a list of the attempts made with a 'new' option"""
        self.checkForSaveFileDirectory()
        #get every file, [0] because it returns a list inside of a list
        saveFiles = [x[2] for x in os.walk(self.saveFileFolder)][0]
        #keep files with attempt in its name, and remove the '.txt'
        saveFiles = [x[:-4] for x in saveFiles if("attempt" in x)] 
        #give the option to make a new saveFile
        saveFiles.append("new")

        return saveFiles
    
    def addNewSaveFile(self):
        #"new" has purposely not been removed, now len == attempt
        saveFiles = self.getSaveFiles()
        number = len(saveFiles)
        #create the file then close it
        open(f"{self.saveFileFolder}/attempt {number}.txt", "x").close()

def checkGames():
    gameFolder = os.path.join(os.path.dirname(os.getcwd()), "games")
    #walks down the directory for other directories, retrieves the names an puts them in a list
    games = [x[1] for x in os.walk(gameFolder)][0]
    #no games
    if not games:
        return ["new"]
    return games

    
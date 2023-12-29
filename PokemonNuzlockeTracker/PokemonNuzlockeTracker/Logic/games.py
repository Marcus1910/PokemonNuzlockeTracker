from area import Area
from trainer import Trainer
from trainerPokemon import TrainerPokemon, EncounteredPokemon
from item import Item
from readFormattedData import readFormattedData
from loggerConfig import logicLogger as logger


import json
import os

txtfile = "trainerData.txt"
#change to settings
opaque = (1, 1, 1, 0.6)
standardColor = (1, 1, 1, 1)
red = (1, 0, 0, 1)
blue = (0, 0, 1, 1) 
green = (0, 1, 0, 1)


class MainGame():
    errorName = "error something went wrong reading from the json file" # TODO settings.py
    def __init__(self, gameName, saveFileName = 'new'): #TODO change new to actual new attempt name
        self.gameName = gameName
        self.saveFileName = f"{saveFileName}.txt"

        self.readData = None
        self.saveFileError = False
        self._badge = 0 #default badge 0
        
        #not a dictionary, because we want it to be in documentation order and in a stable order, dict items can change position
        self.areaList = []
        self.gamePath = os.path.join(os.path.dirname(os.getcwd()), f"games/{self.gameName}")
        self.dataFolder = os.path.join(self.gamePath, "data")
        self.saveFileFolder = os.path.join(self.gamePath, "saveFiles")

        self._saveFile = os.path.join(self.saveFileFolder, self.saveFileName)
        self.dataFile = os.path.join(self.dataFolder, f"{self.gameName}GameData.txt")
    
    @property
    def badge(self):
        return self._badge
    
    @badge.setter
    def badge(self, badge):
        self._badge = badge
    
    @property
    def saveFile(self):
        return self._saveFile
    
    @saveFile.setter
    def saveFile(self, filename):
        self._saveFile = os.path.join(self.saveFileFolder, f"{filename}.txt")

    def writeToFile(self):
        logger.info("saving game")
        dataAreaList = []
        saveFileList = [{"_badge": 6}]
        #fill lists with all the data to save
        for area in self.areaList:
            dataAreaList.append(area.storeToDataFile())
            saveFileList.append(area.storeToSaveFile())

        #savefile location has been edited if there was an error reading from it
        with open(self.saveFile, "w") as file:
            file.truncate()
            file.write(json.dumps(saveFileList, default = vars, indent = 1))

        with open(self.dataFile, "w") as file:
            file.truncate()
            file.write(json.dumps(dataAreaList, default = vars, indent = 1))  

    def retrieveGameData(self):
        """retrieves all information that can be found about the current game, including selected savefile"""
        self.retrieveGlobalGameData()
        if not self.saveFileError:
            self.retrieveSaveFile()
        return self.areaList

    def retrieveGlobalGameData(self):
        """retrieves game data and saves it into readData"""
        try:
            with open(self.dataFile, "r") as file:
                try:
                    self.readData = json.load(file)
                    self.addGameData()
                except json.JSONDecodeError as e:
                    logger.error(f"json failed to load so file is empty or invalid, reloading from correctdata, {e}")
                    #change datafile name so no progress is lost
                    self.retrieveEncounterData()
        except FileNotFoundError:
            logger.error(f"there is no GameData for {self.gameName}, collecting it from {self.gameName}CorrectData.txt",exc_info = True)
            self.retrieveEncounterData()

    def retrieveSaveFile(self):
        try:
            with open(self.saveFile, "r") as file:
                try:
                    saveFileJson = json.load(file)
                    self.addSaveFileData(saveFileJson)
                except json.JSONDecodeError as e:
                    self.saveFileError = True
                    #TODO change self.saveFileError to a different file because the original cannot be read
                    logger.error(f"Something went wrong, could not load saveFile", exc_info = True)
        except FileNotFoundError:
            logger.error(f"Savefile, {self.saveFile} could not be found", exc_info = True)
            self.saveFileError = True

    def retrieveEncounterData(self):
        #only needed to create the json dumps and backup if file cannot be read
        self.areaList = readFormattedData(f"{self.dataFolder}\{self.gameName}CorrectData.txt").returnAreaList()

    def addGameData(self):
        """converts all data read from the game data json file and converts it into objects"""  
        for area in self.readData:
            alreadyexists = False
            areaName = area["_name"]
            
            #check if route exists by looping through entire list
            for route in self.areaList:
                if areaName == route.name:
                    wildArea = route
                    alreadyexists = True
                    break
            #if not found in areaList
            else:
                wildArea = Area(areaName)
                wildArea = self.getFromJSON(wildArea, area, ["_encounters", "_items", "_trainers", "_encounteredPokemon"])#exclude items, trainers, encounters and encounteredpokemon
            
            '''retrieve encounters from json dump in sacredGoldGameData.txt'''
            terrainTypes = area["_encounters"]
            for terrain in terrainTypes:
                encounterList = []
                terrainName = terrain[0]
                pokemonList = terrain[1]
                for pokemonJson in pokemonList:
                    encounterPokemon = EncounteredPokemon(self.errorName)
                    encounterPokemon = self.getFromJSON(encounterPokemon, pokemonJson)
                    logger.debug(f"FINISHED POKEMON: {encounterPokemon}")
                    encounterList.append(encounterPokemon)
                wildArea._encounters.append([terrainName, encounterList])
                encounterList = [terrainName, pokemonList]
            
            """retrieve all area attributes"""
            items = area["_items"]
            logger.debug(f"STARTING {areaName} ITEMS")
            for itemName, itemJson in items.items():
                areaItem = Item(itemName)
                areaItem = self.getFromJSON(areaItem, itemJson)
                logger.debug(f"FINISHED ITEM: {itemName}")
                wildArea.items[areaItem.name] = areaItem
            logger.debug(f"FINISHED {areaName} ITEMS")
            
            """retrieve all trainer attributes"""
            logger.debug(f"STARTING {areaName} TRAINERS")
            trainers = area["_trainers"]
            for trainerName, trainerJson in trainers.items():
                #trainerName = trainer["_name"]
                pokemonTrainer = Trainer(trainerName)
                
                pokemonTrainer = self.getFromJSON(pokemonTrainer, trainerJson, ["_pokemon"]) #puts json as a pokemon
                logger.debug(f"FINISHED {pokemonTrainer.name} WITHOUT POKEMON ATTRIBUTES")

                
                """retrieve pokemon attributes"""
                pokemonJson = trainerJson["_pokemon"]
                pokemonAmount = len(trainerJson["_pokemon"])
                for number in range(pokemonAmount):
                    trainerPokemon = TrainerPokemon(self.errorName, 0)
                    trainerPokemon = self.getFromJSON(trainerPokemon, pokemonJson[number])
                    pokemonTrainer.pokemon = trainerPokemon
                #append to area object
                logger.debug(f"added {trainerName} to {wildArea.name}")
                wildArea.addTrainer(pokemonTrainer)

            if not alreadyexists:
                self.areaList.append(wildArea)

            logger.debug(f"FINISHED {areaName} TRAINERS")
            logger.debug("FINISHED GAME DATA")

    def addSaveFileData(self, saveFileJson):
        """updates the self.arealist with the savefile"""
        #remove dictionary from json
        try:
            self.badge = saveFileJson.pop(0)["_badge"]
        except KeyError as e:
            logger.debug("badges not found, defaulting to 0")

        for area in saveFileJson:
            areaName = area["_name"]
            #loop through each area
            for areaObject in self.areaList:
                if areaObject.name == areaName:
                    #add trainers defeated status
                    for trainer in area["_trainers"]:
                        #check if trainer has been defeated
                        if area["_trainers"][trainer]["_defeated"]:
                            #add defeated to the arealist
                            areaObject.trainers[trainer].defeated = True
                            #set all trainer pokemon to defeated
                            for pokemonIndex, _ in enumerate(areaObject.trainers[trainer].pokemon): 
                                #True in case it is wrongly saved in the save file
                                areaObject.trainers[trainer].pokemon[pokemonIndex].defeated = True
                        else:
                            #trainer undefeated, look at pokemon
                            areaObject.trainers[trainer].defeated = False
                            for pokemonAmount, pokemon in enumerate(area["_trainers"][trainer]["_pokemon"]):
                                #keep track of defeated pokemon
                                defeated = 0
                                for pokemonObject in areaObject.trainers[trainer].pokemon:
                                    if pokemonObject.name == pokemon["_name"]:
                                        pokemonObject.defeated = pokemon["_defeated"]
                                        if pokemonObject.defeated: defeated += 1
                                if defeated == pokemonAmount:
                                    #all pokemon are defeated, set trainer to defeated
                                    areaObject.trainers[trainer].defeated = True

                    #add items picked up
                    #items that are not picked up don't get saved by default, still check just in case
                    for item in area["_items"]:
                        if area["_items"][item]["_grabbed"]:
                            # print(type(area["_items"][item]["_grabbed"]))
                            # print(f"changed item: {item}")
                            areaObject.items[item].grabbed = True
                        else:
                            areaObject.items[item].grabbed = False

                    #add encounters caught on route
            break


    def checkVarExistsJsonDump(self, attribute, json, value = "n/a"):
        """checks whether a variable exists in a json else returns value or defaults to n/a"""
        try:
            x = json[attribute]
        except KeyError as e:
            x = value
        return x

    def getFromJSON(self, object, json, notWanted = []):
        """function that reads the attributes of an object and completes them given the correct json"""
        defaultValues = {}
        notWanted = [*notWanted]
        #removes all the __variables and methods (including setters and getters from property methods) from the attributes list
        attributes = [attribute for attribute in dir(object) if not attribute.startswith('__') \
                      and not callable(getattr(object, attribute)) and not isinstance(getattr(type(object), attribute, None), property)]
        #remove all the class variables from the attributes list, [:] makes a copy of the list instead of making a secondary list
        for attribute in attributes[:]:
            if hasattr(type(object), attribute): #need the type of object else all variables will be removed
                attributes.remove(attribute)
                if "default" in attribute:
                    #remove default from attribute
                    keyName = attribute.replace("default", "")
                    #decapitalize the actual variable
                    keyName = keyName[0].lower() + keyName[1:]
                    #the attribute 100% exists, so no default for the getattr
                    defaultValues[keyName] = getattr(object, attribute)
                #print(f"removed: {attribute}")
        #remove not wanted variables
        for variable in notWanted[:]:
            if variable in attributes:
                attributes.remove(variable)
        
        #add correct values to the variables of the object
        for attribute in attributes:
            default = "n/a"
            if attribute in defaultValues.keys():
                default = defaultValues[attribute]
            #get the default value for an attribute if it is given as class variable
            attributeValue = self.checkVarExistsJsonDump(attribute, json, getattr(object, attribute, default))
            setattr(object, attribute, attributeValue)
        #print(object.name)
        return object



    

    

def checkGames():
    gameFolder = os.path.join(os.path.dirname(os.getcwd()), "games")
    #walks down the directory for other directories, retrieves the names and puts them in a list
    games = [gameName for gameName in next(os.walk(gameFolder))[1] if gameName != "Generic"]
    #no games found
    if not games:
        return ["new"]
    games.append("new")
    return games

def checkForSaveFileDirectory(gameFolder):
    """checks if the directory existst otherwise creates it, returns 1 when succesful else 0"""
    #if savefile directory doesn't exists
    if not os.path.isdir(gameFolder):
        logger.info(f"creating new directory {gameFolder} - TODO")
        #os.mkdir(gameFolder)

def getSaveFiles(gameName):
    """returns a list of the attempts made with a 'new' option"""
    gameFolder = os.path.join(os.path.dirname(os.getcwd()), "games", gameName, "saveFiles")
    checkForSaveFileDirectory(gameFolder)
    #get every file, [0] because it returns a list inside of a list
    saveFiles = [x[2] for x in os.walk(gameFolder)][0]
    #keep files with attempt in its name, and remove the '.txt'
    saveFiles = [x[:-4] for x in saveFiles if("attempt" in x)] 
    #give the option to make a new saveFile
    saveFiles.append("new")

    return saveFiles
    
# def addNewSaveFile():
#     #"new" has purposely not been removed, now len == attempt
#     saveFiles = self.getSaveFiles()
#     number = len(saveFiles)
#     #create the file then close it
#     open(f"{self.saveFileFolder}/attempt {number}.txt", "x").close()




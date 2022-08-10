from games.area import Area
from games.trainer import Trainer
from games.pokemon import Pokemon
from games.item import Item
from readFormattedData import readFormattedData

import json
txtfile = "trainerData.txt"

class MainGame():
    def __init__(self):
        self.file = None
        self.areaList = []
        self.readData = None


    def writeToFile(self):
        with open(self.file, "w") as file:
            file.truncate()
            file.write(json.dumps(self.areaList, default = vars, indent = 1))

    def readFromFile(self):
        with open(self.file, "r") as file:
            try:
                self.readData = json.load(file)
                self.convertDataToObjects()
            except json.JSONDecodeError:
                print("no save data found")
    
    def retrieveEncounterData(self):
        self.areaList = readFormattedData('sacredGoldCorrectData').returnAreaList()
                
    def convertDataToObjects(self):
        #get all the data from the text file
        for area in self.readData:
            areaName = area["_name"]
            startLine = area["_startLine"]
            wildArea = Area(areaName)
            wildArea.startLine = startLine


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
                    trainerPokemon = Pokemon(pokemonName, pokemonLevel)
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
            self.areaList.append(wildArea)

class SacredGold(MainGame):
    def __init__(self):
        super().__init__()
        self.file = "trainerData.txt"
        self.retrieveEncounterData()

        #self.readFromFile()
        #self.writeToFile()


game1 = SacredGold()
# route1 = Area("Route 1", 5)
# route2 = Area("Route 2", 16)

# trainer1 = Trainer("Falkner")
# trainer2 = Trainer("Maarten")
# pokemon1 = Pokemon("charmander", 60)
# pokemon2 = Pokemon("squirtle", 75)
# pokemon3 = Pokemon("Alakazam", 15)

# pokemon1.moves = "Tackle"
# pokemon1.moves = "Flamethrower"
# pokemon2.moves = "Pound"
# pokemon2.moves = "Surf"
# pokemon3.moves = "psychic"

# trainer1.pokemon = pokemon2
# trainer1.pokemon = pokemon3
# trainer2.pokemon = pokemon1
# trainer2.pokemon = pokemon2

# item1 = Item("Master Ball")
# item2 = Item("Oran Berry")
# item3 = Item("Choice Scarf")

# route1.trainers = trainer1
# route2.trainers = trainer2
# route2.trainers = trainer1

# route1.item = item1
# route1.item = item3
# route2.item = item2


# game1.areaList.append(route1)
# game1.areaList.append(route2)

# print(route1._items)
# game1.writeToFile()



# import os
# import requests
# imageUrl = "https://play.pokemonshowdown.com/sprites/gen5/"

# r = requests.get(imageUrl).content

# with open('abra.txt', 'wb') as handler:
#     handler.write(r)

# with open('abra.txt', 'r') as file:
#     global readData
#     readData = file.readlines()

# with open('abra.txt', 'w') as writer:
#     for line in readData:
#         if "a href" in line and ".png" in line:
#             line = line.split('"')
#             writer.write(line[7] + '\n')
    
# with open('abra.txt', 'r') as file:
#     data = file.readlines()
#     for index, line in enumerate(data):
#         data[index] = line.replace('\n', '')
    
#     for index, line in enumerate(data):
#         pokemon = str(imageUrl + line)
#         w = requests.get(pokemon).content
#         correctFolder = str(os.getcwd()+ '\sprites\pokemon')
#         correctFile = os.path.join(correctFolder, line)
#         #print(correctFile)
#         open(correctFile, 'wb').write(w)
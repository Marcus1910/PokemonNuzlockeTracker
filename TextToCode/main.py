from area import Area
from trainer import Trainer
from pokemon import Pokemon

import json
txtfile = "trainerData.txt"
class MainGame():
    def __init__(self, file):
        self.file = file
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
                
    def convertDataToObjects(self):
        #get all the data from the text file
        for area in self.readData:
            areaName = area["_name"]
            startLine = area["_startLine"]
            wildArea = Area(areaName, startLine)

            #trainer data and amount of trainers
            trainers = area["_trainers"]
            for trainer in trainers:
                trainerName = trainer["_name"]
                pokemonTrainer = Trainer(trainerName)
                pokemonTrainer.trainerType = trainer["_trainerType"]
                pokemonTrainer.gender = trainer["_gender"]
                #grab all atributes a pokemon could have
                for pokemon in trainer["_pokemon"]:
                    pokemonName = pokemon["_name"]
                    pokemonLevel = pokemon["_level"]
                    trainerPokemon = Pokemon(pokemonName, pokemonLevel)
                    trainerPokemon.gender = pokemon["_gender"]
                    trainerPokemon.ability = pokemon["_ability"]
                    trainerPokemon.heldItem = pokemon["_heldItem"]
                    #give the moves to the pokemon
                    moves = pokemon["_moves"]
                    for move in range(len(moves)):
                        trainerPokemon.moves = moves[move]
                    pokemonTrainer.pokemon = trainerPokemon
                wildArea.trainers = pokemonTrainer
            self.areaList.append(wildArea)

class SacredGold(MainGame):
    def __init__(self, file):
        super().__init__(file)

# game = MainGame()
# game.readFromFile()
# game.writeToFile()

game1 = SacredGold(txtfile)
game1.readFromFile()
print(game1.readData)

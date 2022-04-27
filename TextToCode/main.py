from area import Area
from trainer import Trainer
from pokemon import Pokemon

import json

#length from readData is amount of areas
#TODO convert areaData back to classes
areaList = []
readData = None


def writeToFile():
    with open("trainerData.txt", "w") as file:
        file.truncate()
        file.write(json.dumps(areaList, default = vars, indent = 1))

def readFromFile():
    global readData
    with open("trainerData.txt", "r") as file:
        try:
            readData = json.load(file)
            convertDataToObjects()
        except json.JSONDecodeError:
            print("no save data found")
            
def convertDataToObjects():
    #get all the data from the text file
    for index, area in enumerate(readData):
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
        areaList.append(wildArea)




            
readFromFile()
#area = areaList[0]
#area.name = "kutzooi"
writeToFile()


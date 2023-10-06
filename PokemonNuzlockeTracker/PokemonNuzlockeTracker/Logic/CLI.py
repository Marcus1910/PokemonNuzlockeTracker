from games import MainGame
from trainer import Trainer
from trainerPokemon import TrainerPokemon
from item import Item
from trainerPokemon import Pokemon

class CLI():
    game = MainGame("SacredGold", 'attempt 1.txt')
    print(game.badge)
    listAreas = game.retrieveGameData()
    newBark = listAreas[0]
    trainers = newBark.trainers
    items = newBark.items
    encounters = newBark.encounters
    # geodude = Pokemon("Geodude", 15)
    # listAreas[0].encounteredPokemon["Geodude"] = geodude

    larry = Trainer("Larry")
    squirtle = TrainerPokemon("squirtle", 25)
    charmander = TrainerPokemon("Charmander", 50)
    listAreas[0].trainers["Larry"].pokemon[1].defeated = True
    for trainer in trainers.values():
       print(trainer)
    berry = Item("Oran Berry", True)
    chesto = Item("Chesto Berry", True)

    listAreas[0].items["Chesto Berry"] = chesto
    listAreas[0].items["Oran Berry"] = berry
    
    # print(listAreas[0].items)

    #     for pokemon in trainer.pokemon:
    #         print(pokemon)
    # for item in items.values():
    #     print(item.name)



    game.writeToFile()
    #print(items)
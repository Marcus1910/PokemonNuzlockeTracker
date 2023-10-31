from games import MainGame
from trainer import Trainer
from trainerPokemon import TrainerPokemon
from item import Item
from trainerPokemon import Pokemon

class CLI():
   game = MainGame("SacredGold", 'attempt 1')
   print(game.badge)
   listAreas = game.retrieveGameData()
   newBark = listAreas[0]
   trainers = newBark.trainers
   items = newBark.items
   encounters = newBark.encounters

   print(trainers["Larry"])
    # geodude = Pokemon("Geodude", 15)
    # listAreas[0].encounteredPokemon["Geodude"] = geodude

   #  larry = Trainer("Larry"
   squirtle = TrainerPokemon("alakazam", 25)
   charmander = TrainerPokemon("machamp", 50)
   # listAreas[0].trainers["Morty"].pokemon = squirtle
   # listAreas[0].trainers["Morty"].pokemon = charmander

   #  for trainer in trainers.values():
   #     print(trainer)
   #  berry = Item("Oran Berry", True)
   #  chesto = Item("Chesto Berry", True)

   #  listAreas[0].items["Chesto Berry"] = chesto
   #  listAreas[0].items["Oran Berry"] = berry
    
    # print(listAreas[0].items)

    #     for pokemon in trainer.pokemon:
    #         print(pokemon)
    # for item in items.values():
    #     print(item.name)



   game.writeToFile()
    #print(items)
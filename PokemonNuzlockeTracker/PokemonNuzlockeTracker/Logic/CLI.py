from games import MainGame
from trainer import Trainer
from trainerPokemon import TrainerPokemon
from item import Item
from trainerPokemon import Pokemon
from loggerConfig import logicLogger as logger

class CLI():
   game = MainGame("SacredGold", 'attempt 1')
   listAreas = game.retrieveGameData()
   newBark = listAreas[0]
   trainers = newBark.trainers
   items = newBark.items
   encounters = newBark.encounters
   trainer = trainers["JonkoMon"]
   trainer.removePokemon("Air")

   magikarp = TrainerPokemon("magikarp", 55)

   trainer.editPokemon(magikarp, newPokemonName = "Electivire")

   # print(trainers)
   # # newTrainer = Trainer("Gary")
   # # squirtle = TrainerPokemon("Electivire", 25)
   # Electro = newBark.trainers["electro"]
   # charmander = TrainerPokemon("RayQuaza", 50)
   # Electro.pokemon = charmander

   # newBark.editTrainer(Electro)
   # newTrainer.pokemon = squirtle

   # newBark.addTrainer(newTrainer)
   # print(trainers)
   # newTrainer.pokemon = charmander 
   # newBark.editTrainer(newTrainer)
   # print(trainers)
   # newBark.removeTrainer(newTrainer.name)
   print(trainer)

   # game.writeToFile()
   #print(items)
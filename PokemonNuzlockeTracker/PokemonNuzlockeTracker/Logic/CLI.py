from games import MainGame
from trainer import Trainer
from pokemon import TrainerPokemon
from item import Item
from pokemon import Pokemon, PlayerPokemon
from loggerConfig import logicLogger as logger
from fileRetriever import FileRetriever

class CLI():
   def __init__(self, operatingSystem):
      fileRetriever = FileRetriever(operatingSystem)
      #set fileretriever variables correctly, TODO update earlier
      gameName = "SacredGold"
      fileRetriever.setFolderVariables(gameName)
      #fileRetriever.addNewPokemonGame(gameName)
      game = MainGame(fileRetriever, gameName, "attempt 1")
      newBark = game.areaList[0]
      print(newBark)
      Magikarp = PlayerPokemon("magikarp", 55)
      Charmander = PlayerPokemon("charmander", 34)
      game.catchPokemon(Magikarp,  "New Bark Town")
      print(game.arena)
      game.removeFromArena(Charmander)
      print(game.arena)
      game.writeToFile()


      # newBark = listAreas[0]
      # trainers = newBark.trainers
      # items = newBark.items
      # encounters = newBark.encounters
      # trainer = trainers["Larry"]
      # trainer.removePokemon("Air")

      # magikarp = TrainerPokemon("magikarp", 55)

      # trainer.editPokemon(magikarp, newPokemonName = "Electivire")

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
      # print(trainer)

      # game.writeToFile()
      #print(items)
import os
import json

from loggerConfig import logger
from Logic.databaseModels.game import Game
from Logic.databaseModels.location import Location#, locationAlreadyExists
from Logic.databaseModels.trainer import Trainer
from Logic.databaseModels.pokemon import TrainerPokemon, Pokemon

class Reader():
    def __init__(self, IDGame: int, session): #gameRecord
        print(os.getcwd())
        self.jsonPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "PokemonNuzlockeTracker/games/SacredGold/data/SacredGoldGameData.txt")
        self.IDGame = IDGame
        self.session = session
        
        self.pokedexJsonFile = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "PokemonNuzlockeTracker/games/Generic/data/pokedex.json")
        
        # data = self.readJson(self.jsonPath)
        # if data == '':
        #     logger.error("could not read json file")
        
        # self.storeDataInDatabase(data)
        
    def readJson(self, file: str) -> str:
        data = ''
        with open(file, 'r') as dataFile:
            try:
                data = json.load(dataFile)
            except json.JSONDecodeError as e:
                logger.error(f"json failed to load {e}")
        return data

    def storeDataInDatabase(self, data: str) -> bool:
        for location in data:
            print(location)
            # if locationAlreadyExists(self.IDGame, location["_name"]):
            #    continue
            locationObject = Location(location["_name"], self.IDGame, noBadgesRequired = location["_accessible"])
            print(locationObject)
            self.session.add(locationObject)
            self.session.commit()
            # for trainer in location["_trainers"]:
            #     # if trainerAlreadyExists:
            #     #     continue
            #     trainerObject = Trainer(locationObject.IDLocation, "Youngster", trainer["_name"], "M", )
            #     print(trainerObject)
            #     for trainerPokemon in trainer["_pokemon"]:
            #         trainerPokemonObject = TrainerPokemon()
            
            # for encounterPokemon in location["_encounters"]:
    
    def readBasePokedexData(self, session):
        if not os.path.isfile(self.pokedexJsonFile):
            logger.error("pokedex path is incorrect, could not read data")
            exit()
        pokedexJson = self.readJson(self.pokedexJsonFile)
        for pokedexEntry in pokedexJson:
            data = pokedexJson[pokedexEntry]
            if len(data["types"]) == 1:
                type2 = None
            else:
                type2 = data["types"][1]
            
            pokemon = Pokemon(data["name"], data["num"], data["types"][0], type2)
            session.add(pokemon)
            if pokemon.name == "MissingNo.":
                #laatste echte pokemon
                return
                
                
                
            

            
    
    
    
                    

    
import os
import json

from loggerConfig import logger
from Logic.databaseModels.game import Game
from Logic.databaseModels.location import Location#, locationAlreadyExists
from Logic.databaseModels.trainer import Trainer
from Logic.databaseModels.pokemon import TrainerPokemon, Pokemon
from Logic.databaseModels import Ability, AbilitySlot, PokemonAbilities

class Reader():
    def __init__(self, IDGame: int, session, dataRetriever): #gameRecord
        print(os.getcwd())
        self.jsonPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "PokemonNuzlockeTracker/games/SacredGold/data/SacredGoldGameData.txt")
        self.IDGame = IDGame
        self.session = session
        self.dataRetriever = dataRetriever
        
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
        """adds base pokemon, abilities"""
        if not os.path.isfile(self.pokedexJsonFile):
            logger.error("pokedex path is incorrect, could not read data")
            return
        pokedexJson = self.readJson(self.pokedexJsonFile)
        for pokedexEntry in pokedexJson:
            data = pokedexJson[pokedexEntry]
            IDPokemon = self.dataRetriever.getIDPokemonByName(data["name"])
            
            if IDPokemon is None:     
                if len(data["types"]) == 1:
                    type2 = None
                else:
                    type2 = data["types"][1]
            
                pokemon = Pokemon(data["name"], data["num"], data["types"][0], type2)
                if not self.dataRetriever.insertRecord(pokemon):
                    logger.error("could not insert pokemon")
                    return
                
                IDPokemon = self.dataRetriever.getIDPokemonByName(data["name"])
            
            for abilitySlot, abilityName in data["abilities"].items():
                self.addPokemonAbility(session, abilityName, abilitySlot, IDPokemon)

            if data["name"] == "MissingNo.":
                #last actual pokemon
                return
            session.commit()
            
    
    def addPokemonAbility(self, session, abilityName, abilitySlot, IDPokemon):
        """checks whether ability already exists otherwise creates it and links it to the pokemon"""
        IDAbility = self.dataRetriever.getIDAbilityByName(abilityName)
        if IDAbility is None:
            ability = Ability(abilityName)
            if not self.dataRetriever.insertRecord(ability):
                logger.error("could not insert Ability")
                return
            IDAbility = self.dataRetriever.getIDAbilityByName(abilityName)
        
        if self.dataRetriever.doesPokemonAbilitiesExist(IDPokemon, IDAbility, abilitySlot):
            #logger.info("ability pokemon combination already exists")
            return
        
        pokemonAbilities = PokemonAbilities(IDPokemon, IDAbility, abilitySlot)
        session.add(pokemonAbilities)

    def addPokemonBasestats(self):
        """TODO add basestats to pokemon in another table"""
        return
        
            
        
        
        
        
        
                
                
            

            
    
    
    
                    

    
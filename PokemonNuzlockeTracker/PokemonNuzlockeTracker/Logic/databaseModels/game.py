from sqlalchemy import ForeignKey, Column, String, Integer, Boolean, func
from sqlalchemy.orm import Session, relationship
import os
from time import sleep
from enum import Enum
from .base import Base, StrictInteger

from loggerConfig import logicLogger as logger


newGameString = "New Game"
newAttemptString = "Select attempt"
newLocationString = "New Location"
chooseLocationString = "Select Location"
newTrainerString = "New trainer"
editTrainerString = "Edit Trainer"
chooseTrainerString = "Select trainer"

#change to settings
opaque = (1, 1, 1, 0.6)
standardColor = (1, 1, 1, 1)
red = (1, 0, 0, 1)
blue = (0, 0, 1, 1) 
green = (0, 1, 0, 1)

spriteFolder = os.path.join(os.path.dirname(os.getcwd()), "images", "sprites")
pokemonSprites = os.path.join(spriteFolder, "pokemon")
trainerSprites = os.path.join(spriteFolder, "trainers")
itemSprites = os.path.join(spriteFolder, "items")

class NLS(Enum):
    GENDER = 1
    TRAINER = 2
    TRAINERTYPE = 3
    ABILITY = 4
    GAME = 5
    ITEM = 6
    POKEMON = 7
    POKEMONABILITY = 8
    TYPING = 9
    LOCATION = 10
    BASEGAME = 11
    ATTEMPT = 12

class Game(Base):
    __tablename__ = "Game"

    IDGame = Column("IDGame", StrictInteger, primary_key = True, autoincrement = True)
    name = Column("Name", String, nullable = False)
    gen = Column("Gen", StrictInteger, nullable = False)
    IDParentGame = Column("IDParentGame", ForeignKey("Game.IDGame"))
    hasPhysicalSpecialSplit = Column("HasPhysicalSpecialSplit", Boolean, default = True)
    encountersPerLocation = Column("EncountersPerLocation", Integer, default = 1)
    
    
    attempt = relationship("Attempt", back_populates = "game")

    def __init__(self, name: str, gen: int, IDParentGame: int = None, hasPhysicalSpecialSplit: bool = True, encountersPerLocation: int = 1):
        self.name = name.capitalize()
        self.gen = int(gen)
        self.IDParentGame = IDParentGame
        self.hasPhysicalSpecialSplit = hasPhysicalSpecialSplit
        self.encountersPerLocation = encountersPerLocation
  
    def __repr__(self):
        return f"{self.IDGame, self.name, self.gen, self.IDParentGame, self.hasPhysicalSpecialSplit, self.encountersPerLocation}"

def gameExists(session: Session, gameName: str):
    return False if session.query(Game).filter(func.lower(Game.name) == func.lower(gameName)).first() == None else True

def addGame(session: Session, name: str, gen: int, IDParentGame = None, hasPhysicalSpecialSplit = None, encountersPerLocation = 1) -> Game:
    newGame = Game(name, gen, IDParentGame, hasPhysicalSpecialSplit, encountersPerLocation)
    session.add(newGame)
    session.commit()
    return newGame

def getGameRecord(session, IDGame: int) -> Game | None:
    game = session.query(Game).get(IDGame)
    return game

def getGames(session, text: str = ""):
    return {game.IDGame: game.name for game in session.query(Game).filter(Game.name.like(f"%{text}%")).all()}
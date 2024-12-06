from sqlalchemy import ForeignKey, Column, String, Integer, Boolean, Float
from sqlalchemy.orm import Session, relationship
import os
from time import sleep
from .base import Base, StrictInteger

from loggerConfig import logicLogger as logger


newGameString = "New Game"
newAttemptString = "select the attempt"
newLocationString = "New Location"
chooseLocationString = "choose an Location"
newTrainerString = "New trainer"
chooseTrainerString = "Choose a trainer"

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

def addGame(session: Session, name: str, gen: int, IDParentGame = None, hasPhysicalSpecialSplit = None, encountersPerLocation = 1) -> Game:
    newGame = Game(name, gen, IDParentGame, hasPhysicalSpecialSplit, encountersPerLocation)
    session.add(newGame)
    session.commit()
    return newGame

def getGameFromGameName(session, GameName: str) -> Game | None:
    game = session.query(Game).filter(Game.name == GameName).first()
    return game
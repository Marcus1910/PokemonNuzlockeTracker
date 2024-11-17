from sqlalchemy import ForeignKey, Column, String, Integer, Boolean, Float
from sqlalchemy.orm import sessionmaker
import os
from .base import Base


newGameString = "New Game"
newAttemptString = "select the attempt"
newLocationString = "New Location"
chooseLocationString = "choose an Location"

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

	IDGame = Column("IDGame", Integer, primary_key = True, autoincrement = True)
	name = Column("Name", String, nullable = False)
	gen = Column("Gen", Integer, nullable = False)
	IDParentGame = Column("IDParentGame", ForeignKey("Game.IDGame"))
	hasPhysicalSpecialSplit = Column("HasPhysicalSpecialSplit", Boolean, default = True)
	encountersPerLocation = Column("EncountersPerLocation", Integer, default = 1)

	def __init__(self, name, gen, IDParentGame = None, hasPhysicalSpecialSplit = True, encountersPerLocation = 1):
		self.name = name
		self.gen = gen
		self.IDParentGame = IDParentGame
		self.hasPhysicalSpecialSplit = hasPhysicalSpecialSplit
		self.encountersPerLocation = encountersPerLocation

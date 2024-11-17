from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Boolean, Float, Table, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
#from PokemonNuzlockeTracker/PokemonNuzlockeTracker/Logic/Pokemon import Pokemon

Base = declarative_base()

class Typing(Base):
	__tablename__ = "Typing"

	IDTyping = Column("IDTyping", String, primary_key = True)
	name = Column("Name", String, nullable = False)

	def __init__(self, name):
		self.name = name

class TypeMatchup(Base):
	__tablename__ = "TypeMatchup"

	IDAttackingType = Column("IDAttackingType", ForeignKey("Typing.IDTyping"), primary_key = True)
	IDDefendingType = Column("IDDefendingType", ForeignKey("Typing.IDTyping"), primary_key = True)
	effectiveness = Column("Effectiveness", Float, nullable = False)

	def __init__(self, IDAttackingType, IDDefendingType, effectiveness):
		self.IDAttackingType = IDAttackingType
		self.IDDefendingType = IDDefendingType
		self.effectiveness = effectiveness

class Location(Base):
	__tablename__ = "Location"

	IDLocation = Column("IDLocation", Integer, primary_key = True, autoincrement = True)
	IDParentLocation = Column("IDParentLocation", ForeignKey("Location.IDLocation"))
	name = Column("Name", String, nullable = False)
	noBadgesRequired = Column("NoBadgesRequired", Integer, default = 0, nullable = False)
	canCatchPokemon = Column("'CanCatchPokemon", Boolean, default = False, nullable = False)

	def __init__(self, IDParentLocation, name, noBadgesRequired = 0, canCatchPokemon = False):
		self.IDParentLocation = IDParentLocation
		self.name = name
		self.noBadgesRequired = noBadgesRequired
		self.canCatchPokemon = canCatchPokemon

class Item(Base):
	__tablename__ = "Item"

	IDItem = Column("IDItem", Integer, primary_key = True, autoincrement = True)
	name = Column("Name", String, nullable = False)
	description = Column("Description", String)
	isKeyItem = Column("IsKeyItem", Boolean, default = False, nullable = False)

	def __init__(self, name, description = None, isKeyItem = False):
		self.name = name
		self.description = description
		self.isKeyItem = isKeyItem

class FieldItem(Base):
	__tablename__ = "FieldItem"

	IDFieldItem = Column("IDFieldItem", Integer, primary_key = True, autoincrement = True)
	IDItem = Column("IDItem", ForeignKey("Item.IDItem"), nullable = False)
	IDLocation = Column("IDLocation", ForeignKey("Location.IDLocation"), nullable = False)
	locationSpecific = Column("LocationSpecific", String)
	grabbed = Column("Grabbed", Boolean, default = False)

	def __init__(self, IDItem, IDLocation, locationSpecific = None, grabbed = False):
		self.IDItem = IDItem
		self.IDLocation = IDLocation
		self.locationSpecific = locationSpecific
		self.grabbed = grabbed

class Gender(Base):
	__tablename__ = "Gender"

	IDGender = Column("IDGender", String, primary_key = True)

	def __init__(self, IDGender):
		self.IDGender = IDGender

class TrainerType(Base):
	__tablename__ = "TrainerType"

	IDTrainerType = Column("IDTrainerType", Integer, primary_key = True, autoincrement = True)
	name = Column("name", String, nullable = False)
	imageName = Column("ImageName", String)
	IDGender = Column("IDGender", ForeignKey("Gender.IDGender"))

	def __init__(self, name, imageName, IDGender):
		self.name = name
		self.imageName =imageName
		self.IDGender = IDGender

class Trainer(Base):
	__tablename__ = "Trainer"

	IDTrainer = Column("IDTrainer", Integer, primary_key = True, autoincrement = True)
	IDLocation = Column("IDLocation", ForeignKey("Location.IDLocation"), nullable = False)
	IDTrainerType = Column("IDTrainerType", ForeignKey("TrainerType.IDTrainerType"))
	name = Column("Name", String, nullable = False)
	IDGender = Column("IDGender", ForeignKey("Gender.IDGender"))
	isDefeated = Column("isDefeated", Boolean, default = False)
	pokeDollars = Column("PokeDollars", Integer)
	isOptional = Column("IsOptional", Boolean, default = False)
 
class Pokemon(Base):
	__tablename__ = "Pokemon"

	IDPokemon = Column("IDPokemon", Integer, primary_key = True, autoincrement = True)
	name = Column("Name", String, nullable = False)
	dexNo = Column("DexNo", Integer)
	IDTyping1 = Column("IDTyping1", ForeignKey("Typing.IDTyping"), nullable = False)
	IDTyping2 = Column("IDTyping2", ForeignKey("Typing.IDTyping"))
	IDHeldItem = Column("IDHeldItem", ForeignKey("Item.IDItem"))

	def __init__(self, name, dexNo, IDTyping1, IDTyping2, IDHeldItem):
		self.name = name
		self.dexNo = dexNo
		self.IDTyping1 = IDTyping1
		self.IDTyping2 =IDTyping2
		self.IDHeldItem = IDHeldItem

class Ability(Base):
	__tablename__ = "Ability"

	IDAbility = Column("IDAbility", Integer, primary_key = True, autoincrement = True)
	name = Column("Name", String, nullable = False)
	description = Column("Description", String)
	effect = Column("Effect", String)
	chance = Column("Chance", Integer)

	def __init__(self, name, description, effect, chance):
		self.name = name
		self.description = description
		self.effect = effect
		self.chance = chance

class AbilitySlot(Base):
	__tablename__ = "AbilitySlot"
	IDAbilitySlot = Column("IDAbilitySlot", String, primary_key = True)

	def __init__(self, IDAbilitySlot):
		self.IDAbilitySlot = IDAbilitySlot

class PokemonAbilities(Base):
	__tablename__ = "PokemonAbilities"

	IDPokemon = Column("IDPokemon", ForeignKey("Pokemon.IDPokemon"), primary_key = True)
	IDAbility = Column("IDAbility", ForeignKey("Ability.IDAbility"), primary_key = True)
	IDAbilitySlot = Column("AbilitySlot", ForeignKey("AbilitySlot.IDAbilitySlot"), nullable = False)

	def __init__(self, IDPokemon, IDAbility, IDAbilitySlot):
		self.IDPokemon = IDPokemon
		self.IDAbility = IDAbility
		self.IDAbilitySlot = IDAbilitySlot

class PokemonMoveCategory(Base):
	__tablename__ = "PokemonMoveCategory"
	IDPokemonMoveCategory = Column("IDPokemonMoveCategory", String, primary_key = True)

	def __init__(self, IDPokemonMoveCategory):
		self.IDPokemonMoveCategory = IDPokemonMoveCategory

class PokemonMove(Base):
	__tablename__ = "PokemonMove"

	IDPokemonMove = Column("IDPokemonMove", Integer, primary_key = True, autoincrement = True)
	name = Column("Name", String, nullable = False)
	IDTyping =  Column("IDTyping", ForeignKey("Typing.IDTyping"), nullable = False)
	IDPokemonMoveCategory = Column("IDPokemonMoveCategory", ForeignKey("PokemonMoveCategory.IDPokemonMoveCategory"), nullable = False)
	basePower = Column("BasePower", Integer)
	accuracy = Column("Accuracy", Integer)
	powerPoints = Column("PowerPoints", Integer)
	maxPowerPoints = Column("MaxPowerPoints", Integer)
	description = Column("Description", String)
	effect = Column("Effect", String)

	def __init__(self, name, IDTyping, IDPokemonMoveCategory, basePower = None, accuracy = None, powerPoints = None, maxPowerPoints = None, description = None, effect =None ):
		self.name = name
		self.IDTyping = IDTyping
		self.IDPokemonMoveCategory = IDPokemonMoveCategory
		self.basePower = basePower
		self.accuracy = accuracy
		self.powerPoints = powerPoints
		self.maxPowerPoints = maxPowerPoints
		self.description = description
		self.effect = effect


class TrainerPokemon(Base):
	__tablename__ = "TrainerPokemon"

	IDTrainerPokemon = Column("IDTrainerPokemon", Integer, primary_key = True, autoincrement = True)
	IDTrainer = Column("IDTrainer", ForeignKey("Trainer.IDTrainer"), nullable = False)
	IDPokemon = Column("IDPokemon", ForeignKey("Pokemon.IDPokemon"), nullable = False)
	IDAbilitySlot = Column("IDAbilitySlot", ForeignKey("AbilitySlot.IDAbilitySlot"))
	gender = Column("Gender", ForeignKey("Gender.IDGender"))
	isDefeated = Column("isDefeated", Boolean, default = False, nullable = False)
	IDHeldItem = Column("IDHeldItem", ForeignKey("Item.IDItem"))
	IDPokemonMove1 = Column("IDMove1", ForeignKey("PokemonMove.IDPokemonMove"))
	IDPokemonMove2 = Column("IDMove2", ForeignKey("PokemonMove.IDPokemonMove"))
	IDPokemonMove3 = Column("IDMove3", ForeignKey("PokemonMove.IDPokemonMove"))
	IDPokemonMove4 = Column("IDMove4", ForeignKey("PokemonMove.IDPokemonMove"))

	def __init__(self, IDTrainer, IDPokemon, IDAbilitySlot, gender = None, isDefeated = None, IDHeldItem = None, IDPokemonMove1 = None, IDPokemonMove2 = None, IDPokemonMove3 = None, IDPokemonMove4 = None):
		self.IDTrainer = IDTrainer
		self.IDPokemon = IDPokemon
		self.AbilitySlot = IDAbility
		self.gender = gender
		self.isDefeated = isDefeated 
		self.IDHeldItem = IDHeldItem 
		self.IDPokemonMove1 = IDPokemonMove1
		self.IDPokemonMove2 = IDPokemonMove2
		self.IDPokemonMove3 = IDPokemonMove3
		self.IDPokemonMove4 = IDPokemonMove4

class WildPokemon(Base):
	__tablename__ = "WildPokemon"

	IDWildPokemon = Column("IDWildPokemon", Integer, primary_key = True, autoincrement = True)
	IDPokemon = Column("IDPokemon", ForeignKey("Pokemon.IDPokemon"), nullable = False)
	IDLocation =Column("IDLocation", ForeignKey("Location.IDLocation"), nullable = False)
	catchRate = Column("CatchRate", Integer)
	minimumLevel = Column("MinimumLevel", Integer)
	maximumLevel = Column("MaximumLevel", Integer)
	IDHeldItem = Column("IDHeldItem", ForeignKey("Item.IDItem"))

	def __init__(self, IDPokemon, IDLocation, catchRate = None, minimumLevel = None,  maximumLevel = None, IDHeldItem = None):
		self.IDPokemon = IDPokemon
		self.IDLocation = IDLocation
		self.catchRate = catchRate
		self.minimumLevel = minimumLevel
		self.maximumLevel = maximumLevel
		self.IDHeldItem = IDHeldItem

class PlayerPokemon(Base):
	__tablename__ = "PlayerPokemon"

	IDPlayerPokemon = Column("IDPlayerPokemon", Integer, primary_key = True, autoincrement = True)
	IDPokemon = Column("IDPokemon", ForeignKey("Pokemon.IDPokemon"), nullable = False)
	isDead = Column("IsDead", Boolean, nullable = False, default = False)
	IDAbilitySlot = Column("IDAbilitySlot", ForeignKey("AbilitySlot.IDAbilitySlot"))
	IDGender = Column("IDGender", ForeignKey("Gender.IDGender"))
	nickName = Column("Nickname", String)
	IDHeldItem = Column("IDHeldItem", ForeignKey("Item.IDItem"))
	IDPokemonMove1 = Column("IDMove1", ForeignKey("PokemonMove.IDPokemonMove"))
	IDPokemonMove2 = Column("IDMove2", ForeignKey("PokemonMove.IDPokemonMove"))
	IDPokemonMove3 = Column("IDMove3", ForeignKey("PokemonMove.IDPokemonMove"))
	IDPokemonMove4 = Column("IDMove4", ForeignKey("PokemonMove.IDPokemonMove"))

	def __init__(self, IDPokemon, isDead, IDAbilitySlot = None, IDGender = None, nickName = None, IDHeldItem = None, IDPokemonMove1 = None, IDPokemonMove2 = None, IDPokemonMove3 = None, IDPokemonMove4 = None):
		self.IDPokemon = IDPokemon
		self.isDead = isDead
		self.IDAbilitySlot = IDAbilitySlot
		self.IDGender = IDGender
		self.nickName = nickName
		self.IDHeldItem = IDHeldItem
		self.IDPokemonMove1 = IDPokemonMove1
		self.IDPokemonMove2 = IDPokemonMove2
		self.IDPokemonMove3 = IDPokemonMove3
		self.IDPokemonMove4 = IDPokemonMove4

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

class Attempt(Base):
	__tablename__ = "Attempt"
 
	IDAttempt = Column("IDAttempt", Integer, primary_key = True, autoincrement = True)
	IDGame = Column("IDGame", ForeignKey("Game.IDGame"), nullable = False)
	attemptNumber = Column("AttemptNumber", Integer, nullable = False)

	def __init__(self, IDGame, attemptNumber):
		self.IDGame = IDGame
		self.attemptNumber = attemptNumber

engine = create_engine("sqlite:///mydb.db", echo = True)
engine.connect()

Base.metadata.create_all(bind = engine)
metadata = MetaData()

x = Table('Attempt', metadata, autoload_with=engine)
print(x.columns.keys())
Session = sessionmaker(bind = engine)
session = Session()

attempt = Attempt(1, 1)
session.add(attempt)
session.commit()


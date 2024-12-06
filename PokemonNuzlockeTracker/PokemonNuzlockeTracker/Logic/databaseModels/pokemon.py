from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from .base import Base

class Pokemon(Base):
    __tablename__ = "Pokemon"

    IDPokemon = Column("IDPokemon", Integer, primary_key = True, autoincrement = True)
    name = Column("Name", String, nullable = False)
    dexNo = Column("DexNo", Integer)
    IDTyping1 = Column("IDTyping1", ForeignKey("Typing.IDTyping"), nullable = False)
    IDTyping2 = Column("IDTyping2", ForeignKey("Typing.IDTyping"))
    IDHeldItem = Column("IDHeldItem", ForeignKey("Item.IDItem"))

    def __init__(self, name, dexNo, IDTyping1, IDTyping2 = None, IDHeldItem = None):
        self.name = name
        self.dexNo = dexNo
        self.IDTyping1 = IDTyping1
        self.IDTyping2 =IDTyping2
        self.IDHeldItem = IDHeldItem
    
    def __repr__(self):
        return f"name: {self.name}, type1: {self.IDTyping1}, type2: {self.IDTyping2}"

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
        self.AbilitySlot = IDAbilitySlot
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
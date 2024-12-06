from sqlalchemy import ForeignKey, Column, String, Integer
from .base import Base

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
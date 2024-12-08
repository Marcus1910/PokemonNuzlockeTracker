from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class Ability(Base):
    __tablename__ = "Ability"

    IDAbility = Column("IDAbility", Integer, primary_key = True, autoincrement = True)
    name = Column("Name", String, nullable = False)
    description = Column("Description", String)
    effect = Column("Effect", String)
    chance = Column("Chance", Integer)

    def __init__(self, name, description = None, effect = None, chance = None):
        self.name = name
        self.description = description
        self.effect = effect
        self.chance = chance
    
    def __repr__(self):
        return f"name: {self.name}"

def getIDAbilityByName(session, abilityName):
    return session.query(Ability.IDAbility).filter(Ability.name == abilityName).scalar()

class AbilitySlot(Base):
    __tablename__ = "AbilitySlot"
    IDAbilitySlot = Column("IDAbilitySlot", String, primary_key = True)

    def __init__(self, IDAbilitySlot):
        self.IDAbilitySlot = IDAbilitySlot

def fillAbilitySlotTable(session):
    abilitySlots = ["0", "1", "H", "S"]
    session.add_all([AbilitySlot(ability) for ability in abilitySlots])

class PokemonAbilities(Base):
    __tablename__ = "PokemonAbilities"

    IDPokemon = Column("IDPokemon", ForeignKey("Pokemon.IDPokemon"), primary_key = True)
    IDAbility = Column("IDAbility", ForeignKey("Ability.IDAbility"), primary_key = True)
    IDAbilitySlot = Column("AbilitySlot", ForeignKey("AbilitySlot.IDAbilitySlot"), nullable = False)

    def __init__(self, IDPokemon, IDAbility, IDAbilitySlot):
        self.IDPokemon = IDPokemon
        self.IDAbility = IDAbility
        self.IDAbilitySlot = IDAbilitySlot

def doesPokemonAbilitiesExist(session, IDPokemon, IDAbility, IDAbilitySlot) -> bool:
    record = session.query(PokemonAbilities).filter(PokemonAbilities.IDPokemon == IDPokemon).filter(PokemonAbilities.IDAbility == IDAbility).filter(PokemonAbilities.IDAbilitySlot == IDAbilitySlot).first()
    return False if record == None else True
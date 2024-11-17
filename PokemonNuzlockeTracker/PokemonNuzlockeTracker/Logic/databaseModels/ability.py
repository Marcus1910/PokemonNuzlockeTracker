from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

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
from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from .base import Base

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
from sqlalchemy import ForeignKey, Column, String, Float
from .base import Base

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
from sqlalchemy import ForeignKey, Column, Integer
from .base import Base

class Attempt(Base):
	__tablename__ = "Attempt"
 
	IDAttempt = Column("IDAttempt", Integer, primary_key = True, autoincrement = True)
	IDGame = Column("IDGame", ForeignKey("Game.IDGame"), nullable = False)
	attemptNumber = Column("AttemptNumber", Integer, nullable = False)

	def __init__(self, IDGame, IDAttempt, attemptNumber):
		self.IDGame = IDGame
		self.IDAttempt = IDAttempt
		self.attemptNumber = attemptNumber
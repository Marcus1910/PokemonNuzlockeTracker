from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from .base import Base

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
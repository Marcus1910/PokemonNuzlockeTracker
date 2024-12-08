from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from .base import Base
from .location import Location
from .pokemon import TrainerPokemon

class TrainerType(Base):
    __tablename__ = "TrainerType"

    IDTrainerType = Column("IDTrainerType", Integer, primary_key = True, autoincrement = True)
    name = Column("name", String, nullable = False)
    imageName = Column("ImageName", String)
    IDGender = Column("IDGender", ForeignKey("Gender.IDGender"))

    def __init__(self, name, imageName, IDGender):
        self.name = name
        self.imageName = imageName
        self.IDGender = IDGender

def fillTrainerTypeTable(session):
    session.add(TrainerType("Cynthia", "Cynthia.png", "F"))
    session.add(TrainerType("Alder", "Alder.png", "M"))
    

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
    
    def __init__(self, IDLocation: int, IDtrainerType: int, name: str, IDgender: str, isDefeated: bool = False, pokeDollars: int = 0, isOptional: bool = False):
        self.IDLocation = IDLocation
        self.IDTrainerType = IDtrainerType
        self.name = name
        self.IDGender = IDgender
        self.isDefeated = isDefeated
        self.pokeDollars = pokeDollars
        self.isOptional = isOptional  
    
    def changeDefeated(self) -> None:
        """inverts the defeated status"""
        self.isDefeated = not self.isDefeated
    
    def __repr__(self):
        return f"IDLocation: {self.IDLocation}, name: {self.name}, trainerType: {self.IDTrainerType}, gender: {self.IDGender}, defeated: {self.isDefeated}, dollars: {self.pokeDollars}, optional: {self.isOptional}" 
    

def getTrainers(session, locationRecord: Location):  
    trainerNames = [trainer.name for trainer in session.query(Trainer).filter(Trainer.IDLocation == locationRecord.IDLocation).all()]
    return trainerNames

def getTrainerRecordByName(session, locationRecord: Location, trainerName):
    return session.query(Trainer).filter(Trainer.IDLocation == locationRecord.IDLocation).filter(Trainer.name == trainerName).first()

def getIDTrainerPokemon(session, IDTrainer: int, IDLocation: int) -> list[int]:
    return [pokemon.IDTrainerpokemon for pokemon in session.query(TrainerPokemon, Trainer).join(TrainerPokemon).filter(TrainerPokemon.IDTrainer == IDTrainer).filter(Trainer.IDLocation == IDLocation).all()]
from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from .base import Base
from .game import newLocationString

class Location(Base):
    __tablename__ = "Location"

    IDLocation = Column("IDLocation", Integer, primary_key = True, autoincrement = True)
    IDParentLocation = Column("IDParentLocation", ForeignKey("Location.IDLocation"))
    IDGame = Column("IDGame", ForeignKey("Game.IDGame"), nullable = False)
    name = Column("Name", String, nullable = False)
    noBadgesRequired = Column("NoBadgesRequired", Integer, default = 0, nullable = False)
    canCatchPokemon = Column("'CanCatchPokemon", Boolean, default = False, nullable = False)

    def __init__(self, name, IDGame,  IDParentLocation = None, noBadgesRequired = 0, canCatchPokemon = False):
        self.name = name
        self.IDGame = IDGame
        self.IDParentLocation = IDParentLocation
        self.noBadgesRequired = noBadgesRequired
        self.canCatchPokemon = canCatchPokemon
    
    def __repr__(self):
        return f"ID: {self.IDLocation}, IDGame: {self.IDGame}, parentLocation: {self.IDParentLocation}, name: {self.name}"


def getLocations(session, attemptRecord, subName:str):
    locations = {location.IDLocation: location.name for location in session.query(Location).filter(Location.IDGame == attemptRecord.IDGame).filter(Location.name.like(f"%{subName}%")).all()}
    #locationNames = [location.name for location in session.query(Location).filter(Location.IDGame == attemptRecord.IDGame).filter(Location.name.like(f"%{subName}%")).all()]
    locations[0] = newLocationString
    print(locations)
    return locations

def getLocationRecordByName(session, name: str, IDGame: int):
    return session.query(Location).filter(Location.IDGame == IDGame).filter(Location.name == name).first()
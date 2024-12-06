from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import Session, relationship, joinedload
from .base import Base, StrictInteger

from loggerConfig import logicLogger as logger

class Attempt(Base):
    __tablename__ = "Attempt"

    IDAttempt = Column("IDAttempt", StrictInteger, primary_key = True, autoincrement = True)
    IDGame = Column("IDGame", ForeignKey("Game.IDGame"), nullable = False)
    attemptNumber = Column("AttemptNumber", StrictInteger, nullable = False)
    badges = Column("Badges", StrictInteger, nullable = False, default = 0)
    
    game = relationship("Game", back_populates="attempt")

    def __init__(self, IDGame, attemptNumber):
        self.IDGame = IDGame
        self.attemptNumber = attemptNumber
        

    
    def __repr__(self):
        return f"IDAttempt: {self.IDAttempt}, IDGame: {self.IDGame}, attemptNumber: {self.attemptNumber}"

def addAttempt(session: Session, IDGame: int) -> Attempt | None:
    attemptNumber = getNextAttemptNumber(session, IDGame)
    if attemptNumber == -1:
        return None
    newAttempt = Attempt(IDGame, attemptNumber)
    session.add(newAttempt)
    session.commit()  
    return newAttempt

def getNextAttemptNumber(session: Session, IDGame: int)-> int:
    attemptNumber = -1
    attemptNumber = session.query(Attempt).filter(Attempt.IDGame == IDGame).count() + 1
    logger.debug(f"new attempt: {attemptNumber}")    
    return attemptNumber

def getAttempt(session: Session, IDGame: int, attemptNumber: int) -> Attempt | None:
    attempt = session.query(Attempt).filter(Attempt.attemptNumber == attemptNumber).filter(Attempt.IDGame == IDGame).first()
    return attempt
    
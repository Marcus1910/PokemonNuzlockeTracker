from sqlalchemy import ForeignKey, Column, String, Float
from .base import Base

class Typing(Base):
    __tablename__ = "Typing"

    IDTyping = Column("IDTyping", String, primary_key = True)

    def __init__(self, IDTyping):
        self.IDTyping = IDTyping
    
def fillTypeTable(session, types: list[str]):
    session.add_all([Typing(type) for type in types]) 

def addTyping(session, IDTyping: str):
    session.add(Typing(IDTyping))


class TypeMatchup(Base):
    __tablename__ = "TypeMatchup"

    IDAttackingType = Column("IDAttackingType", ForeignKey("Typing.IDTyping"), primary_key = True)
    IDDefendingType = Column("IDDefendingType", ForeignKey("Typing.IDTyping"), primary_key = True)
    effectiveness = Column("Effectiveness", Float, nullable = False)

    def __init__(self, IDAttackingType, IDDefendingType, effectiveness):
        self.IDAttackingType = IDAttackingType
        self.IDDefendingType = IDDefendingType
        self.effectiveness = effectiveness
    
    def __repr__(self):
        return f"attack: {self.IDAttackingType}, defend: {self.IDDefendingType}, effectiveness: {self.effectiveness}"
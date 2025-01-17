from sqlalchemy import Column, String
from .base import Base

class Gender(Base):
    __tablename__ = "Gender"

    IDGender = Column("IDGender", String, primary_key = True)

    def __init__(self, IDGender):
        self.IDGender = IDGender

def getGenders(session):
    return {gender.IDGender: gender.IDGender for gender in session.query(Gender).all()}


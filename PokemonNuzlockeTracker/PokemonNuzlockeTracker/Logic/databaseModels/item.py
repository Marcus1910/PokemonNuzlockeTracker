from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from .base import Base

class Item(Base):
    __tablename__ = "Item"

    IDItem = Column("IDItem", Integer, primary_key = True, autoincrement = True)
    name = Column("Name", String, nullable = False)
    description = Column("Description", String)
    isKeyItem = Column("IsKeyItem", Boolean, default = False, nullable = False)

    def __init__(self, name, description = None, isKeyItem = False):
        self.name = name
        self.description = description
        self.isKeyItem = isKeyItem

class FieldItem(Base):
    __tablename__ = "FieldItem"

    IDFieldItem = Column("IDFieldItem", Integer, primary_key = True, autoincrement = True)
    IDItem = Column("IDItem", ForeignKey("Item.IDItem"), nullable = False)
    IDLocation = Column("IDLocation", ForeignKey("Location.IDLocation"), nullable = False)
    locationSpecific = Column("LocationSpecific", String)
    grabbed = Column("Grabbed", Boolean, default = False)

    def __init__(self, IDItem, IDLocation, locationSpecific = None, grabbed = False):
        self.IDItem = IDItem
        self.IDLocation = IDLocation
        self.locationSpecific = locationSpecific
        self.grabbed = grabbed
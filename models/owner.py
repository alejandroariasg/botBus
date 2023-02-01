import database.db as db
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship


class Owner(db.Base):
    __tablename__ = 'owner'
    id = Column('id', Float, primary_key=True, nullable=False)
    email = Column('email', String, nullable=False)
    vehicles = relationship('Vehicle', back_populates='owner')

    def __init__(self, id, email):
        self.id = id
        self.email = email

    def __repr__(self):
        return f"<Owner {self.id}>"

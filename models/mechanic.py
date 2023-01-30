import database.db as db
from sqlalchemy import Column, Float
from sqlalchemy.orm import relationship


class Mechanic(db.Base):
    __tablename__ = 'mechanic'
    id = Column('id', Float, primary_key=True, nullable=False)
    phone = Column('phone', Float, server_default='0', nullable=False)
    maintenances = relationship('Maintenance', back_populates='mechanic')

    def __init__(self, id, phone):
        self.id = id
        self.phone = phone

    def __repr__(self):
        return f"<Mechanic {self.id}>"

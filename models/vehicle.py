import database.db as db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Vehicle(db.Base):
    __tablename__ = 'vehicle'
    id = Column('id', String(6), primary_key=True, nullable=False)
    model = Column('model', Integer,  nullable=True)
    mark = Column('mark', String(15), server_default='', nullable=True)
    reviews = relationship('Review', back_populates='vehicle')
    insurances = relationship('Insurance', back_populates='vehicle')
    owner_id = Column(Float, ForeignKey("owner.id"))
    owner = relationship("Owner", back_populates="vehicles")

    def __init__(self, id, model, mark, owner_id):
        self.id = id
        self.model = model
        self.mark = mark
        self.owner_id = owner_id

    def __repr__(self):
        return f"<Vehicle {self.id}>"

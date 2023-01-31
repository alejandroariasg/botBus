import database.db as db
from sqlalchemy import Column, DateTime, String,  func, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Maintenance(db.Base):
    __tablename__ = 'maintenance'
    id = Column('id', Integer, primary_key=True, nullable=False)
    description = Column('description', String, nullable=True)
    date = Column('date', DateTime, server_default=func.now(), nullable=False)
    spare_parts = Column('spare_parts', String, nullable=True)
    fluid_check = relationship(
        'FluidCheck', back_populates='maintenance')

    mechanic_id = Column(Float, ForeignKey("mechanic.id"))
    mechanic = relationship("Mechanic", back_populates="maintenances")

    vehicle_id = Column(String(6), ForeignKey("vehicle.id"))
    vehicle = relationship("Vehicle", back_populates="maintenances")

    def __init__(
        self,
        id,
        description,
        date,
        spare_parts,
        mechanic_id,
        vehicle_id
    ):
        self.id = id
        self.description = description
        self.date = date
        self.spare_parts = spare_parts
        self.vehicle_id = vehicle_id
        self.mechanic = mechanic_id

    def __repr__(self):
        return f"<Maintenance {self.id}>"

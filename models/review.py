import database.db as db
from sqlalchemy import Column, DateTime, String,  func, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Review(db.Base):
    __tablename__ = 'review'
    id = Column('id', Integer, primary_key=True,
                nullable=False,  autoincrement=True)
    description = Column('description', String, nullable=True)
    date = Column('date', DateTime, server_default=func.now(), nullable=False)
    spare_parts = Column('spare_parts', String, nullable=True)
    fluid_check = relationship(
        'FluidCheck', back_populates='review')

    mechanic_id = Column(Integer, ForeignKey("mechanic.id"))
    mechanic = relationship("Mechanic", back_populates="reviews")

    vehicle_id = Column(String(6), ForeignKey("vehicle.id"))
    vehicle = relationship("Vehicle", back_populates="reviews")

    def __init__(
        self,
        description,
        spare_parts,
        vehicle,
        mechanic
    ):
        self.description = description
        self.spare_parts = spare_parts
        self.vehicle = vehicle
        self.mechanic = mechanic
    def __repr__(self):
        return f"<Maintenance {self.id}>"

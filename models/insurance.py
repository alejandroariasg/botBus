import database.db as db
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, func
from sqlalchemy.orm import relationship


class Insurance(db.Base):
    __tablename__ = 'insurance'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    validity = Column('validity', Integer, nullable=False)
    date = Column('date', DateTime, server_default=func.now(), nullable=False)
    vehicle_id = Column('vehicle_id',String(6), ForeignKey("vehicle.id"))
    vehicle = relationship("Vehicle", back_populates="insurances")

    def __init__(self, validity, vehicle):
        self.validity = validity
        self.vehicle = vehicle

    def __repr__(self):
        return f"<Insurance {self.id}>"

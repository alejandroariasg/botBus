import database.db as db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class FluidCheck(db.Base):
    __tablename__ = 'fluid_check'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    oil_level = Column('oil_level', Integer, nullable=False)
    brake_fluid_level = Column('brake_fluid_level', Integer, nullable=False)
    coolant_level = Column('coolant_level', Integer, nullable=False)
    steering_fluid_level = Column('steering_fluid_level', Integer, nullable=False)
    maintenance_id = Column(Integer, ForeignKey('maintenance.id'))
    maintenance = relationship("Maintenance", back_populates="fluid_check")
    
    def __init__(
        self,
        id,
        oil_level,
        brake_fluid_level,
        coolant_level,
        steering_fluid_level,
        maintenance_id
    ):
        self.id = id
        self.oil_level = oil_level
        self.brake_fluid_level = brake_fluid_level
        self.coolant_level = coolant_level
        self.steering_fluid_level = steering_fluid_level
        self.maintenance_id = maintenance_id

    def __repr__(self):
        return f"<FluidCheck {self.id}>"

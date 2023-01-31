import database.db as db
from models.mechanic import Mechanic
from models.fluid_check import FluidCheck
from models.insurance import Insurance
from models.maintenance import Maintenance
from models.owner import Owner
from models.vehicle import Vehicle


#### register
def register_mechanic(user_id, phone):
    mechanic = db.session.query(Mechanic).get(user_id)
    db.session.commit()
    if mechanic == None:
        mechanic = Mechanic(user_id, phone)
        db.session.add(mechanic)
        db.session.commit()
        return True
    return False


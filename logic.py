import database.db as db
from models.mechanic import Mechanic
from models.owner import Owner
from models.fluid_check import FluidCheck
from models.insurance import Insurance
from models.review import Review
from models.vehicle import Vehicle
from record import Record
record = Record()

# Authentication
def login_user(user_id):
    mechanic = db.session.query(Mechanic).get(user_id)
    db.session.commit()
    if mechanic != None:
        record.set_user_data(mechanic, 'mechanic')
        return 'mechanic'
    else:
        owner = db.session.query(Owner).get(user_id)
        db.session.commit()
        if owner != None:
            record.set_user_data(owner, 'owner')
            return 'owner'
    return False


# register
def register_mechanic(user_id, phone):
    mechanic = db.session.query(Mechanic).get(user_id)
    db.session.commit()
    if mechanic == None:
        mechanic = Mechanic(user_id, phone)
        db.session.add(mechanic)
        db.session.commit()
        return True
    return False


def register_owner(user_id, email):
    owner = db.session.query(Owner).get(user_id)
    db.session.commit()
    if owner == None:
        owner = Owner(user_id, email)
        db.session.add(owner)
        db.session.commit()
        return True
    return False


def register_review(description, spare_parts, vehicle_id):
    mechanic = db.session.query(Mechanic).get(record.user.id)
    vehicle = db.session.query(Vehicle).get(vehicle_id)
    db.session.commit()

    if (vehicle):
        review = Review(
            description,
            spare_parts,
            vehicle,
            mechanic)
        db.session.add(review)
        db.session.commit()
        return True
    return False

def register_vehicle(id, model, mark, id_owner):
    owner = db.session.query(Owner).get(id_owner)
    if(owner):    
        vehicle = Vehicle(id, model, mark, id_owner)
        db.session.add(vehicle)
        db.session.commit()
        return "Vehículo registrado exitosamente."
    return "El owner no exite. Debes primero registrar este."


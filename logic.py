import database.db as db
from models.mechanic import Mechanic
from models.fluid_check import FluidCheck
from models.insurance import Insurance
from models.review import Review
from models.owner import Owner
from models.vehicle import Vehicle
from record import Record
record = Record()

# Authentication

def login_user(user_id):
    mechanic = db.session.query(Mechanic).get(user_id)
    db.session.commit()
    if mechanic != None:
        record.set_user_data(user_id, 'mechanic')
        return 'mechanic'
    else:
        owner = db.session.query(Owner).get(user_id)
        db.session.commit()
        if owner != None:
            record.set_user_data(user_id, 'owner')
            return 'owner'
    return False


def auth_middleware(user_types):
    def wrapper(func):
        def innerr(*args, **kwargs):
            user_id = kwargs.pop("user_id")
            ok_login = login_user(user_id)
            if (not ok_login or record.user_type not in user_types):
                return "El usuario no se encuentra registrado, o no tiene los permisos suficientes"
            return func(*args, **kwargs)
        return innerr
    return wrapper


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


@auth_middleware(user_types=["mechanic"])
def register_review(description, spare_parts, vehicle_id):
    mechanic = db.session.query(Mechanic).get(record.user_id)
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
        return "Revision registrada con exito"
    return "El vehiculo no se encuentra registrado"

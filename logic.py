import database.db as db
from models.mechanic import Mechanic
from models.fluid_check import FluidCheck
from models.insurance import Insurance
from models.maintenance import Maintenance
from models.owner import Owner
from models.vehicle import Vehicle
from record import Record
record = Record()


def login_user(user_id):
    mechanic = db.session.query(Mechanic).get(user_id)
    db.session.commit()
    if mechanic != None:
        record.set_user_data(user_id, 'mechanic')
        return 'mechanic'
    else:
        owner = db.session.query(Mechanic).get(user_id)
        db.session.commit()
        if owner != None:
            record.set_user_data(user_id, 'owner')
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


def auth_middleware(func):
    def wrapper(user_id, *args):
        if (record.user_id):
            func(*args, user_id)
        else:
            login_user(user_id)
            func(*args, user_id)
    return wrapper


@auth_middleware
def func_prueb(user_id):
    print("dflkfdklfd" + str(record.user_id))

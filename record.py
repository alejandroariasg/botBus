from models.mechanic import Mechanic
from models.owner import Owner


class Record():
    user: Owner | Mechanic = None
    user_type = None
    review = {
        'id': None,
        'description': None,
        'vehicle_id': None,
        'spare_parts': None,
    }

    fluid_check = {
        'oil_level': None,
        'brake_fluid_level': None,
        'coolant_level': None,
        'steering_fluid_level': None,
    }

    vehicle = {
        'id': None,
        'model': None,
        'mark': None,
        'id_owner': None,
    }

    def set_user_data(self, user, user_type):
        self.user = user
        self.user_type = user_type

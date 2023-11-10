import uuid
from api.app import db

class VehicleCreationError(Exception):
    pass

class VehicleDeletionError(Exception):
    pass

class Vehicle:

    def create(self, user_id, registration_number, brand, model, description, first_registration_date, energy, gearbox, type_mine, vin):
        if db.vehicles.find_one({"registration_number": registration_number, "user_id": user_id}):
            raise VehicleCreationError("Ce véhicule existe déjà")

        vehicle_id = uuid.uuid4().hex
        vehicle = {
            "_id": vehicle_id,
            "user_id": user_id,
            "registration_number": registration_number,
            "brand": brand,
            "model": model,
            "description": description,
            "first_registration_date": first_registration_date,
            "energy": energy,
            "gearbox": gearbox,
            "type_mine": type_mine,
            "vin": vin
        }

        result = db.vehicles.insert_one(vehicle)
        if not result.acknowledged:
            raise VehicleCreationError("Une erreur est survenue lors de la création du véhicule")

        return vehicle

    def read(self, user_id, vehicle_id=None, registration_number=None):
        query = {"user_id": user_id}
        if vehicle_id:
            query["_id"] = vehicle_id
        if registration_number:
            query["registration_number"] = registration_number

        if vehicle_id or registration_number:
            vehicle = db.vehicles.find_one(query)
            return vehicle
        else:
            vehicles = list(db.vehicles.find(query))
            return vehicles

    def delete(self, vehicle_id):
        result = db.vehicles.find_one_and_delete({"_id": vehicle_id})
        if not result:
            raise VehicleDeletionError("Le véhicule n'a pas pu être supprimé")

        # Supprimez également tous les suivis associés à ce véhicule
        db.trackings.delete_many({"vehicle_id": vehicle_id})
        return {"message": "Le véhicule a été supprimé avec succès."}

import uuid
from api.app import db


class VehicleCreationError(Exception):
    """
    Custom exception class that is raised when there is an error during the
        creation of a vehicle.
    """
    pass


class VehicleDeletionError(Exception):
    """
    Custom exception class that is raised when there is an error during the
        deletion of a vehicle.
    """
    pass


class Vehicle:
    """
    A class that represents a vehicle and provides methods for creating,
        reading, and deleting vehicles in a database.

    Methods:
        create(user_id, registration_number, brand, model, description,
            first_registration_date, energy, gearbox, type_mine, vin):
                Creates a new vehicle with the given details and stores it in
                    the database. Raises a VehicleCreationError if the vehicle
                        already exists or if there is an error during creation.
                            Returns the created vehicle.

        read(user_id, vehicle_id=None, registration_number=None):
            Reads a vehicle from the database based on the given parameters.
                If only the user_id is provided, it returns a list of all
                    vehicles belonging to that user. If vehicle_id or
                        registration_number is also provided, it returns the
                            specific vehicle matching the given parameter(s).

        delete(vehicle_id):
            Deletes a vehicle from the database based on the given vehicle ID.
                Raises a VehicleDeletionError if the vehicle cannot be deleted
                    or if there is an error during deletion. Also deletes all
                        associated trackings for the vehicle.
                            Returns a success message.
    """

    def create(self, user_id, registration_number, brand, model, description,
               first_registration_date, energy, gearbox, type_mine, vin):
        """
        Creates a new vehicle with the given details and stores it in the
            database.

        Args:
            user_id (str): The ID of the user who owns the vehicle.
            registration_number (str): The registration number of the vehicle.
            brand (str): The brand of the vehicle.
            model (str): The model of the vehicle.
            description (str): The description of the vehicle.
            first_registration_date (str): The date of the first registration
                of the vehicle.
            energy (str): The energy type of the vehicle.
            gearbox (str): The gearbox type of the vehicle.
            type_mine (str): The type mine of the vehicle.
            vin (str): The VIN (Vehicle Identification Number) of the vehicle.

        Returns:
            dict: The created vehicle.

        Raises:
            VehicleCreationError: If the vehicle already exists or if there is
                an error during creation.
        """
        if db.vehicles.find_one(
                {"registration_number": registration_number, "user_id": user_id}):
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
            raise VehicleCreationError(
                "Une erreur est survenue lors de la création du véhicule")

        return vehicle

    def read(self, user_id, vehicle_id=None, registration_number=None):
        """
        Reads a vehicle from the database based on the given parameters.

        Args:
            user_id (str): The ID of the user who owns the vehicle.
            vehicle_id (str, optional): The ID of the vehicle to read.
                Defaults to None.
            registration_number (str, optional): The registration number of the
                vehicle to read. Defaults to None.

        Returns:
            dict or list: The specific vehicle matching the given parameter(s)
                or a list of all vehicles belonging to the user.

        """
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
        """
        Deletes a vehicle from the database based on the given vehicle ID.

        Args:
            vehicle_id (str): The ID of the vehicle to delete.

        Returns:
            dict: A success message.

        Raises:
            VehicleDeletionError: If the vehicle cannot be deleted or if there
                is an error during deletion.
        """
        result = db.vehicles.find_one_and_delete({"_id": vehicle_id})
        if not result:
            raise VehicleDeletionError("Le véhicule n'a pas pu être supprimé")

        db.trackings.delete_many({"vehicle_id": vehicle_id})
        return {"message": "Le véhicule a été supprimé avec succès."}

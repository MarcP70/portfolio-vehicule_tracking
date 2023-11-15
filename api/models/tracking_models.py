import uuid
from api.app import db


class TrackingCreationError(Exception):
    """
    Custom exception class that is raised when there is an error during the
        creation of a tracking entry.
    """
    pass


class TrackingDeletionError(Exception):
    """
    Custom exception class that is raised when there is an error during the
        deletion of a tracking entry.
    """
    pass


class Tracking:
    """
    Class for managing tracking information for vehicles.
    """

    def create(self, vehicle_id, **kwargs):
        """
        Creates a new tracking entry for a vehicle.

        Args:
            vehicle_id (str): The ID of the vehicle.
            **kwargs: Additional keyword arguments for the tracking entry.

        Returns:
            dict: The created tracking entry.

        Raises:
            TrackingCreationError: If there is an error during the creation of
                the tracking entry.
        """
        tracking_id = uuid.uuid4().hex
        tracking = {
            "_id": tracking_id,
            "vehicle_id": vehicle_id,
            **kwargs
        }
        result = db.trackings.insert_one(tracking)
        if not result.acknowledged:
            raise TrackingCreationError("Erreur lors de la création du suivi")
        return tracking

    def read_by_vehicle(self, vehicle_id):
        """
        Retrieves all tracking entries for a vehicle.

        Args:
            vehicle_id (str): The ID of the vehicle.

        Returns:
            list: A list of tracking entries.
        """
        return list(db.trackings.find({"vehicle_id": vehicle_id}))

    def read(self, tracking_id):
        """
        Retrieves a specific tracking entry.

        Args:
            tracking_id (str): The ID of the tracking entry.

        Returns:
            dict: The tracking entry.
        """
        return db.trackings.find_one({"_id": tracking_id})

    def delete_by_vehicle(self, vehicle_id):
        """
        Deletes all tracking entries for a vehicle.

        Args:
            vehicle_id (str): The ID of the vehicle.

        Raises:
            TrackingDeletionError: If no tracking entries are found for the
                vehicle.
        """
        result = db.trackings.delete_many({"vehicle_id": vehicle_id})
        if result.deleted_count == 0:
            raise TrackingDeletionError("Aucun suivi trouvé pour ce véhicule")

    def delete(self, tracking_id):
        """
        Deletes a specific tracking entry.

        Args:
            tracking_id (str): The ID of the tracking entry.

        Raises:
            TrackingDeletionError: If the tracking entry is not found or
                already deleted.
        """
        result = db.trackings.delete_one({"_id": tracking_id})
        if result.deleted_count == 0:
            raise TrackingDeletionError("Suivi introuvable ou déjà supprimé")

    def update(self, tracking_id, **kwargs):
        """
        Updates a specific tracking entry.

        Args:
            tracking_id (str): The ID of the tracking entry.
            **kwargs: Additional keyword arguments for updating the
                tracking entry.

        Raises:
            TrackingDeletionError: If the tracking entry is not found.
            TrackingCreationError: If no modifications are made to the
                tracking entry.
        """
        result = db.trackings.update_one(
            {"_id": tracking_id},
            {"$set": kwargs}
        )
        if result.matched_count == 0:
            raise TrackingDeletionError("Suivi introuvable")
        if result.modified_count == 0:
            raise TrackingCreationError("Aucune modification apportée")

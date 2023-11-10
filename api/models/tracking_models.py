import uuid
from api.app import db

class TrackingCreationError(Exception):
    pass

class TrackingDeletionError(Exception):
    pass

class Tracking:

    def create(self, vehicle_id, **kwargs):
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
        return list(db.trackings.find({"vehicle_id": vehicle_id}))

    def read(self, tracking_id):
        return db.trackings.find_one({"_id": tracking_id})

    def delete_by_vehicle(self, vehicle_id):
        result = db.trackings.delete_many({"vehicle_id": vehicle_id})
        if result.deleted_count == 0:
            raise TrackingDeletionError("Aucun suivi trouvé pour ce véhicule")

    def delete(self, tracking_id):
        result = db.trackings.delete_one({"_id": tracking_id})
        if result.deleted_count == 0:
            raise TrackingDeletionError("Suivi introuvable ou déjà supprimé")

    def update(self, tracking_id, **kwargs):
        result = db.trackings.update_one(
            {"_id": tracking_id},
            {"$set": kwargs}
        )
        if result.matched_count == 0:
            raise TrackingDeletionError("Suivi introuvable")
        if result.modified_count == 0:
            raise TrackingCreationError("Aucune modification apportée")

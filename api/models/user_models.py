import re
from passlib.hash import pbkdf2_sha256
from api.app import db
import uuid

class UserDeletionError(Exception):
    """Exception levée si une erreur est survenue dans le processus de suppression."""
    pass

class UserNotFoundError(Exception):
    """Exception levée si l'utilisateur n'a pas été trouvé."""
    pass

class PasswordResetError(Exception):
    """Exception levée si le mot de passe n'a pas pu être modifié"""
    pass

class User:
    def __init__(self, user_data):
        self.user_data = user_data
        self.user_id = user_data.get('_id')

    @classmethod
    def validate_email(cls, email):
        return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)

    @classmethod
    def create(cls, email, name, password):
        if not cls.validate_email(email):
            raise ValueError("Adresse email invalide")

        if db.users.find_one({"email": email}):
            raise ValueError("Adresse email déjà utilisée")

        user_id = uuid.uuid4().hex
        hashed_password = pbkdf2_sha256.encrypt(password)
        user = {
            "_id": user_id,
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "user"
        }

        if db.users.insert_one(user).acknowledged:
            return cls(user)
        else:
            raise Exception("Échec de l'enregistrement")

    def update(self, name, email, password):
        if not self.validate_email(email):
            raise ValueError("Adresse email invalide")

        update_data = {"name": name, "email": email}
        if password:
            update_data['password'] = pbkdf2_sha256.encrypt(password)

        result = db.users.update_one({"_id": self.user_id}, {"$set": update_data})

        if result.modified_count == 0:
            raise Exception("Aucune modification apportée")


    @classmethod
    def delete(cls, user_id):
        # Vérifier que l'utilisateur existe bien
        user = db.users.find_one({"_id": user_id})
        if not user:
            raise ValueError("Cet utilisateur n'existe pas")

        # Supprimer les suivis des véhicules de l'utilisateur
        vehicles = db.vehicles.find({"user_id": user_id}, {"_id": 1})
        vehicle_ids = [vehicle['_id'] for vehicle in vehicles]
        if vehicle_ids:
            db.trackings.delete_many({"vehicle_id": {"$in": vehicle_ids}})

        # Supprimer les véhicules de l'utilisateur
        db.vehicles.delete_many({"user_id": user_id})

        # Supprimer l'utilisateur lui-même
        result = db.users.delete_one({"_id": user_id})
        if result.deleted_count == 0:
            raise UserDeletionError("Échec de la suppression du compte")
        return {"message": "Compte et données associées supprimés avec succès"}


    @classmethod
    def login(cls, email, password):
        user = db.users.find_one({"email": email})
        if user and pbkdf2_sha256.verify(password, user['password']):
            # Retourner une instance de l'utilisateur avec les données nécessaires
            return cls(user)  # Retourner une instance de l'utilisateur
        else:
            # Vous pouvez lever une exception ou retourner None selon la façon dont vous voulez gérer les erreurs de connexion
            raise ValueError("Adresse e-mail non trouvée ou mot de passe incorrect")

    @classmethod
    def reset_password(cls, user_id, new_password):
        hashed_password = pbkdf2_sha256.encrypt(new_password)
        result = db.users.update_one({"_id": user_id}, {"$set": {"password": hashed_password}})
        if result.modified_count == 0:
            raise PasswordResetError("La réinitialisation du mot de passe a échoué.")
        return {"message": "Mot de passe réinitialisé avec succès."}


    @classmethod
    def get_all_users(cls):
        users = db.users.find({"role": 'user'}, {"password": 0})  # Exclure les mots de passe pour des raisons de sécurité
        return list(users)

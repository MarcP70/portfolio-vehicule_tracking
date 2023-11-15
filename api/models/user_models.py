import re
from passlib.hash import pbkdf2_sha256
from api.app import db
import uuid


class UserDeletionError(Exception):
    """
    Exception raised when an error occurs during the process of deleting
        a user.
    """
    pass


class UserNotFoundError(Exception):
    """
    Custom exception raised when a user is not found.
    """
    pass


class PasswordResetError(Exception):
    """
    Custom exception raised when an error occurs during the process of
        resetting a user's password.
    """
    pass


class User:
    def __init__(self, user_data):
        """
        Initializes a new instance of the User class.

        Args:
            user_data (dict): A dictionary containing the user data,
                including the user ID (`_id`).
        """
        self.user_data = user_data
        self.user_id = user_data.get('_id')

    @classmethod
    class UserNotFoundError:
        """
        Represents an error that occurs when a user is not found.
        """

        def validate_email(cls, email):
            """
            Validates the format of an email address.

            Args:
                email (str): The email address to validate.

            Returns:
                bool: True if the email address is valid, False otherwise.
            """
            return re.match(
                r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)

    @classmethod
    def create(cls, email, name, password):
        """
        Create a new user in the system.

        Args:
            email (str): The email address of the user.
            name (str): The name of the user.
            password (str): The password of the user.

        Returns:
            User: An instance of the User class representing the newly
                created user.

        Raises:
            ValueError: If the email address is invalid or already used by
                another user.
            Exception: If the insertion of user data fails.
        """
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
        """
        Update the name, email, and password of a user in the system.

        Args:
            name (str): The new name of the user.
            email (str): The new email address of the user.
            password (str): The new password of the user.

        Raises:
            ValueError: If the email address is invalid.
            Exception: If no modifications were made.

        Returns:
            None. If no exception is raised, it indicates that the user data
                was successfully updated.
        """
        if not self.validate_email(email):
            raise ValueError("Adresse email invalide")

        update_data = {"name": name, "email": email}
        if password:
            update_data['password'] = pbkdf2_sha256.encrypt(password)

        result = db.users.update_one(
            {"_id": self.user_id}, {"$set": update_data})

        if result.modified_count == 0:
            raise Exception("Aucune modification apportée")

    @classmethod
    def delete(cls, user_id):
        """
        Delete a user and all associated data from the system.

        Args:
            user_id (str): The ID of the user to be deleted.

        Raises:
            ValueError: If the user with the given user_id does not exist.
            UserDeletionError: If the deletion of the user fails.

        Returns:
            dict: A dictionary with the message "Compte et données associées
                supprimés avec succès" if the user deletion was successful.
        """
        # Check that the user exists
        user = db.users.find_one({"_id": user_id})
        if not user:
            raise ValueError("Cet utilisateur n'existe pas")

        # Delete user vehicle tracking
        vehicles = db.vehicles.find({"user_id": user_id}, {"_id": 1})
        vehicle_ids = [vehicle['_id'] for vehicle in vehicles]
        if vehicle_ids:
            db.trackings.delete_many({"vehicle_id": {"$in": vehicle_ids}})

        # Delete user vehicles
        db.vehicles.delete_many({"user_id": user_id})

        # Delete the user himself
        result = db.users.delete_one({"_id": user_id})
        if result.deleted_count == 0:
            raise UserDeletionError("Échec de la suppression du compte")
        return {"message": "Compte et données associées supprimés avec succès"}

    @classmethod
    def login(cls, email, password):
        """
        Authenticate a user by checking if the provided email and password
            match the stored user data.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: An instance of the User class representing the
                authenticated user.

        Raises:
            ValueError: If the user does not exist or the password is
                incorrect.

        """
        user = db.users.find_one({"email": email})
        if user and pbkdf2_sha256.verify(password, user['password']):
            # Return an instance of the user
            return cls(user)
        else:
            raise ValueError(
                "Adresse e-mail non trouvée ou mot de passe incorrect")

    @classmethod
    def reset_password(cls, user_id, new_password):
        """
        Reset the password of a user in the system.

        Args:
            user_id (str): The ID of the user whose password needs to be reset.
            new_password (str): The new password to set for the user.

        Returns:
            dict: A dictionary with a success message if the password reset
                was successful.

        Raises:
            PasswordResetError: If the password reset fails.
        """
        hashed_password = pbkdf2_sha256.encrypt(new_password)
        result = db.users.update_one(
            {"_id": user_id}, {"$set": {"password": hashed_password}})
        if result.modified_count == 0:
            raise PasswordResetError(
                "La réinitialisation du mot de passe a échoué.")
        return {"message": "Mot de passe réinitialisé avec succès."}

    @classmethod
    def get_all_users(cls):
        """
        Retrieves all users from the database with the role 'user' and excludes
            their passwords for security reasons.

        Returns:
            list: A list of user objects, each containing the user's ID, name,
                email, and role.

        Security: {"password": 0} # Exclude passwords for security reasons
        """
        users = db.users.find({"role": 'user'}, {"password": 0})
        return list(users)

import unittest
from unittest.mock import patch, MagicMock
from api.app import db
from api.models.user_models import User, UserNotFoundError, UserDeletionError, PasswordResetError, pbkdf2_sha256

class TestUser(unittest.TestCase):

    def setUp(self):
        # Set up a mock database for testing
        self.mock_db = MagicMock()
        self.patcher = patch('api.models.user_models.db', self.mock_db)
        self.patcher.start()

    def tearDown(self):
        # Stop the patcher after each test
        self.patcher.stop()

    def test_create_user(self):
        # Test the create method
        with patch('api.models.user_models.uuid') as mock_uuid:
            mock_uuid.uuid4.return_value.hex = 'test_user_id'
            self.mock_db.users.find_one.return_value = None

            user = User.create('test@example.com', 'Test User', 'password123')

            self.assertEqual(user.user_id, 'test_user_id')

    def test_create_user_invalid_email(self):
        # Test create method with an invalid email
        with self.assertRaises(ValueError):
            User.create('invalid_email', 'Test User', 'password123')

    def test_create_user_duplicate_email(self):
        # Test create method with a duplicate email
        self.mock_db.users.find_one.return_value = {'_id': 'existing_user_id'}
        with self.assertRaises(ValueError):
            User.create('existing@example.com', 'Test User', 'password123')

    def test_update_user(self):
        # Test the update method
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com'}
        user_instance = User(user_data)
        self.mock_db.users.update_one.return_value.modified_count = 1

        with patch('api.models.user_models.pbkdf2_sha256') as mock_pbkdf2:
            mock_pbkdf2.hash.return_value = 'hashed_password'

            user_instance.update('Updated User', 'updated@example.com', 'new_password')

        # Ensure the update data is passed to the database
        self.mock_db.users.update_one.assert_called_with(
            {"_id": 'test_user_id'},
            {"$set": {'name': 'Updated User', 'email': 'updated@example.com', 'password': 'hashed_password'}}
        )

    def test_update_user_invalid_email(self):
        # Test update method with an invalid email
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com'}
        user_instance = User(user_data)
        with self.assertRaises(ValueError):
            user_instance.update('Updated User', 'invalid_email', 'new_password')

    def test_update_user_no_modifications(self):
        # Test update method with no modifications
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com'}
        user_instance = User(user_data)
        self.mock_db.users.update_one.return_value.modified_count = 0
        with self.assertRaises(Exception):
            user_instance.update('Test User', 'test@example.com', 'password123')

    def test_delete_user(self):
        # Test the delete method
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com'}
        user_instance = User(user_data)
        self.mock_db.users.find_one.return_value = user_data
        self.mock_db.vehicles.find.return_value = [{'_id': 'vehicle_id'}]
        self.mock_db.trackings.delete_many.return_value.deleted_count = 1
        self.mock_db.vehicles.delete_many.return_value.deleted_count = 1
        self.mock_db.users.delete_one.return_value.deleted_count = 1

        result = user_instance.delete('test_user_id')

        self.assertEqual(result['message'], 'Compte et données associées supprimés avec succès')

    def test_delete_user_not_found(self):
        # Test delete method with a user not found
        self.mock_db.users.find_one.return_value = None
        with self.assertRaises(ValueError):
            User.delete('nonexistent_user_id')

    def test_delete_user_deletion_error(self):
        # Test delete method with a deletion error
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com'}
        user_instance = User(user_data)
        self.mock_db.users.find_one.return_value = user_data
        self.mock_db.vehicles.find.return_value = [{'_id': 'vehicle_id'}]
        self.mock_db.trackings.delete_many.return_value.deleted_count = 1
        self.mock_db.vehicles.delete_many.return_value.deleted_count = 1
        self.mock_db.users.delete_one.return_value.deleted_count = 0
        with self.assertRaises(UserDeletionError):
            user_instance.delete('test_user_id')

    def test_login_user(self):
        # Test the login method
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com', 'password': 'hashed_password'}
        self.mock_db.users.find_one.return_value = user_data

        # Correct import for pbkdf2_sha256
        with patch('api.models.user_models.pbkdf2_sha256') as mock_pbkdf2:
            # Mock the verify function to always return True
            mock_pbkdf2.verify.return_value = True

            user = User.login('test@example.com', 'password123')

        self.assertEqual(user.user_id, 'test_user_id')

    def test_login_user_not_found(self):
        # Test login method with a user not found
        self.mock_db.users.find_one.return_value = None
        with self.assertRaises(ValueError):
            User.login('nonexistent@example.com', 'password123')

    def test_login_user_incorrect_password(self):
        # Test login method with an incorrect password
        user_data = {'_id': 'test_user_id', 'name': 'Test User', 'email': 'test@example.com', 'password': 'hashed_password'}
        self.mock_db.users.find_one.return_value = user_data
        with self.assertRaises(ValueError):
            User.login('test@example.com', 'incorrect_password')

    def test_reset_password(self):
        # Test the reset_password method
        user_instance = User({'_id': 'test_user_id'})
        self.mock_db.users.update_one.return_value.modified_count = 1

        result = user_instance.reset_password('test_user_id', 'new_password')

        self.assertEqual(result['message'], 'Mot de passe réinitialisé avec succès.')

    def test_reset_password_failure(self):
        # Test reset_password method with a failure
        user_instance = User({'_id': 'test_user_id'})
        self.mock_db.users.update_one.return_value.modified_count = 0
        with self.assertRaises(PasswordResetError):
            user_instance.reset_password('test_user_id', 'new_password')

    def test_get_all_users(self):
        # Test the get_all_users method
        self.mock_db.users.find.return_value = [{'_id': 'user_id', 'name': 'User1', 'email': 'user1@example.com', 'role': 'user'}]

        users = User.get_all_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['_id'], 'user_id')
        self.assertEqual(users[0]['name'], 'User1')
        self.assertEqual(users[0]['email'], 'user1@example.com')
        self.assertEqual(users[0]['role'], 'user')


if __name__ == '__main__':
    unittest.main()

import unittest
from user import User  # Importez votre classe User ici
from unittest.mock import patch

class TestUser(unittest.TestCase):

    def test_validate_email_valid(self):
        self.assertTrue(User.validate_email("test@example.com"))

    def test_validate_email_invalid(self):
        self.assertFalse(User.validate_email("test@example"))

    @patch('user.db.users.find_one')
    def test_create_user_success(self, mock_find_one):
        mock_find_one.return_value = None
        with patch('user.db.users.insert_one') as mock_insert_one:
            mock_insert_one.return_value = MockAcknowledged(True)
            result = User.create("test@example.com", "Test User", "password123")
            self.assertIsInstance(result, User)


class MockAcknowledged:
    def __init__(self, acknowledged):
        self.acknowledged = acknowledged

if __name__ == '__main__':
    unittest.main()

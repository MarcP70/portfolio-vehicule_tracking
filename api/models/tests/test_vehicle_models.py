import unittest
from unittest.mock import patch, MagicMock
from api.app import db
from api.models.vehicle_models import Vehicle, VehicleCreationError, VehicleDeletionError


class TestVehicle(unittest.TestCase):

    def setUp(self):
        # Set up a mock database for testing
        self.mock_db = MagicMock()
        self.patcher = patch('api.models.vehicle_models.db', self.mock_db)
        self.patcher.start()

    def tearDown(self):
        # Stop the patcher after each test
        self.patcher.stop()

    def test_create_vehicle(self):
        # Test the create method
        with patch('api.models.vehicle_models.uuid') as mock_uuid:
            mock_uuid.uuid4.return_value.hex = 'test_vehicle_id'

            # Configure the mock_db to return None for find_one, indicating that the vehicle does not exist
            self.mock_db.vehicles.find_one.return_value = None

            # Configure the mock_db to acknowledge the insertion
            self.mock_db.vehicles.insert_one.return_value.acknowledged = True

            vehicle = Vehicle().create(
                'test_user_id', 'ABC123', 'Toyota', 'Camry', 'Test Vehicle',
                '2022-01-01', 'Gasoline', 'Automatic', 'Sedan', '12345678901234567'
            )

            self.assertEqual(vehicle['_id'], 'test_vehicle_id')
            self.assertEqual(vehicle['user_id'], 'test_user_id')
            self.assertEqual(vehicle['registration_number'], 'ABC123')
            self.assertEqual(vehicle['brand'], 'Toyota')
            self.assertEqual(vehicle['model'], 'Camry')
            self.assertEqual(vehicle['description'], 'Test Vehicle')
            self.assertEqual(vehicle['first_registration_date'], '2022-01-01')
            self.assertEqual(vehicle['energy'], 'Gasoline')
            self.assertEqual(vehicle['gearbox'], 'Automatic')
            self.assertEqual(vehicle['type_mine'], 'Sedan')
            self.assertEqual(vehicle['vin'], '12345678901234567')

    def test_create_vehicle_error(self):
        # Test create method with an error
        with patch('api.models.vehicle_models.uuid') as mock_uuid:
            mock_uuid.uuid4.return_value.hex = 'test_vehicle_id'
            self.mock_db.vehicles.insert_one.return_value.acknowledged = False

            with self.assertRaises(VehicleCreationError):
                Vehicle().create(
                    'test_user_id', 'ABC123', 'Toyota', 'Camry', 'Test Vehicle',
                    '2022-01-01', 'Gasoline', 'Automatic', 'Sedan', '12345678901234567'
                )

    def test_read_user_vehicles(self):
        # Test the read method with only user_id provided
        self.mock_db.vehicles.find.return_value = [
            {'_id': 'vehicle_id1', 'user_id': 'test_user_id', 'registration_number': 'ABC123'},
            {'_id': 'vehicle_id2', 'user_id': 'test_user_id', 'registration_number': 'XYZ789'}
        ]

        vehicles = Vehicle().read('test_user_id')

        self.assertEqual(len(vehicles), 2)
        self.assertEqual(vehicles[0]['_id'], 'vehicle_id1')
        self.assertEqual(vehicles[0]['user_id'], 'test_user_id')
        self.assertEqual(vehicles[0]['registration_number'], 'ABC123')
        self.assertEqual(vehicles[1]['_id'], 'vehicle_id2')
        self.assertEqual(vehicles[1]['user_id'], 'test_user_id')
        self.assertEqual(vehicles[1]['registration_number'], 'XYZ789')

    def test_read_vehicle_by_id(self):
        # Test the read method with vehicle_id provided
        self.mock_db.vehicles.find_one.return_value = {'_id': 'vehicle_id', 'user_id': 'test_user_id', 'registration_number': 'ABC123'}

        vehicle = Vehicle().read('test_user_id', vehicle_id='vehicle_id')

        self.assertEqual(vehicle['_id'], 'vehicle_id')
        self.assertEqual(vehicle['user_id'], 'test_user_id')
        self.assertEqual(vehicle['registration_number'], 'ABC123')

    def test_read_vehicle_by_registration_number(self):
        # Test the read method with registration_number provided
        self.mock_db.vehicles.find_one.return_value = {'_id': 'vehicle_id', 'user_id': 'test_user_id', 'registration_number': 'ABC123'}

        vehicle = Vehicle().read('test_user_id', registration_number='ABC123')

        self.assertEqual(vehicle['_id'], 'vehicle_id')
        self.assertEqual(vehicle['user_id'], 'test_user_id')
        self.assertEqual(vehicle['registration_number'], 'ABC123')

    def test_delete_vehicle(self):
        # Test the delete method
        self.mock_db.vehicles.find_one_and_delete.return_value = {'_id': 'vehicle_id'}

        result = Vehicle().delete('vehicle_id')

        self.mock_db.trackings.delete_many.assert_called_with({"vehicle_id": 'vehicle_id'})
        self.assertEqual(result, {"message": "Le véhicule a été supprimé avec succès."})

    def test_delete_vehicle_not_found(self):
        # Test delete method with not found error
        self.mock_db.vehicles.find_one_and_delete.return_value = None

        with self.assertRaises(VehicleDeletionError):
            Vehicle().delete('nonexistent_vehicle_id')


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from api.app import db
from api.models.tracking_models import Tracking, TrackingCreationError, TrackingDeletionError


class TestTracking(unittest.TestCase):

    def setUp(self):
        # Set up a mock database for testing
        self.mock_db = MagicMock()
        self.patcher = patch('api.models.tracking_models.db', self.mock_db)
        self.patcher.start()

    def tearDown(self):
        # Stop the patcher after each test
        self.patcher.stop()

    def test_create_tracking(self):
        # Test the create method
        with patch('api.models.tracking_models.uuid') as mock_uuid:
            mock_uuid.uuid4.return_value.hex = 'test_tracking_id'
            self.mock_db.trackings.insert_one.return_value.acknowledged = True

            tracking = Tracking().create('test_vehicle_id', location='Test Location', mileage=100)

            self.assertEqual(tracking['_id'], 'test_tracking_id')
            self.assertEqual(tracking['vehicle_id'], 'test_vehicle_id')
            self.assertEqual(tracking['location'], 'Test Location')
            self.assertEqual(tracking['mileage'], 100)

    def test_create_tracking_error(self):
        # Test create method with an error
        with patch('api.models.tracking_models.uuid') as mock_uuid:
            mock_uuid.uuid4.return_value.hex = 'test_tracking_id'
            self.mock_db.trackings.insert_one.return_value.acknowledged = False

            with self.assertRaises(TrackingCreationError):
                Tracking().create('test_vehicle_id', location='Test Location', mileage=100)

    def test_read_by_vehicle(self):
        # Test the read_by_vehicle method
        self.mock_db.trackings.find.return_value = [{'_id': 'tracking_id', 'vehicle_id': 'test_vehicle_id', 'location': 'Test Location', 'mileage': 100}]

        trackings = Tracking().read_by_vehicle('test_vehicle_id')

        self.assertEqual(len(trackings), 1)
        self.assertEqual(trackings[0]['_id'], 'tracking_id')
        self.assertEqual(trackings[0]['vehicle_id'], 'test_vehicle_id')
        self.assertEqual(trackings[0]['location'], 'Test Location')
        self.assertEqual(trackings[0]['mileage'], 100)

    def test_read_tracking(self):
        # Test the read method
        self.mock_db.trackings.find_one.return_value = {'_id': 'tracking_id', 'vehicle_id': 'test_vehicle_id', 'location': 'Test Location', 'mileage': 100}

        tracking = Tracking().read('tracking_id')

        self.assertEqual(tracking['_id'], 'tracking_id')
        self.assertEqual(tracking['vehicle_id'], 'test_vehicle_id')
        self.assertEqual(tracking['location'], 'Test Location')
        self.assertEqual(tracking['mileage'], 100)

    def test_delete_by_vehicle(self):
        # Test the delete_by_vehicle method
        self.mock_db.trackings.delete_many.return_value.deleted_count = 1

        Tracking().delete_by_vehicle('test_vehicle_id')

        self.mock_db.trackings.delete_many.assert_called_with({"vehicle_id": 'test_vehicle_id'})

    def test_delete_by_vehicle_error(self):
        # Test delete_by_vehicle method with an error
        self.mock_db.trackings.delete_many.return_value.deleted_count = 0

        with self.assertRaises(TrackingDeletionError):
            Tracking().delete_by_vehicle('nonexistent_vehicle_id')

    def test_delete_tracking(self):
        # Test the delete method
        self.mock_db.trackings.delete_one.return_value.deleted_count = 1

        Tracking().delete('tracking_id')

        self.mock_db.trackings.delete_one.assert_called_with({"_id": 'tracking_id'})

    def test_delete_tracking_error(self):
        # Test delete method with an error
        self.mock_db.trackings.delete_one.return_value.deleted_count = 0

        with self.assertRaises(TrackingDeletionError):
            Tracking().delete('nonexistent_tracking_id')

    def test_update_tracking(self):
        # Test the update method
        self.mock_db.trackings.update_one.return_value.matched_count = 1
        self.mock_db.trackings.update_one.return_value.modified_count = 1

        Tracking().update('tracking_id', location='Updated Location', mileage=200)

        self.mock_db.trackings.update_one.assert_called_with(
            {"_id": 'tracking_id'},
            {"$set": {'location': 'Updated Location', 'mileage': 200}}
        )

    def test_update_tracking_not_found(self):
        # Test update method with a not found error
        self.mock_db.trackings.update_one.return_value.matched_count = 0

        with self.assertRaises(TrackingDeletionError):
            Tracking().update('nonexistent_tracking_id', location='Updated Location', mileage=200)

    def test_update_tracking_no_modifications(self):
        # Test update method with no modifications
        self.mock_db.trackings.update_one.return_value.matched_count = 1
        self.mock_db.trackings.update_one.return_value.modified_count = 0

        with self.assertRaises(TrackingCreationError):
            Tracking().update('tracking_id', location='Updated Location', mileage=200)


if __name__ == '__main__':
    unittest.main()

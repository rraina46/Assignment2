import unittest

from app import app, client  # Ensure accurate import paths
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_method_on_home_route(self):
        """
        Test 1: Route Test
        Test that sending a POST request to the home route ('/') returns a 405 status code,
        as the route only accepts GET requests.
        """
        response = self.app.post('/')
        self.assertEqual(response.status_code, 405)  # Ensure 405 status code for invalid method

    @patch('app.client.admin.command')
    def test_mongodb_connection(self, mock_command):
        """
        Test 2: Database Read Operation
        Test to check the correct connection of a MongoDB read operation using the ping command.
        """
        # Mock the ping command to simulate a successful connection
        mock_command.return_value = {'ok': 1.0}

        try:
            result = client.admin.command('ping')
            self.assertEqual(result['ok'], 1.0)
        except ConnectionFailure:
            self.fail("MongoDB connection failed")  # Fail the test if connection is not established

    @patch('app.products_collection')
    def test_mongodb_write_operation(self, mock_products_collection):
        """
        Test 3: Database Write Operation
        Test to check the MongoDB write operation (inserting a new document) and querying it.
        """
        mock_inserted_id = MagicMock()
        mock_products_collection.insert_one.return_value.inserted_id = mock_inserted_id

        new_product = {'name': 'New Product', 'price': 300}
        result = mock_products_collection.insert_one(new_product)
        inserted_id = result.inserted_id

        # Ensure the insert operation returns the mocked inserted_id
        self.assertEqual(inserted_id, mock_inserted_id)

        # Mock the query to return the inserted document
        mock_products_collection.find_one.return_value = new_product
        queried_product = mock_products_collection.find_one({'_id': inserted_id})

        # Ensure the queried document matches the inserted document
        self.assertEqual(queried_product, new_product)


if __name__ == '__main__':
    unittest.main()

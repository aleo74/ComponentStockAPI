import unittest
from app import create_app
from flask_jwt_extended import create_access_token
import json


class StocksControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def get_jwt_token(self):
        with self.app.app_context():
            token = create_access_token(identity='test_user')
        return token

    def test_save_stock(self):
        token = self.get_jwt_token()
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        data = json.dumps({'name': 'test', 'desc': 'description de test', 'qty': 1})
        response = self.client.post('/save_stock', data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        expected_data = {"message": "Stock enregistre avec succes"}
        response_data = json.loads(response.data)

        self.assertIn(expected_data, [response_data])

    def test_get_one_stock(self):
        token = self.get_jwt_token()
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/get_one_stock/test', headers=headers)

    def test_get_stock(self):
        token = self.get_jwt_token()
        headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/get_stocks/test', headers=headers)

    def test_edit_stock(self):
        token = self.get_jwt_token()
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

        data = json.dumps({'name': 'testUpdate', 'desc': 'description de test', 'qty': 1})
        self.client.post('/save_stock', data=data, headers=headers)

        response = self.client.get('/get_one_stock/testUpdate', headers=headers)
        stock_data = json.loads(response.data)

        updated_data = {'qty': 2}
        response = self.client.put(f'/edit_stock/{stock_data["_id"]}', data=json.dumps(updated_data), headers=headers)

        self.assertEqual(response.status_code, 200)
        expected_data = {"message": "Stock mis à jour avec succès"}
        response_data = json.loads(response.data)
        self.assertEqual(expected_data, response_data)

        response = self.client.get(f'/get_one_stock/test_updated', headers=headers)
        updated_stock_data = json.loads(response.data)
        self.assertEqual(updated_stock_data['name'], 'test_updated')
        self.assertEqual(updated_stock_data['desc'], 'description mise à jour')
        self.assertEqual(updated_stock_data['qty'], 2)


if __name__ == '__main__':
    unittest.main()

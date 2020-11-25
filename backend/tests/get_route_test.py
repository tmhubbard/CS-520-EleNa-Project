import unittest
import json

from server import app as flask_app

class GetRouteTest(unittest.TestCase):

    def setUp(self):
        flask_app.config['TESTING'] = True
        self.app = flask_app.test_client()

    def tearDown(self):
        pass
    
    def test_get_route_0(self):
        """Test route
                FROM: 100 North Pleasant Street, Amherst, MA, USA
                TO: 180 North Pleasant Street, Amherst, MA, USA
        """
        error = None
        
        with self.app as client:
            try:
                json_data = {
                    'start_point': {'lat': 42.3771782, 'lng': -72.5203465}, 
                    'end_point': {'lat': 42.3782802, 'lng': -72.5202872}, 
                    'elevation_type': 'min', 
                    'percent_of_distance': '145'
                }
                response = client.post('/getRoute', json=json_data)
            except Exception as e:
                error = e

            self.assertEqual(error, None, \
                "Exception caught in getRoute endpoint "
                f"Exception: {error}")

            self.assertEqual(response.status_code, 200, \
                f"Invalid Response Code! Got {response.status_code}")

            expected_response = {
                'route': [
                    {'lat': 42.3771782, 'lng': -72.5203465}, 
                    {'lat': 42.38138877500999, 'lng': -72.5206228697157}, 
                    {'lat': 42.3782802, 'lng': -72.5202872}
                ], 
                'total_elevation_gain': 3.8315887451171875,
                'total_distance_travelled': 1453
            }

            self.assertEqual(response.json, expected_response, \
                f"Invalid Response Data! Got {response.json}, \
                Expected {expected_response}")

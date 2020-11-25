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
                    'start_point': {'lat': 42.39035906429909, 'lng': -72.52511712936675}, 
                    'end_point': {'lat': 42.38978061083876, 'lng': -72.52498938916241}, 
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
                    {'lat': 42.39035906429909, 'lng': -72.52511712936675}, 
                    {'lat': 42.38978061083876, 'lng': -72.52498938916241}
                ], 
                'total_elevation_gain': 0.589, 
                'total_distance_travelled': 65.0
            }
            
            self.assertEqual(response.json, expected_response, \
                f"Invalid Response Data! Got {response.json}, \
                Expected {expected_response}")

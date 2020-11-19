from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from controller import test

# import controller
# import model

app = Flask(__name__)
CORS(app)


# Command to test a post request
    # curl -H "Content-type: application/json" -d '{ "origin_lat":"123", "min_max":"min" }' 'http://127.0.0.1:5000/getRoute'

@app.route('/getRoute', methods=['POST'])
def get_route():

    """
    INCOMING DATA:
        start_point: {lat: (value) lng: (value)},
        end_point: {lat: (value) lng: (value)},
        elevation_type: ("min" or "max"),
        percent_of_distance: (range of 0-100),
    """
    request_data = request.get_json(force=True, silent=False)

    # Deserialize Data
    start_point = request_data['start_point']
    end_point = request_data['end_point']
    elevation_type = request_data['elevation_type']
    percent_of_distance = float(request_data['percent_of_distance'])

    # PROCESS request_data
    origin = (start_point['lat'], start_point['lng'])
    destination = (end_point['lat'], end_point['lng'])
    overhead = percent_of_distance/100

    route = test(origin, destination, overhead)

    breakpoint()
    # FAKE DATA
    response = {
        "route": route,
        # [
            # {"lat": 42.389995, "lng": -72.528271}, 
            # {"lat": 42.389504, "lng": -72.528455}, 
            # {"lat": 42.390011, "lng": -72.528659}
        # ],
        "total_elevation_gain": 24.5,
        "total_distance_travelled": 40
    }

    return jsonify(**response)


if __name__ == '__main__':
   app.run(debug = True)
from flask import Flask, jsonify, request
from flask_cors import CORS

# import controller
# import model

app = Flask(__name__)
CORS(app)


# Command to test a post request
    # curl -H "Content-type: application/json" -d '{ "origin_lat":"123", "min_max":"min" }' 'http://127.0.0.1:5000/getRoute'

@app.route('/getRoute', methods=['POST'])
def get_route():
    # origin lat, long
    # dest lat, long
    # min/max
    # percentage overhead
    request_data = request.get_json(force=True, silent=False)

    # PROCESS request_data

    # FAKE DATA
    response = {
        "route": [
            (42.389995, -72.528271), 
            (42.389504, -72.528455), 
            (42.390011, -72.528659)
        ],
        "total_elevation_gain": 24.5,
        "total_distance_travelled": 40
    }

    return jsonify(**response)


if __name__ == '__main__':
   app.run(debug = True)
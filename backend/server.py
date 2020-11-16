from flask import Flask, jsonify, request
from flask_cors import CORS
# import controller
# import model

app = Flask(__name__)
CORS(app)

@app.route('/getRoute', methods=['POST'])
def get_route():
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
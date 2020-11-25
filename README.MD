# EleNA: Elevation Based Navigation

## What is EleNA?
EleNa (Elevation-based Navigation) is a web application that finds the an optimal route between two points by considering distance and elevation gain. EleNa would be used by runners, bikers, and hikers.

<img src="static_images/img1.PNG" alt="UI 1" width="1000"/>
<img src="static_images/img2.PNG" alt="UI 2" width="1000"/>

## How to run the App

First, install both the front-end dependencies and the server dependencies using the following two commands:

### `npm install` inside the react-googlemaps directory
### `pip install -r requirements.txt` inside backend directory

In the *react-googlemaps* directory, run the React client using the following command:

### `npm start`

In the the *backend* directory, run the Flask server using the following command:

### `python server.py`

## How to run Tests

### `npm test` In the *react-googlemaps* directory

### `python -m unittest discover -v -s ./tests -p "*_test.py"` In the the *backend* directory
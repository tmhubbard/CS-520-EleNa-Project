import React from 'react';
import InputForm from './InputForm';
import MapComponent from './MapComponent';
import RouteStats from './RouteStats';

/*Display is the final parent component, it handles all the data through its state and callback functions passed to children,
and handles the logic for submitting user queries to the backend for routes*/
class Display extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapcenter: {lat: 42.3732, lng: -72.5199},
            route: null,
            renderRoute: false,
            isStartingMarkerShown: false,
            isEndMarkerShown: false,
            startPoint: null,
            endPoint: null,
            elevationType: "min",
            percentRoute: 120,
            startAddress: '',
            endAddress: '',
            totalElevation: 0,
            totalDistance:  0,
            errorMessage: ""
        };

        this.handleMapStartChange = this.handleMapStartChange.bind(this);
        this.handleMapEndChange = this.handleMapEndChange.bind(this);
        this.handleInputStartChange = this.handleInputStartChange.bind(this);
        this.handleInputEndChange = this.handleInputEndChange.bind(this);
        this.handleInputTypeChange = this.handleInputTypeChange.bind(this);
        this.handleInputPercentChange = this.handleInputPercentChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    /*CALL BACK FUNCTIONS PASSED TO CHILDREN COMPONENT TO UPDATE STATE
    ----------------------------------------------------------------*/

    //handles start location change from the MapComponent
    handleMapStartChange(location, address) {
        this.setState({isStartingMarkerShown: true, startPoint : location, startAddress: address, mapCenter: location});
    }

    //handles end location change from the MapComponent
    handleMapEndChange(location, address) {
        this.setState({isEndMarkerShown: true, endPoint: location, endAddress: address, mapcenter: location});
    }

    //handles start location change from the InputForm
    handleInputStartChange(location, address) {
        if(location != null) {
            this.setState({isStartingMarkerShown: true, startPoint: location, startAddress: address});
        }
        else {
            this.setState({isStartingMarkerShown: false, startPoint: location, startAddress: address});
        }
    }

    //handles end location change from the InputForm
    handleInputEndChange(location, address) {
        if(location != null) {
            this.setState({isEndMarkerShown: true, endPoint : location, endAddress: address});
        }
        else {
            this.setState({isEndMarkerShown: false, endPoint : location, endAddress: address});
        }
    }

    //handles route type change from InputForm
    handleInputTypeChange(type) {
        this.setState({elevationType: type});
    }

    //handles route distance change from Inputform
    handleInputPercentChange(percent) {
        this.setState({percentRoute: percent});
    }

    /*Callback function passed to Inputform for submit "find route" button*/
    handleSubmit() {
        //info for submission comes from state
        var submission = {
            start_point: this.state.startPoint,
            end_point: this.state.endPoint,
            elevation_type: this.state.elevationType,
            percent_of_distance: this.state.percentRoute,
        }
        //submission object turned to JSON string
        var JSONsubmission = JSON.stringify(submission);
        //validation checking to make sure a valid location is passed to backend, displays error if null
        if (this.state.startPoint == null || this.state.endPoint == null) {
            this.setState({errorMessage: "Error: no location selected for either start or end point"});
            return;
        }
        //resets error message to nothing once valid points are entered
        else {
            this.setState({errorMessage: ""});
        }

        //call to backend to send query for route
        fetch("http://localhost:5000/getRoute", {
          method: 'POST',
          body: JSONsubmission
        })
        //receiving backend response as a route with statistics
        .then(res => res.json())
        .then(json => {
            this.setState({
              route: json.route,
              renderRoute: true,
              totalDistance: json.total_distance_travelled,
              totalElevation: json.total_elevation_gain
            });

            //recenters the map based on the route received
            var pathCoordinates = this.state.route;
            var bounds = new window.google.maps.LatLngBounds();
            for (var i = 0; i < pathCoordinates.length; i++) {
                bounds.extend(pathCoordinates[i]);
            }
            var coordinate = {lat: bounds.getCenter().lat(), lng: bounds.getCenter().lng()};
            this.setState({mapcenter: coordinate})
        });
    }


    render() {
        return (
            <div>
                {/*MapComponent*/}
                <div style = {{float: 'right', width: '82%', height: '100%', overflowX: 'hidden'}}> 
                <MapComponent onStartChange = {this.handleMapStartChange} 
                    onEndChange = {this.handleMapEndChange}
                    startPoint = {this.state.startPoint}
                    endPoint = {this.state.endPoint}
                    isStartingMarkerShown = {this.state.isStartingMarkerShown}
                    isEndMarkerShown = {this.state.isEndMarkerShown}
                    mapcenter = {this.state.mapcenter}
                    renderRoute = {this.state.renderRoute}
                    route = {this.state.route}
                    />
                </div>
                {/*Div for InputForm component, Error message, and RouteStats component*/}
                <div style = {{marginLeft: "20px", width: '17%', height: '100%'}}>
                <label style = {{color: 'darkcyan', fontFamily: '"Trebuchet MS", Helvetica, sans-serif ', fontSize: '275%'}}>EleNa</label>
                {/* <h1 style = {{color: 'darkcyan', fontFamily: '"Trebuchet MS", Helvetica, sans-serif '}}>EleNa</h1> */}
                {/*InputForm*/}
                <InputForm style = {{marginTop: '10px'}}onStartChange = {this.handleInputStartChange}
                    onEndChange = {this.handleInputEndChange}
                    onTypeChange = {this.handleInputTypeChange}
                    onPercentChange = {this.handleInputPercentChange}
                    startLocation = {this.state.startPoint}
                    endLocation = {this.state.endPoint}
                    startAddress = {this.state.startAddress}
                    endAddress = {this.state.endAddress}
                    submit = {this.handleSubmit}
                />
                {/*Displays error message if invalid start/end points are subitted*/}
                {this.state.errorMessage && <h3 className="error" style = {{color: 'red'}}> {this.state.errorMessage}</h3>}
                {/*RouteStats*/}
                <RouteStats elevation = {this.state.totalElevation}
                    distance = {this.state.totalDistance}/>

                </div>
            </div>
        );
    }
}

export default Display;
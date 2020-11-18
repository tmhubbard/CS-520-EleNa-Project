import React from 'react';
import InputForm from './InputForm';
import MapComponent from './MapComponent';
import RouteStats from './RouteStats';

class Display extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mapCenter: {lat: 42.3732, lng: -72.5199},
            route: null,
            renderRoute: false,
            isStartingMarkerShown: false,
            isEndMarkerShown: false,
            startPoint: null,
            endPoint: null,
            elevationType: "min",
            percentRoute: 10,
            startAddress: '',
            endAddress: '',
            totalElevation: 0,
            totalDistance:  0
        };

        this.handleMapStartChange = this.handleMapStartChange.bind(this);
        this.handleMapEndChange = this.handleMapEndChange.bind(this);
        this.handleInputStartChange = this.handleInputStartChange.bind(this);
        this.handleInputEndChange = this.handleInputEndChange.bind(this);
        this.handleInputTypeChange = this.handleInputTypeChange.bind(this);
        this.handleInputPercentChange = this.handleInputPercentChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    //callback functions
    handleMapStartChange(location, address) {
        this.setState({isStartingMarkerShown: true, startPoint : location, startAddress: address, mapCenter: location});
        console.log(location);
        console.log(address);
    }

    handleMapEndChange(location, address) {
        this.setState({isEndMarkerShown: true, endPoint: location, endAddress: address, mapCenter: location});
        console.log(location);
        console.log(address);
    }

    handleInputStartChange(location, address) {
        this.setState({isStartingMarkerShown: true, startPoint: location,
        startAddress: address, mapCenter: location});
        console.log(location);
        console.log(address);
    }

    handleInputEndChange(location, address) {
        this.setState({isEndMarkerShown: true, endPoint : location,
        endAddress: address, mapCenter: location});
        console.log(location);
        console.log(address);
    }

    handleInputTypeChange(type) {
        this.setState({elevationType: type});
        console.log(type);
    }

    handleInputPercentChange(percent) {
        this.setState({percentRoute: percent});
        console.log(percent);
    }

    // handleRecenter(location) {
    //     this.setState({mapCenter: location});
    //     console.log(location);
    // }

    handleSubmit() {
        var submission = {
            start_point: this.state.startPoint,
            end_point: this.state.endPoint,
            elevation_type: this.state.elevationType,
            percent_of_distance: this.state.percentRoute,
        }
        var JSONsubmission = JSON.stringify(submission);
        // console.log(JSONsubmission);
        //send data to backend
        //then request data back?

        fetch("http://localhost:5000/getRoute", {
          method: 'POST',
          body: JSONsubmission
        })
        .then(res => res.json())
        .then(json => {
            this.setState({
              route: json.route,
              renderRoute: true,
              totalDistance: json.total_distance_travelled,
              totalElevation: json.total_elevation_gain
            });
            // console.log(json);

            var pathCoordinates = this.state.route;
            console.log(this.state.route);
            var bounds = new window.google.maps.LatLngBounds();
            for (var i = 0; i < pathCoordinates.length; i++) {
                bounds.extend(pathCoordinates[i]);
            }
            var coordinate = {lat: bounds.getCenter().lat(), lng: bounds.getCenter().lng()};
            // console.log(coordinate);
            this.setState({mapCenter: coordinate})
        });
        
        
        
    }


    render() {
        return (
            <div>
                <MapComponent onStartChange = {this.handleMapStartChange} 
                    onEndChange = {this.handleMapEndChange}
                    startPoint = {this.state.startPoint}
                    endPoint = {this.state.endPoint}
                    recenter = {this.handleRecenter}
                    isStartingMarkerShown = {this.state.isStartingMarkerShown}
                    isEndMarkerShown = {this.state.isEndMarkerShown}
                    mapCenter = {this.state.mapCenter}
                    renderRoute = {this.state.renderRoute}
                    route = {this.state.route}
                    />
                {/* <div> */}
                <InputForm onStartChange = {this.handleInputStartChange}
                    onEndChange = {this.handleInputEndChange}
                    onTypeChange = {this.handleInputTypeChange}
                    onPercentChange = {this.handleInputPercentChange}
                    startLocation = {this.state.startPoint}
                    endLocation = {this.state.endPoint}
                    startAddress = {this.state.startAddress}
                    endAddress = {this.state.endAddress}
                    submit = {this.handleSubmit}
                />
                <RouteStats elevation = {this.state.totalElevation}
                    distance = {this.state.totalDistance}/>
                {/* </div> */}
            </div>
        );
    }
}

export default Display;
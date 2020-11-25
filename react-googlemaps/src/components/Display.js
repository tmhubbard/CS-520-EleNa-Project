import React from 'react';
import InputForm from './InputForm';
import MapComponent from './MapComponent';
import RouteStats from './RouteStats';

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

    //callback functions
    handleMapStartChange(location, address) {
        this.setState({isStartingMarkerShown: true, startPoint : location, startAddress: address, mapCenter: location});
    }

    handleMapEndChange(location, address) {
        this.setState({isEndMarkerShown: true, endPoint: location, endAddress: address, mapcenter: location});
    }

    handleInputStartChange(location, address) {
        if(location != null) {
            this.setState({isStartingMarkerShown: true, startPoint: location, startAddress: address});
        }
        else {
            this.setState({isStartingMarkerShown: false, startPoint: location, startAddress: address});
        }
    }

    handleInputEndChange(location, address) {
        if(location != null) {
            this.setState({isEndMarkerShown: true, endPoint : location, endAddress: address});
        }
        else {
            this.setState({isEndMarkerShown: false, endPoint : location, endAddress: address});
        }
    }

    handleInputTypeChange(type) {
        this.setState({elevationType: type});
    }

    handleInputPercentChange(percent) {
        this.setState({percentRoute: percent});
    }

    handleSubmit() {
        var submission = {
            start_point: this.state.startPoint,
            end_point: this.state.endPoint,
            elevation_type: this.state.elevationType,
            percent_of_distance: this.state.percentRoute,
        }
        var JSONsubmission = JSON.stringify(submission);
        if (this.state.startPoint == null || this.state.endPoint == null) {
            this.setState({errorMessage: "Error: no location selected for either start or end point"});
            return;
        }
        else {
            this.setState({errorMessage: ""});
        }

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
                <div style = {{marginLeft: "20px", width: '17%', height: '100%'}}>
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
                {this.state.errorMessage && <h3 className="error" style = {{color: 'red'}}> {this.state.errorMessage}</h3>}
                <RouteStats elevation = {this.state.totalElevation}
                    distance = {this.state.totalDistance}/>
                </div>
            </div>
        );
    }
}

export default Display;
import React from 'react';
import InputForm from './InputForm';
import MapComponent from './MapComponent';

class Display extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isStartingMarkerShown: false,
            isEndMarkerShown: false,
            startPoint: null,
            endPoint: null,
            elevationType: "min",
            percentRoute: 10,
            startAddress: '',
            endAddress: ''
        };

        this.handleMapStartChange = this.handleMapStartChange.bind(this);
        this.handleMapEndChange = this.handleMapEndChange.bind(this);
        this.handleInputStartChange = this.handleInputStartChange.bind(this);
        this.handleInputEndChange = this.handleInputEndChange.bind(this);
        this.handleInputTypeChange = this.handleInputTypeChange.bind(this);
        this.handleInputPercentChange = this.handleInputPercentChange.bind(this);
    }
    //callback functions
    handleMapStartChange(location) {
        this.setState({isStartingMarkerShown: true, startPoint : location});
        console.log(location);
    }

    handleMapEndChange(location) {
        this.setState({isEndMarkerShown: true, endPoint: location});
        console.log(location);
    }

    handleInputStartChange(location, address) {
        this.setState({isStartingMarkerShown: true, startPoint: location,
        startAddress: address});
        console.log(location);
        console.log(address);
    }

    handleInputEndChange(location, address) {
        this.setState({isEndMarkerShown: true, endPoint : location,
        endAddress: address});
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

    render() {
        return (
            <div>
                <MapComponent onStartChange = {this.handleMapStartChange} 
                    onEndChange = {this.handleMapEndChange}
                    startPoint = {this.state.startPoint}
                    endPoint = {this.state.endPoint}
                    isStartingMarkerShown = {this.state.isStartingMarkerShown}
                    isEndMarkerShown = {this.state.isEndMarkerShown}/>

                <InputForm onStartChange = {this.handleInputStartChange}
                    onEndChange = {this.handleInputEndChange}
                    onTypeChange = {this.handleInputTypeChange}
                    onPercentChange = {this.handleInputPercentChange}
                    startLocation = {this.state.startPoint}
                    endLocation = {this.state.endPoint}
                    // startAddress = {this.state.startAddress}
                    // endAddress = {this.state.endAddress}
                />
            </div>
        );
    }
}

export default Display;
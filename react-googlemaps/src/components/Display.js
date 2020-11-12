import React from 'react';
import InputForm from './InputForm';
import MapComponent from './MapComponent';

class Display extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            startPoint: null,
            endPoint: null,
            elevationType: "min",
            percentRoute: 10
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
        this.setState({startPoint : location});
    }

    handleMapEndChange(location) {
        this.setState({endPoint: location});
    }

    handleInputStartChange(location) {
        this.setState({startPoint: location});
    }

    handleInputEndChange(location) {
        this.setState({endPoint : location});
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
                    onEndChange = {this.handleMapEndChange}/>

                <InputForm onStartChange = {this.handleInputStartChange}
                    onEndChange = {this.handleInputEndChange}
                    onTypeChange = {this.handleInputTypeChange}
                    onPercentChange = {this.handleInputPercentChange}
                    />
            </div>
        );
    }
}

export default Display;
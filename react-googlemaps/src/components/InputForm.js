import React from 'react';
import Slider from './Slider';
import PlacesAutocomplete, { geocodeByAddress, getLatLng } from 'react-places-autocomplete';



class InputForm extends React.Component {
    constructor(props) {
        super(props);

        // this.state = {
        //     startPoint: null,
        //     endPoint: null,
        //     elevationType: "min",
        //     percentRoute: 10,
        //     startAddress: '',
        //     endAddress: ''
        // };
        this.handleStartAutocompleteChange = this.handleStartAutocompleteChange.bind(this);
        this.handleStartSelect = this.handleStartSelect.bind(this);
        this.handleEndAutocompleteChange = this.handleEndAutocompleteChange.bind(this);
        this.handleEndSelect = this.handleEndSelect.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleSliderChange = this.handleSliderChange.bind(this);
    }

    handleStartAutocompleteChange = startAddress => {
        // this.setState({ startAddress });
        this.props.onStartChange(null, startAddress);
    };

    handleStartSelect = async value => {
        const results = await geocodeByAddress(value);
        const latLng = await getLatLng(results[0]);
        // this.setState({startAddress: value, startPoint: latLng });
        this.props.onStartChange(latLng, value);
        // console.log(results[0].formatted_address);
        // console.log(latLng);
    };

    handleEndAutocompleteChange = endAddress => {
        // this.setState({ endAddress });
        this.props.onEndChange(null, endAddress);
    };

    handleEndSelect = async value => {
        const results = await geocodeByAddress(value);
        const latLng = await getLatLng(results[0]);
        // this.setState({endAddress: value, endPoint: latLng });
        this.props.onEndChange(latLng, value);
        // console.log(this.state.endPoint);
    };
    
      

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        //console.log(value);

        if(name === "elevationType"){
            this.props.onTypeChange(value);
        }
    }

    handleSubmit(event) {
        event.preventDefault(); //prevents form from actually being submitted
        this.props.submit();
    }
    
    handleSliderChange(percent) {
        this.setState({percentRoute: percent});
        this.props.onPercentChange(percent);
        //console.log(this.state.percentRoute);
    }

    render() {
        // console.log(this.state.startAddress);
        console.log(this.props.startAddress);
        return (
            <div //style={{float: 'left', width: '25%', height: '100%'}}
            >
            <form onSubmit = {this.handleSubmit}>
                <label style={{fontWeight: "bold"}}>
                    Start Point
                    <br />
                    <PlacesAutocomplete
                        value={this.props.startAddress}
                        onChange={this.handleStartAutocompleteChange}
                        onSelect={this.handleStartSelect}
                    >
                        {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                            <div>
                                <input
                                {...getInputProps({
                                    placeholder: 'Search Places ...',
                                    className: 'location-search-input',
                                })}
                                />
                                <div className="autocomplete-dropdown-container">
                                {loading && <div>Loading...</div>}
                                {suggestions.map(suggestion => {
                                    const className = suggestion.active
                                    ? 'suggestion-item--active'
                                    : 'suggestion-item';
                                    // inline style for demonstration purpose
                                    const style = suggestion.active
                                    ? { backgroundColor: '#fafafa', cursor: 'pointer' }
                                    : { backgroundColor: '#ffffff', cursor: 'pointer' };

                                    return (
                                    <div
                                        {...getSuggestionItemProps(suggestion, {
                                        className,
                                        style,
                                        })}
                                    >
                                        <span>{suggestion.description}</span>
                                    </div>
                                    );
                                })}
                                </div>
                            </div>
                            )}
                    </PlacesAutocomplete>
                </label>
                <br />
                <label style={{fontWeight: "bold"}}>
                    End Point
                    <br />
                    <PlacesAutocomplete
                        value={this.props.endAddress}
                        onChange={this.handleEndAutocompleteChange}
                        onSelect={this.handleEndSelect}
                    >
                        {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                            <div>
                                <input
                                {...getInputProps({
                                    placeholder: 'Search Places ...',
                                    className: 'location-search-input',
                                })}
                                />
                                <div className="autocomplete-dropdown-container">
                                {loading && <div>Loading...</div>}
                                {suggestions.map(suggestion => {
                                    const className = suggestion.active
                                    ? 'suggestion-item--active'
                                    : 'suggestion-item';
                                    // inline style for demonstration purpose
                                    const style = suggestion.active
                                    ? { backgroundColor: '#fafafa', cursor: 'pointer' }
                                    : { backgroundColor: '#ffffff', cursor: 'pointer' };

                                    return (
                                    <div
                                        {...getSuggestionItemProps(suggestion, {
                                        className,
                                        style,
                                        })}
                                    >
                                        <span>{suggestion.description}</span>
                                    </div>
                                    );
                                })}
                                </div>
                            </div>
                            )}
                    </PlacesAutocomplete>
                </label>
                <br />
                <label style={{fontWeight: "bold"}}>
                    Type of Route:
                </label>
                <div style={{display: "block"}}>
                    <input type="radio" id="min" name="elevationType" value="min" onChange={this.handleChange}/>
                    <label htmlFor="min">Minimum Elevation</label>
                    <br />
                    <input type="radio" id="max" name="elevationType" value="max" onChange={this.handleChange}/>
                    <label htmlFor="max">Maximum Elevation</label>
                </div>
                <br />
                <label style={{fontWeight: "bold"}}>
                    Maximum Distance:
                </label>
                <div className="slidecontainer">
                    <Slider onSliderChange = {this.handleSliderChange}/>
                </div>
                <input type="submit" value="Find Route" style={{marginLeft: "20px"}}/>
            </form>
            </div>
        );
    }
}

export default InputForm;
import React from 'react';
import Slider from './Slider';
import PlacesAutocomplete, { geocodeByAddress, getLatLng } from 'react-places-autocomplete';



class InputForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            startPoint: null,
            endPoint: null,
            elevationType: "min",
            percentRoute: 10,
            startLatLng: null,
            endLatLng: null,
            startAddress: '',
            endAddress: ''
        };

        this.handleStartAutocompleteChange = this.handleStartAutocompleteChange.bind(this);
        this.handleStartSelect = this.handleStartSelect.bind(this);
        this.handleEndAutocompleteChange = this.handleEndAutocompleteChange.bind(this);
        this.handleEndSelect = this.handleEndSelect.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleSliderChange = this.handleSliderChange.bind(this);
    }

    handleStartAutocompleteChange = startAddress => {
        this.setState({ startAddress });
    };

    handleStartSelect = async value => {
        const results = await geocodeByAddress(value);
        const latLng = await getLatLng(results[0]);
        this.setState({
            startAddress: value,
            startLatLng: latLng
        });
        // console.log(this.state.startLatLng);
    };

    handleEndAutocompleteChange = endAddress => {
        this.setState({ endAddress });
    };

    handleEndSelect = async value => {
        const results = await geocodeByAddress(value);
        const latLng = await getLatLng(results[0]);
        this.setState({
            endAddress: value,
            endLatLng: latLng
        });
        // console.log(this.state.endLatLng);
    };
    
      

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        //console.log(value);
        this.setState({
            [name]: value
        });

        if(name === "startPoint"){
            this.props.onStartChange(value);
        }
        else if(name === "endPoint"){
            this.props.onEndChange(value);
        }
        else if(name === "elevationType"){
            this.props.onPercentChange(value);
        }
    }

    handleSubmit(event) {
        //console.log("form submitted");
        event.preventDefault(); //prevents form from actually being submitted
    }
    
    handleSliderChange(percent) {
        this.setState({percentRoute: percent});
        this.props.onPercentChange(percent);
        //console.log(this.state.percentRoute);
    }

    render() {
        return (
            <div style={{float: 'left', width: '25%', height: '100%'}}>
            <form>
                <label>
                    Start Point
                    <br />
                    <PlacesAutocomplete
                        value={this.state.startAddress}
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
                <label>
                    End Point
                    <br />
                    <PlacesAutocomplete
                        value={this.state.endAddress}
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
                <label>
                    Type of Route:
                    <br />
                    <input type="radio" id="min" name="elevationType" value="min" onChange={this.handleChange}/>
                    <label htmlFor="min">Minimum Elevation</label>
                    <input type="radio" id="max" name="elevationType" value="max" onChange={this.handleChange}/>
                    <label htmlFor="max">Maximum Elevation</label>
                </label>
                <br />
                <label>
                    Distance (Percent of Route):
                </label>
                <div className="slidecontainer">
                    <Slider onSliderChange = {this.handleSliderChange}/>
                </div>
                <input type="submit" value="Find Route" />
            </form>
            </div>
        );
    }
}

export default InputForm;
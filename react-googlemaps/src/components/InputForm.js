import React from 'react';
import Slider from './Slider';
import PlacesAutocomplete, { geocodeByAddress, getLatLng } from 'react-places-autocomplete';

//InputForm component handles majority of the user input,
//has no state because it passes all the information via callback functions to parent component Display
class InputForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleStartAutocompleteChange = this.handleStartAutocompleteChange.bind(this);
        this.handleStartSelect = this.handleStartSelect.bind(this);
        this.handleEndAutocompleteChange = this.handleEndAutocompleteChange.bind(this);
        this.handleEndSelect = this.handleEndSelect.bind(this);
        this.handleTypeChange = this.handleTypeChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleSliderChange = this.handleSliderChange.bind(this);
    }

    /*ALL CHANGES ARE HANDLED BY USING THE CALLBACK FUNCTIONS PASSED AS PROPS BY DISPLAY COMPONENT
    --------------------------------------------------------------------------------------------*/

    //handles change in start location Autocomplete search bar
    handleStartAutocompleteChange = startAddress => {
        this.props.onStartChange(null, startAddress);
    };

    //handles selection in start location Autocomplete search bar
    handleStartSelect = async value => {
        const results = await geocodeByAddress(value);
        const latLng = await getLatLng(results[0]);
        this.props.onStartChange(latLng, value);
    };

    //handles change in end location Autocomplete search bar
    handleEndAutocompleteChange = endAddress => {
        this.props.onEndChange(null, endAddress);
    };

    //handles selection in end location Automcomplete search bar
    handleEndSelect = async value => {
        const results = await geocodeByAddress(value);
        const latLng = await getLatLng(results[0]);
        this.props.onEndChange(latLng, value);
    }; 

    //handles changes to radio buttons regarding the type of route (min vs max)
    handleTypeChange(event) {
        this.props.onTypeChange(event.target.value);
    }

    //handles submit button
    handleSubmit(event) {
        //prevents page from being refreshed
        event.preventDefault();
        this.props.submit();
    }
    
    //handles changes to the slider component
    handleSliderChange(percent) {
        this.props.onPercentChange(percent);
    }

    render() {  
        const minChecked = this.props.elevationType === "min" ? true : false;    
        return (
            <div>
            <form onSubmit = {this.handleSubmit}>
                {/*Start point autocomplete search bar element*/}
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
                {/*End point autocomplete search bar element*/}
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
                {/*Route Elevation type radio buttons*/}
                <label style={{fontWeight: "bold"}}>
                    Type of Route:
                </label>
                <div style={{display: "block"}}>
                    <input type="radio" id="min" name="elevationType" value="min" checked={minChecked} onChange={this.handleTypeChange}/>
                    <label htmlFor="min">Minimum Elevation</label>
                    <br />
                    <input type="radio" id="max" name="elevationType" value="max" checked={!minChecked} onChange={this.handleTypeChange}/>
                    <label htmlFor="max">Maximum Elevation</label>
                </div>
                <br />
                {/*Distance slider bar element*/}
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
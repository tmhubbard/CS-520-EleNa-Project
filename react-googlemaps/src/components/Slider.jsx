import React from 'react';

//This is the slider component for determining the percentage of route
class Slider extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: 120
        }

        this.handleOnChange = this.handleOnChange.bind(this);
    }

    //on change updates both state and callback function passed in props by InputForm
    handleOnChange(event) {
        this.setState({value: event.target.value});
        this.props.onSliderChange(event.target.value);
    }

    //renders html element "range" (the slider) and the current value below it
    render() {
        return (
            <div>
            <input type="range" min="100" max="200" step="1" value={this.state.value} className="slider" onChange={this.handleOnChange} />
            <p style={{marginLeft: "50px", marginTop: "0px"}}>{this.state.value}%</p>
            </div>
        );
    }
}
export default Slider;
import React from 'react';

class Slider extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: 10
        }

        this.handleOnChange = this.handleOnChange.bind(this);
    }

    handleOnChange(event) {
        this.setState({value: event.target.value});
        this.props.onSliderChange(event.target.value);
    }

    render() {
        return (
            <div>
            <input type="range" min="0" max="100" value={this.state.value} className="slider" onChange={this.handleOnChange} />
            <p style={{marginLeft: "50px", marginTop: "0px"}}>{this.state.value}</p>
            </div>
        );
    }
}
export default Slider;
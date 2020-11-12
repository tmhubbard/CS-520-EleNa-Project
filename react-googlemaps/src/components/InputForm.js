import React from 'react';
import Slider from './Slider';

class InputForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            startPoint: null,
            endPoint: null,
            elevationType: "min",
            percentRoute: 10
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleSliderChange = this.handleSliderChange.bind(this);
    }

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
            <div style={{float: 'right'}}>
            <form>
                <label>
                    Start Point
                    <br />
                    <input  />
                </label>
                <br />
                <label>
                    End Point
                    <br />
                    <input />
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
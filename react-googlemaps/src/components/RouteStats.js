import React from 'react';

//This is the component that displays the statistics of the route received
class RouteStats extends React.Component {
    render() {
        return (
            <div style={{float: 'left', clear: 'both', marginTop: "10px"}}>
                <label style={{fontWeight: "bold"}}>
                    Total Elevation Gain:
                    <p style={{fontWeight: "normal", marginLeft: "10px"}}>
                        {this.props.elevation} meters
                    </p>
                </label>
                <label style={{fontWeight: "bold"}}>
                    Total Distance:
                    <p style={{fontWeight: "normal", marginLeft: "10px"}}>
                        {this.props.distance} meters
                    </p>
                </label>
            </div>
        );
    }
}

export default RouteStats;
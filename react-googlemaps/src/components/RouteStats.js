import React from 'react';

class RouteStats extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={{float: 'left', clear: 'both'}}>
                <label>
                    Total Elevation Gain:
                    <p>
                        {this.props.elevation} meters
                    </p>
                </label>
                <label>
                    Total Distance:
                    <p>
                        {this.props.distance} meters
                    </p>
                </label>
            </div>
        );
    }
}

export default RouteStats;
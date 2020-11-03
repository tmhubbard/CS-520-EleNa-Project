import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';

const mapStyles = {
  width: '100%',
  height: '100%'
};

export class MapContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isStartingMarkerShown: false,
      startingMarkerPosition: null,
      isEndMarkerShown: false,
      endMarkerPosition: null
    };
    this.handleMapClick = this.handleMapClick.bind(this);
    this.handleMapRightClick = this.handleMapRightClick.bind(this);
  }

  handleMapClick = (ref, map, ev) => {
    const location = ev.latLng;
    this.setState({
      isStartingMarkerShown: true,
      startingMarkerPosition: location
    });
    // console.log(location);
    map.panTo(location);
  };

  handleMapRightClick = (ref, map, ev) => {
    const location = ev.latLng;
    this.setState({
      isEndMarkerShown: true,
      endMarkerPosition: location
    });
    // console.log(location);
    map.panTo(location);
  };

  onStartingMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    
    this.setState({
      isStartingMarkerShown: true,
      startingMarkerPosition: latLng
    });
    // console.log(latLng);

  };

  onEndMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    
    this.setState({
      isEndMarkerShown: true,
      endMarkerPosition: latLng
    });
    // console.log(latLng);

  };



  render() {
    return (
      <Map
        google={this.props.google}
        zoom={14}
        style={mapStyles}
        initialCenter={
          {
            lat: 42.3732,
            lng: -72.5199
          }
        }
        onClick={this.handleMapClick}
        onRightclick={this.handleMapRightClick}
      >
        {this.state.isStartingMarkerShown && 
        <Marker 
        position={this.state.startingMarkerPosition}
        draggable={true}
        label="A"
        onDragend={(t, map, coord) => this.onStartingMarkerDragEnd(coord)}
        />}
        {this.state.isEndMarkerShown && 
        <Marker 
        position={this.state.endMarkerPosition}
        draggable={true}
        label="B"
        onDragend={(t, map, coord) => this.onEndMarkerDragEnd(coord)}
        />}

      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA'
})(MapContainer);
import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, Polyline } from 'google-maps-react';

const mapStyles = {
  width: '100%',
  height: '100%'
};

export class MapComponent extends Component {
  constructor(props) {
    super(props);
    // this.state = {
    //   isStartingMarkerShown: false,
    //   startingMarkerPosition: null,
    //   isEndMarkerShown: false,
    //   endMarkerPosition: null
    // };
    this.handleMapClick = this.handleMapClick.bind(this);
    this.handleMapRightClick = this.handleMapRightClick.bind(this);
  }

  handleMapClick = (ref, map, ev) => {
    const location = ev.latLng;
    var coordinate = {lat: location.lat(), lng: location.lng()};  //creating latlng object in {lat, lng} format
    this.setState({
      isStartingMarkerShown: true,
      startingMarkerPosition: coordinate
    });
    //callback function to Display
    this.props.onStartChange(coordinate);
    map.panTo(location);



    //this is how we turn a google maps api latLng object to a readable JSON object
    //var object = JSON.stringify(ev.latLng.toJSON(), null, 2);
  };

  handleMapRightClick = (ref, map, ev) => {
    const location = ev.latLng;
    var coordinate = {lat: location.lat(), lng: location.lng()};  //creating latlng object in {lat, lng} format
    this.setState({
      isEndMarkerShown: true,
      endMarkerPosition: coordinate
    });
    //callback function to Display
    this.props.onEndChange(coordinate);
    //console.log(location);
    map.panTo(location);
  };

  onStartingMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    var coordinate = {lat: latLng.lat(), lng: latLng.lng()};  //creating latlng object in {lat, lng} format
    this.setState({
      isStartingMarkerShown: true,
      startingMarkerPosition: coordinate
    });
    this.props.onStartChange(coordinate);
    // console.log(latLng);
  };

  onEndMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    var coordinate = {lat: latLng.lat(), lng: latLng.lng()};  //creating latlng object in {lat, lng} format
    this.setState({
      isEndMarkerShown: true,
      endMarkerPosition: coordinate
    });
    this.props.onEndChange(coordinate);
    // console.log(latLng);
  };

  receiveStartPoint(props) {
    this.setState({startingMarkerPosition: props.startLocation});
  }

  receiveEndPoint(props) {
    this.setState({endMarkerPosition: props.endLocation});
  }



  render() {
    // const pathCoordinates = [
    //   { lat: 42.37380692489817, lng: -72.53280681833881 },
    //   { lat: 42.37314905741523, lng: -72.51986784205097 }
    // ];
    return (
      <div style = {{float: 'right', width: '75%', height: '100%'}}>
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
          {/* <Polyline
            path={pathCoordinates}
            geodesic={true}
            options={{
                strokeColor: "#ff2527",
                strokeOpacity: 0.75,
                strokeWeight: 2,
            }}
            /> */}
          {this.props.isStartingMarkerShown && 
          <Marker 
          position={this.props.startPoint}
          draggable={true}
          label="A"
          onDragend={(t, map, coord) => this.onStartingMarkerDragEnd(coord)}
          />}
          {this.props.isEndMarkerShown && 
          <Marker 
          position={this.props.endPoint}
          draggable={true}
          label="B"
          onDragend={(t, map, coord) => this.onEndMarkerDragEnd(coord)}
          />}

        </Map>
      </div>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA'
})(MapComponent);
import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, Polyline } from 'google-maps-react';
import Geocode from 'react-geocode';


const mapStyles = {
  width: '75%',
  height: '100%'
};

export class MapComponent extends Component {
  constructor(props) {
    super(props);
    this.handleMapClick = this.handleMapClick.bind(this);
    this.handleMapRightClick = this.handleMapRightClick.bind(this);
  }

  handleMapClick = (ref, map, ev) => {
    const location = ev.latLng;
    var coordinate = {lat: location.lat(), lng: location.lng()};  //creating latlng object in {lat, lng} format    
    let address = "";
    Geocode.setApiKey("AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA");
    Geocode.fromLatLng(location.lat(), location.lng()).then(
      response => {
        address = response.results[0].formatted_address;
        this.props.onStartChange(coordinate, address);
      },
      error => {
        console.error(error);
      }
    );
    //callback function to Display
    
    map.panTo(location);

    //this is how we turn a google maps api latLng object to a readable JSON object
    //var object = JSON.stringify(ev.latLng.toJSON(), null, 2);
  };

  handleMapRightClick = (ref, map, ev) => {
    const location = ev.latLng;
    var coordinate = {lat: location.lat(), lng: location.lng()};  //creating latlng object in {lat, lng} format    
    let address = "";
    Geocode.setApiKey("AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA");
    Geocode.fromLatLng(location.lat(), location.lng()).then(
      response => {
        address = response.results[0].formatted_address;
        this.props.onEndChange(coordinate, address);
      },
      error => {
        console.error(error);
      }
    );
    //callback function to Display
    
    //console.log(location);
    map.panTo(location);
  };

  onStartingMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    var coordinate = {lat: latLng.lat(), lng: latLng.lng()};  //creating latlng object in {lat, lng} format    
    let address = "";
    Geocode.setApiKey("AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA");
    Geocode.fromLatLng(latLng.lat(), latLng.lng()).then(
      response => {
        address = response.results[0].formatted_address;
        this.props.onStartChange(coordinate, address);
      },
      error => {
        console.error(error);
      }
    );
    // console.log(latLng);
  };

  onEndMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    var coordinate = {lat: latLng.lat(), lng: latLng.lng()};  //creating latlng object in {lat, lng} format
    let address = "";
    Geocode.setApiKey("AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA");
    Geocode.fromLatLng(latLng.lat(), latLng.lng()).then(
      response => {
        address = response.results[0].formatted_address;
        this.props.onEndChange(coordinate, address);
      },
      error => {
        console.error(error);
      }
    );
    
    // console.log(latLng);
  };

  receiveStartPoint(props) {
    this.setState({startingMarkerPosition: props.startLocation});
  }

  receiveEndPoint(props) {
    this.setState({endMarkerPosition: props.endLocation});
  }



  render() {
    var pathCoordinates = this.props.route;
    
    return (
      <div style = {{float: 'right', width: '75%', height: '100%'}}>
        <Map
          google={this.props.google}
          zoom={14}
          style={mapStyles}
          initialCenter= {{lat: 42.3732, lng: -72.5199}}
          center= {this.props.mapcenter}
          onClick={this.handleMapClick}
          onRightclick={this.handleMapRightClick}
        >
          {this.props.renderRoute &&
          // <div>
          //   {coordinates}
          //   </div>
          <Polyline
          path={pathCoordinates}
          geodesic={true}
          options={{
              strokeColor: "#FF2527",
              strokeOpacity: 0.75,
              strokeWeight: 2
          }}/>
          }
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
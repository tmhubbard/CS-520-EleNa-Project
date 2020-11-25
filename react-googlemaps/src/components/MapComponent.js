import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Marker, Polyline } from 'google-maps-react';
import Geocode from 'react-geocode';


const mapStyles = {
  width: '82%',
  height: '100%',
  overflowX: 'hidden'
};

export class MapComponent extends Component {
  constructor(props) {
    super(props);
    this.handleMapClick = this.handleMapClick.bind(this);
    this.handleMapRightClick = this.handleMapRightClick.bind(this);
  }

  //updates parent Display component state on a left click (adding start marker to map)
  handleMapClick = (ref, map, ev) => {
    const location = ev.latLng;
    var coordinate = {lat: location.lat(), lng: location.lng()};  //creating latlng object in {lat, lng} format    
    let address = "";

    // gets address of location given latlng values using Google Maps Geocode library
    Geocode.setApiKey("AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA");
    Geocode.fromLatLng(location.lat(), location.lng()).then(
      response => {
        address = response.results[0].formatted_address;
        this.props.onStartChange(coordinate, address);
        map.panTo(location);
      },
      error => {
        console.error(error);
      }
    );
  };

  //updates parent Display component state on a right click (adding end marker to map)
  handleMapRightClick = (ref, map, ev) => {
    const location = ev.latLng;
    var coordinate = {lat: location.lat(), lng: location.lng()};  //creating latlng object in {lat, lng} format    
    let address = "";

    // gets address of location given latlng values using Google Maps Geocode library
    Geocode.setApiKey("AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA");
    Geocode.fromLatLng(location.lat(), location.lng()).then(
      response => {
        address = response.results[0].formatted_address;
        this.props.onEndChange(coordinate, address);
        map.panTo(location);
      },
      error => {
        console.error(error);
      }
    );
  };

  //updates parent Display component state on the conclusion of the dragging of start marker
  onStartingMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    var coordinate = {lat: latLng.lat(), lng: latLng.lng()};  //creating latlng object in {lat, lng} format    
    let address = "";

    // gets address of location given latlng values using Google Maps Geocode library
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
  };

  //updates parent Display component state on the conclusion of the dragging of end marker
  onEndMarkerDragEnd = (coord) => {
    const { latLng } = coord;
    var coordinate = {lat: latLng.lat(), lng: latLng.lng()};  //creating latlng object in {lat, lng} format
    let address = "";

    // gets address of location given latlng values using Google Maps Geocode library
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
  };

  render() {
    var pathCoordinates = this.props.route;
    
    return (
        <Map
          google={this.props.google}
          zoom={14}
          style={mapStyles}
          initialCenter= {{lat: 42.3732, lng: -72.5199}}
          center= {this.props.mapcenter}
          onClick={this.handleMapClick}
          onRightclick={this.handleMapRightClick}
        >
          {/* if renderRoute is true, draw polylines to represent the route */}
          {this.props.renderRoute &&
            <Polyline
            path={pathCoordinates}
            geodesic={true}
            options={{
                strokeColor: "#FF2527",
                strokeOpacity: 1.0,
                strokeWeight: 3
            }}/>
          }

          {/* If isStartingMarkerShown is true, render the start Marker */}
          {this.props.isStartingMarkerShown && 
            <Marker 
            position={this.props.startPoint}
            draggable={true}
            label="A"
            onDragend={(t, map, coord) => this.onStartingMarkerDragEnd(coord)}
            />
          }

          {/* If isStartingMarkerShown is true, render the start Marker */}
          {this.props.isEndMarkerShown && 
            <Marker 
            position={this.props.endPoint}
            draggable={true}
            label="B"
            onDragend={(t, map, coord) => this.onEndMarkerDragEnd(coord)}
            />
          }
        </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyCyrU7Z1OXQxOpvVMsQVk1FZvWWb3R3ssA'
})(MapComponent);
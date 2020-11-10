import React, { Component } from 'react';
import InputForm from './components/InputForm';
import MapComponent from './components/MapComponent';

class App extends Component {
  render() {
    return (
      <div>
        <MapComponent />
        <InputForm style={{float: 'right'}}/>
      </div>
      
    );
  }
}

export default App;
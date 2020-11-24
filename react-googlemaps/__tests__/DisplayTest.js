import React from 'react';
import Display from '../src/components/Display';
import { shallow, mount, render, ReactWrapper } from 'enzyme';
import Enzyme from 'enzyme';
import Adapter from '@wojtekmaj/enzyme-adapter-react-17';
import InputForm from '../src/components/InputForm';
import RouteStats from '../src/components/RouteStats';

Enzyme.configure({ adapter: new Adapter() });


// ensures Display component renders child components correctly upon initalization
it('renders correctly', () => {
    const result = shallow(<Display />);
    // console.log(result.debug());
    expect(result.debug()).toMatchSnapshot();
});


it('renders GoogleMaps Wrapper', () => {
    const result = shallow(<Display />);
    expect(result.find('Wrapper').exists()).toBe(true);
});


it('renders InputForm and RouteStats', () => {
    const result = shallow(<Display />);
    expect(result.find(InputForm).exists()).toBe(true);
    expect(result.find(RouteStats).exists()).toBe(true);
});


it('renders error header correctly', () => {
    const result = shallow(<Display />);
    expect(result.find('h3').exists()).toBe(false);
    result.find(InputForm).prop('submit')();
    expect(result.find('h3').exists()).toBe(true)
});

it('handleMapStartChange callback function modifies Display state correctly', () => {
    const result = shallow(<Display />);
    expect(result.state('isStartingMarkerShown')).toBe(false);
    expect(result.state('startPoint')).toBe(null);
    expect(result.state('startAddress')).toBe('');
    result.find('Wrapper').prop('onStartChange')({lat: 42.37849519999998, lng: -72.52029559999998}, '39 196 N Pleasant St, Amherst, MA 01002, USA');
    expect(result.state('isStartingMarkerShown')).toBe(true);
    expect(result.state('startPoint')).toStrictEqual({lat: 42.37849519999998, lng: -72.52029559999998});
    expect(result.state('startAddress')).toBe('39 196 N Pleasant St, Amherst, MA 01002, USA');
});

it('handleMapEndChange callback function modifies Display state correctly', () => {
    const result = shallow(<Display />);
    expect(result.state('isEndMarkerShown')).toBe(false);
    expect(result.state('endPoint')).toBe(null);
    expect(result.state('endAddress')).toBe('');
    result.find('Wrapper').prop('onEndChange')({lat: 42.37849519999998, lng: -72.52029559999998}, '39 196 N Pleasant St, Amherst, MA 01002, USA');
    expect(result.state('isEndMarkerShown')).toBe(true);
    expect(result.state('endPoint')).toStrictEqual({lat: 42.37849519999998, lng: -72.52029559999998});
    expect(result.state('endAddress')).toBe('39 196 N Pleasant St, Amherst, MA 01002, USA');
});

it('handleInputStartChange callback function modifies Display state correctly', () => {
    const result = shallow(<Display />);
    expect(result.state('isStartingMarkerShown')).toBe(false);
    expect(result.state('startPoint')).toBe(null);
    expect(result.state('startAddress')).toBe('');
    result.find(InputForm).prop('onStartChange')({lat: 42.37849519999998, lng: -72.52029559999998}, '39 196 N Pleasant St, Amherst, MA 01002, USA');
    expect(result.state('isStartingMarkerShown')).toBe(true);
    expect(result.state('startPoint')).toStrictEqual({lat: 42.37849519999998, lng: -72.52029559999998});
    expect(result.state('startAddress')).toBe('39 196 N Pleasant St, Amherst, MA 01002, USA');
});

it('handleInputEndChange callback function modifies Display state correctly', () => {
    const result = shallow(<Display />);
    expect(result.state('isEndMarkerShown')).toBe(false);
    expect(result.state('endPoint')).toBe(null);
    expect(result.state('endAddress')).toBe('');
    result.find(InputForm).prop('onEndChange')({lat: 42.37849519999998, lng: -72.52029559999998}, '39 196 N Pleasant St, Amherst, MA 01002, USA');
    expect(result.state('isEndMarkerShown')).toBe(true);
    expect(result.state('endPoint')).toStrictEqual({lat: 42.37849519999998, lng: -72.52029559999998});
    expect(result.state('endAddress')).toBe('39 196 N Pleasant St, Amherst, MA 01002, USA');
});


it('handleInputTypeChange callback function modifies Display state correctly', () => {
    const result = shallow(<Display />);
    expect(result.state('elevationType')).toBe("min");
    result.find(InputForm).prop('onTypeChange')("min");
    expect(result.state('elevationType')).toBe("min");
    result.find(InputForm).prop('onTypeChange')("max");
    expect(result.state('elevationType')).toBe("max");
    result.find(InputForm).prop('onTypeChange')("min");
    expect(result.state('elevationType')).toBe("min");
});

it('handleInputPercentChange callback function modifies Display state correctly', () => {
    const result = shallow(<Display />);
    expect(result.state('percentRoute')).toBe(120);
    result.find(InputForm).prop('onPercentChange')(130);
    expect(result.state('percentRoute')).toBe(130);
});



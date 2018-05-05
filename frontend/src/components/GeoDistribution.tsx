import * as React from 'react';
import {GoogleMap, Marker, withGoogleMap, withScriptjs} from 'react-google-maps';

export interface GeoDistributionProps {
}

const MapWithAMarker = withScriptjs(withGoogleMap(_ =>
    <GoogleMap
        defaultZoom={8}
        defaultCenter={{lat: -34.397, lng: 150.644}}
    >
        <Marker
            position={{lat: -34.397, lng: 150.644}}
        />
    </GoogleMap>
));


export default class GeoDistribution extends React.Component<GeoDistributionProps, any> {


    render() {
        return (
            <div>
                <MapWithAMarker
                    googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyC4R6AN7SmujjPUIGKdyao2Kqitzr1kiRg&v=3.exp&libraries=geometry,drawing,places"
                    loadingElement={<div style={{height: `100%`}}/>}
                    containerElement={<div style={{height: `400px`}}/>}
                    mapElement={<div style={{height: `100%`}}/>}
                />
            </div>
        );
    }
}


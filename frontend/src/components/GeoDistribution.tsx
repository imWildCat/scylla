import * as React from 'react';
import axios from "axios";
import {getBaseURL, Proxy, ResponseJSON} from "../utils";
import {Tooltip} from "react-tooltip"

import {
    ComposableMap,
    ZoomableGroup,
    Geographies,
    Geography,
    Marker,
} from 'react-simple-maps';

export interface GeoDistributionProps {
}

export interface GeoDistributionState {
    proxies: Proxy[],
}

export default class GeoDistribution extends React.Component<GeoDistributionProps, GeoDistributionState> {

    constructor(props: GeoDistributionProps) {
        super(props);
        this.state = {
            proxies: [],
        };
    }

    componentDidMount() {
        this.loadData();
    }
    render() {
        return (
            <div>
                <ComposableMap style={{width: "100%"}}>
                    <ZoomableGroup>
                        <Geographies geography={'https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-50m-simplified.json'}>
                            {({ geographies }) => geographies.map((geography) => (
                                <Geography
                                    key={geography.properties.ISO_A3 + '_' + geography.properties.NAME}
                                    geography={geography}
                                    style={{
                                        default: {fill: "#D8D8D8"},
                                        hover: {fill: "#D8D8D8"},
                                        pressed: {fill: "#D8D8D8"},
                                    }}
                                />
                            ))}
                        </Geographies>
                        {/* Render markers here */}
                    </ZoomableGroup>
                </ComposableMap>
                <Tooltip />
            </div>
        );
    }
    renderMarker(proxy: Proxy): JSX.Element | null {
        const locationStr = proxy.location;
        if (locationStr) {
            const locations = locationStr.split(',').map(coord => parseFloat(coord));

            return (
                <Marker
                    key={proxy.id}
                    coordinates={[locations[1], locations[0]]}
                >
                    {/* ... */}
                </Marker>
            );
        } else {
            return null;
        }
    }

    mapProxyColor(proxy: Proxy): string {
        if (proxy.latency < 180 && proxy.stability >= 0.6) {
            return '#417505';
        } else if (proxy.latency < 300 && proxy.stability >= 0.4) {
            return '#F8E71C';
        } else if (proxy.latency < 500 && proxy.stability > 0.0) {
            return '#FF3824';
        } else {
            return '#000';
        }
    }

    async loadData() {
        const response = await axios.get(`${getBaseURL()}/api/v1/proxies?limit=4095`);
        const res: ResponseJSON = response.data;
        const proxies: Proxy[] = res.proxies;
        this.setState({
            proxies: proxies,
        });
    }
}


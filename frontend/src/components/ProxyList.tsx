import * as React from "react";
import axios from 'axios';

import {getBaseURL} from '../utils';

// import * as moment from 'moment';
const moment = require('moment')['default'];

export interface AppState {
    proxies: Array<any>,
}

export default class ProxyIPList extends React.Component<{}, AppState> {
    private initialState: AppState = {proxies: []};

    constructor(props: {}) {
        super(props);
        this.state = this.initialState;
    }

    render(): JSX.Element {
        // const { timesClicked, on } = this.state;
        return (
            <div>
                <h1>Proxy IP list</h1>

                {this.renderList2()}
            </div>
        );
    }

    renderList2(): JSX.Element {
        const list = this.state.proxies;
        return (
            <div>
                <table>
                    <thead>
                    <tr>
                        <th>IP</th>
                        <th>Port</th>
                        <th>Anonymous</th>
                        <th>Latency</th>
                        <th>Updated at</th>
                    </tr>
                    </thead>
                    <tbody>
                    {list.map(r =>
                        <tr key={`ip-` + r.ip}>
                            <td>{r.ip}</td>
                            <td>{r.port}</td>
                            <td>{r.is_anonymous ? 'Yes' : 'No'}</td>
                            <td>{r.latency.toFixed(0)} ms</td>
                            <td>{moment.unix(r.updated_at).format('YYYYMMDD HH:mm:ss')}</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        );
    }

    componentDidMount() {
        this.loadData();
    }

    async loadData() {
        const response = await axios.get(`${getBaseURL()}/api/v1/proxies`);
        const proxies: [any] = response.data.proxies;
        console.log(proxies);
        this.setState({proxies: proxies})
    }

}
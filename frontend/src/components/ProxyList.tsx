import * as React from "react";
import axios from 'axios';

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
                proxy ip list

                {this.renderList()}
            </div>
        );
    }

    renderList(): JSX.Element {
        return (
            <div>
                {this.state.proxies.map(p => {
                    return (
                        <div key={'proxy-' + p.id}>
                            <p>{p.ip}</p>
                        </div>
                    )
                })}
            </div>
        );
    }

    componentDidMount() {
        this.loadData();
    }

    async loadData() {
        const response = await axios.get('http://localhost:8000/api/v1/proxies');
        const proxies: [any] = response.data.proxies;
        console.log(proxies);
        this.setState({proxies: proxies})
    }

}
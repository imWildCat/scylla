import * as React from "react";
import axios from 'axios';

export interface AppState {
    timesClicked: number;
    on: boolean;
}

export default class ProxyIPList extends React.Component<{}, AppState> {
    private initialState: AppState = {timesClicked: 0, on: false};

    constructor(props: {}) {
        super(props);
        this.state = this.initialState;
    }

    render(): JSX.Element {
        // const { timesClicked, on } = this.state;
        return (
            <div>
                proxy ip list
            </div>
        );
    }

    componentDidMount() {
        axios.get('http://localhost:8000/api/v1/proxies')
    }

}